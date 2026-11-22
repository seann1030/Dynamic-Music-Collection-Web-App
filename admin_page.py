import database
import tools

def generate_admin():
    """Return the admin page HTML. This should contain all comments in a table."""

    page = """
    <!DOCTYPE html>
    <html lang="en">

    <head>
        <meta charset="UTF-8">
        <title>Admin</title>
        <link rel="stylesheet" href="/main.css">
    </head>

    <body>
        <header>
            <h1>Comment Administration</h1>
            <nav>
                <a href="/home">Home</a>
                <a href="/browse">Browse Items</a>
                <a href="/collection">Collection</a>
                <a href="/admin/moderate">Admin</a>
            </nav>
        </header>

        <table>
            <tr>
                <th>Item</th>
                <th>Commenter</th>
                <th>Comment</th>
                <th>Actions</th>
            </tr>
    """

    # load all comments from the database and generate table rows for each comment
    comments = database.load_all_comments()

    for comment in comments: 
        item_id = comment.get("item_id", "")
        name = comment.get("name", "")
        comment_text = comment.get("comment", "")
        comment_id = comment["id"]

        # escape HTML to prevent injection
        item_id_escaped = tools.escape_html(str(item_id))
        name_escaped = tools.escape_html(name)
        comment_text_escaped = tools.escape_html(comment_text)

        page += f"""
            <tr data-id="{comment_id}">
                <td>{item_id_escaped}</td>
                <td>{name_escaped}</td>
                <td class="comment-text">{comment_text_escaped}</td>
                <td>
                    <button class="delete-button">Delete</button>
                    <button class="disemvowel-button">Disemvowel</button>
                    <p class="row-message"></p>
                </td>
            </tr>
        """

    
    page += """
        </table>
        <p id="admin-message"></p>
        <script src="/admin.js" defer></script>
    </body>
    </html>
    """
    return page