import base64

ADMIN_USER = "goldie"
ADMIN_PASS = "G04_life"  # capitol G, number 0, number 4, underscore, life.

def validate_password(header_value):
    try:
        # decode header_value into username and password
        if header_value.startswith("Basic "):
            encoded_credentials = header_value[6:] # remove Basic prefix
            decoded_bytes = base64.b64decode(encoded_credentials, validate=True) # decode base64
            decoded_str = decoded_bytes.decode("utf-8") # decode bytes to string
            username, password = decoded_str.split(":", 1) 

            # check the username and password
            if username == ADMIN_USER and password == ADMIN_PASS:
                return True

        return False
    except:
        # If something goes wrong just return false.
        return False

def unescape_url(url_formatted_str):
    import urllib.parse

    # NOTE -- this is the only place urllib is allowed on this assignment.
    return urllib.parse.unquote_plus(url_formatted_str)


def parse_query_parameters(query: str) -> dict[str, str]:
    if query == "":
        return {}
    pairs = query.split("&")
    output = {}
    for pair in pairs:
        if "=" in pair:
            K, V = pair.split("=", 1)
            K = unescape_url(K)
            V = unescape_url(V)
            output[K] = V
        else:
            # this is not a perfect fallback, but it's fine
            K = unescape_url(pair)
            output[K] = None
    return output


def escape_html(text):
    import html

    return html.escape(text)
