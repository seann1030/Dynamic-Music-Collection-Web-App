def collection_page() -> str:
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>My Collection</title>
        <link rel="stylesheet" href="/main.css">
        <script src="/collection.js" defer></script>
    </head>
    <body>
        <header>
            <h1>My Collection</h1>
            <nav>
                <a href="/home">Home</a>
                <a href="/browse">Browse Items</a>
                <a href="/collection">My Collection</a>
                <a href="/admin/moderate">Admin</a>
            </nav>
        </header>

        <main>
            <div class="card_list" id="collection-list"></div>

            <p id="empty-collection" hidden>Your collection is empty.</p>
        </main>
    </body>
    </html>
    """

    return html
