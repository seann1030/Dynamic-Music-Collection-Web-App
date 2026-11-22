import argparse
import importlib
import sys
import traceback
from http.server import BaseHTTPRequestHandler, HTTPServer
import router

HOT_RELOAD = True  # Change to True, then restart, to reload Python code per request.
HOTRELOAD_PRESERVE_DATA = True  # Change to False to disable possibly buggy attempts
#                                 to preserve global data. If you do this, global
#                                 variables may be reset each request during hot reload.

# list of modules to hotreload.
reload_whitelist = [
    "router",
    "browse_page",
    "admin_page",
    "item_page",
    "database",
    "tools",
]

# list of types of variables that are likey _data_ and not _code_
# any of these properties will attempt to be cached if HOTRELOAD_PRESERVE_DATA is True
cacheable_types = [
    int,
    float,
    complex,
    str,
    list,
    tuple,
    range,
    dict,
    set,
    frozenset,
    bool,
    bytes,
    bytearray,
    type(None),
]

def do_hotreload():
    if not HOT_RELOAD:
        return

    data_cache = {}

    for mod_name in reload_whitelist:
        if mod_name not in sys.modules:
            continue
        module = sys.modules[mod_name]
        data_cache[mod_name] = {}

        if HOTRELOAD_PRESERVE_DATA:
            for key in dir(module):
                if key.startswith("__"):
                    continue  # don't cache internals.
                val = getattr(module, key)
                if type(val) in cacheable_types:
                    data_cache[mod_name][key] = val
        del sys.modules[mod_name]

    for mod_name, mod_saves in data_cache.items():
        importlib.import_module(mod_name)

        # restore any cached properties
        for key, val in mod_saves.items():
            setattr(sys.modules[mod_name], key, val)

    # finally, we gotta re-do the reloads for this actual file.
    global router
    import router


class RequestHandler(BaseHTTPRequestHandler):
    def reply(self, body, status, headers):
        # convert to bytes for network transmission
        if body is None:
            raw = None
        else:
            raw = body if isinstance(body, bytes) else body.encode("utf-8")

        # send minimal headers.
        self.protocol_version = "HTTP/1.1"
        self.send_response(status)

        # Send headers (plus a few we'll handle for you)
        for key, value in headers.items():
            self.send_header(key, value)

        if raw is not None:
            self.send_header("Content-Length", str(len(raw)))
            self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()

        if self.command != "HEAD" and raw is not None:
            self.wfile.write(raw)

    def c_read_body(self):
        length = int(self.headers.get("Content-Length", "0"))
        if length < 0:
            raise ValueError("Content-Length cannot be negative.")
        body = self.rfile.read(length).decode("utf-8")
        return body

    def do_GET(self):
        # Step 1: read the last bit of the request
        try:
            do_hotreload()
            message, response_code, headers = router.server(
                "GET", self.path, None, self.headers
            )
            # Step 3: send the response
            self.reply(message, response_code, headers)
        except Exception:
            # If your code crashes -- that's your fault 500
            traceback.print_exc()

            self.reply(
                "The server function crashed.", 500, {"Content-Type": "text/plain"}
            )
            raise

    do_HEAD = do_GET

    def do_POST(self):
        # Step 1: read the last bit of the request
        try:
            body = self.c_read_body()
        except Exception:
            # Can't read it -- that's the client's fault 400
            self.reply(
                "Couldn't read body as text", 400, {"Content-Type": "text/plain"}
            )
            raise

        try:
            do_hotreload()
            message, response_code, headers = router.server(
                "POST", self.path, body, self.headers
            )
            # Step 3: send the response
            self.reply(message, response_code, headers)
        except Exception:
            # If your code crashes -- that's your fault 500
            traceback.print_exc()

            self.reply(
                "The server function crashed.", 500, {"Content-Type": "text/plain"}
            )
            raise

    def do_DELETE(self):
        try:
            do_hotreload()
            message, response_code, headers = router.server(
                "DELETE", self.path, None, self.headers
            )
            # Step 3: send the response
            self.reply(message, response_code, headers)
        except Exception:
            # If your code crashes -- that's your fault 500
            traceback.print_exc()

            self.reply(
                "The server function crashed.", 500, {"Content-Type": "text/plain"}
            )
            raise

    def do_PUT(self):
        # Step 1: read the last bit of the request
        try:

            body = self.c_read_body()
        except Exception:
            # Can't read it -- that's the client's fault 400
            self.reply(
                "Couldn't read body as text", 400, {"Content-Type": "text/plain"}
            )
            raise

        try:
            do_hotreload()
            message, response_code, headers = router.server(
                "PUT", self.path, body, self.headers
            )
            # Step 3: send the response
            self.reply(message, response_code, headers)
        except Exception:
            traceback.print_exc()

            self.reply(
                "The server function crashed.", 500, {"Content-Type": "text/plain"}
            )
            raise


def run(port):
    print(f"Starting hobby collection: http://localhost:{port}/")
    with HTTPServer(("", port), RequestHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=4131)
    args = parser.parse_args()
    run(port=args.port)
