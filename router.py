import types
import json

import browse_page
import admin_page
import item_page
import tools
import database
import collection_page

def server(
    request_method: str,
    url: str,
    request_body: str | None,
    request_headers: dict[str, str],
) -> tuple[str | bytes, int, dict[str, str]]:

    response_body = None
    status = 200
    response_headers = {}

    if "?" in url:
        path, query = url.split("?", 1)
        parameters = tools.parse_query_parameters(query)
    else:
        path = url
        query = ""
        parameters = {}
    
    if (path.startswith("/admin/") or path.startswith("/api/admin/")) and not tools.validate_password(request_headers.get("Authorization", "")):
        return ("Unauthorized", 401,
            {
                "Content-Type": "text/plain; charset=utf-8",
                "WWW-Authenticate": 'Basic realm="Admin"'
            }
        )
    
    if request_method == "GET" and (path == "/" or path == "/home"):
        response_body = open("static/html/home.html", "r", encoding="utf-8").read()
        status = 200
        response_headers["Content-Type"] = "text/html; charset=utf-8"

    elif request_method == "GET" and path == "/browse":
        response_body = browse_page.browse_page(query)
        status = 200
        response_headers["Content-Type"] = "text/html; charset=utf-8"

    elif request_method == "GET" and path == "/admin/moderate":
        response_body = admin_page.generate_admin()
        status = 200
        response_headers["Content-Type"] = "text/html; charset=utf-8"

    elif request_method == "GET" and path.startswith("/api/item/"): # API endpoint for fetching item data
        item_parts = path.split("/")

        if len(item_parts) == 4 and item_parts[3].isdigit():
            page_id = int(item_parts[3])
            item = database.get_item(page_id)
        else:
            item = None

        if item is None:
            response_body = json.dumps({"error": "Item not found"})
            status = 404
        else:
            response_body = json.dumps(item)
            status = 200

        response_headers["Content-Type"] = "application/json; charset=utf-8"
    
    elif request_method == "GET" and (path == "/item" or path.startswith("/item/")):
        item_parts = path.split("/")

        if len(item_parts) == 3 and item_parts[2].isdigit():
            page_id = item_parts[2]
        else:
            page_id = ""

        if not page_id or database.get_item(int(page_id)) is None:
            response_body = item_page.no_item_found()
            status = 404
        else:
            response_body = item_page.item_page(page_id)
            status = 200

        response_headers["Content-Type"] = "text/html; charset=utf-8"

    elif request_method == "GET" and path == "/collection":
        response_body = collection_page.collection_page()
        status = 200
        response_headers["Content-Type"] = "text/html; charset=utf-8"

    elif request_method == "GET" and path == "/main.css":
        response_body = open("static/css/main.css", "r", encoding="utf-8").read()
        status = 200
        response_headers["Content-Type"] = "text/css; charset=utf-8"

    elif request_method == "GET" and path == "/comments.js":
        response_body = open("static/js/comments.js", "r", encoding="utf-8").read()
        status = 200
        response_headers["Content-Type"] = "text/javascript"

    elif request_method == "GET" and path == "/collection.js":
        response_body = open("static/js/collection.js", "r", encoding="utf-8").read()
        status = 200
        response_headers["Content-Type"] = "text/javascript"

    elif request_method == "GET" and path == "/admin.js":
        response_body = open("static/js/admin.js", "r", encoding="utf-8").read()
        status = 200
        response_headers["Content-Type"] = "text/javascript"
    
    elif request_method == "GET" and path == "/cd.png":
        response_body = open("static/images/cd.png", "rb").read()
        status = 200
        response_headers["Content-Type"] = "image/png"

    elif request_method == "GET" and path == "/Quicksand-VariableFont_wght.ttf":
        response_body = open("static/fonts/Quicksand-VariableFont_wght.ttf", "rb").read()
        status = 200
        response_headers["Content-Type"] = "font/ttf"

    elif request_method == "POST" and path.startswith("/item/"):
        item_parts = path.split("/")

        if len(item_parts) != 3 or not item_parts[2].isdigit():
            response_body = open("static/html/404.html", "r").read()
            status = 404

        else:
            page_id = int(item_parts[2])
            item = database.get_item(page_id)

            if item is None:
                response_body = open("static/html/404.html", "r").read()
                status = 404

            elif not request_headers.get("Content-Type", "").lower().startswith("application/x-www-form-urlencoded"):
                response_body = "<p>Invalid Content-Type</p>"
                status = 400

            else:
                form_data = tools.parse_query_parameters(request_body or "")

                name = form_data.get("name", "")
                comment = form_data.get("comment", "")

                if not name.strip() or not comment.strip():
                    response_body = item_page.item_page(
                        page_id, error_message="Name and comment cannot be empty.",
                        name=name, comment=comment
                    )
                    status = 400

                elif len(name) > 80:
                    response_body = item_page.item_page(
                        page_id, error_message="Name cannot exceed 80 characters.",
                        name=name, comment=comment
                    )
                    status = 413

                elif len(comment) > 500:
                    response_body = item_page.item_page(
                        page_id, error_message="Comment cannot exceed 500 characters.",
                        name=name, comment=comment
                    )
                    status = 413

                else:
                    database.save_comment(page_id, name, comment)
                    response_body = item_page.item_page(page_id)
                    status = 201

        response_headers["Content-Type"] = "text/html; charset=utf-8"

    elif request_method == "DELETE" and path.startswith("/api/admin/comments/"):
        comment_parts = path.split("/")

        if len(comment_parts) != 5 or not comment_parts[4].isdigit():
            response_body = json.dumps({"error": "Invalid comment ID"})
            status = 404

        else:
            comment_id = int(comment_parts[4])
            comments = database.load_all_comments()

            comment_exists = any(
                comment["id"] == comment_id for comment in comments
            )

            if not comment_exists:
                response_body = json.dumps({"error": "Comment not found"})
                status = 404

            else:
                database.delete_comment(comment_id)
                response_body = None
                status = 204

        if status != 204:
            response_headers["Content-Type"] = "application/json; charset=utf-8"

    elif request_method == "PUT" and path.startswith("/api/admin/comments/"):
        comment_parts = path.split("/")

        if len(comment_parts) != 5 or not comment_parts[4].isdigit():
            response_body = json.dumps({"error": "Invalid comment ID"})
            status = 404

        elif not request_headers.get("Content-Type", "").lower().startswith("application/json"):
            response_body = json.dumps({"error": "Invalid Content-Type"})
            status = 400

        else:
            try:
                data = json.loads(request_body or "")
            except (json.JSONDecodeError, TypeError):
                data = None

            if not isinstance(data, dict) or not isinstance(data.get("disemvoweled"), bool):
                response_body = json.dumps({"error": "Invalid request body"})
                status = 400

            else:
                comment_id = int(comment_parts[4])
                comments = database.load_all_comments()
                comment = next(
                    (c for c in comments if c["id"] == comment_id),
                    None
                )

                if comment is None:
                    response_body = json.dumps({"error": "Comment not found"})
                    status = 404

                else:
                    if data["disemvoweled"]:
                        new_text = "".join(
                            char for char in comment["comment"]
                            if char not in "aeiouAEIOU"
                        )

                        database.edit_comment(comment_id, new_comment=new_text)
                        comment["comment"] = new_text

                    response_body = json.dumps(comment)
                    status = 200

        response_headers["Content-Type"] = "application/json; charset=utf-8"

    else:
        # final catch-all
        response_body = open("static/html/404.html", "r", encoding="utf-8").read()
        status = 404
        response_headers["Content-Type"] = "text/html; charset=utf-8"

    return response_body, status, response_headers
