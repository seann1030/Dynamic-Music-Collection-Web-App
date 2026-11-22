from database import get_item, load_items, load_comments_for_item
import random # random module to shuffle recommendations
import tools

def no_item_found() -> str: # returns an HTML page if no item is found
    no_item_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>No Item Found</title>
        <link rel="stylesheet" href="/main.css">
    </head>
    <body>
        <header>
            <h1>No Item Found</h1>
            <nav>
                <a href="/home">Home</a>
                <a href="/browse">Browse Items</a>
                <a href="/collection">Collection</a>
                <a href="/admin/moderate">Admin</a>
            </nav>
        </header>

        <main>
            <h2>Item Not Found</h2>
            <p>The item you are looking for does not exist.</p>
            <a class="back-button" href="/browse">Back to Browse</a>
        </main>
    </body>
    </html>
    """
    return no_item_html

def item_page(page_id, error_message="", name="", comment="") -> str:
    if (str(page_id).isdigit() == False):  # check if the page_id is not a digit
        return no_item_found()

    page_id = int(page_id)
    item = get_item(page_id)
    
    if item is None:  # check if the item was not found in the database
        return no_item_found()
    
    items = load_items()
    recommendations = []
    other_categories = []

    for other_item in items:
        if other_item["id"] != item["id"]:
            if other_item["category"] == item["category"]:
                recommendations.append(other_item)
            else:
                other_categories.append(other_item)

    random.shuffle(recommendations)
    recommendations = recommendations[:4] # limit recommendations to 4 items

    random.shuffle(other_categories)

    if len(recommendations) < 4:
        remaining = 4 - len(recommendations)
        recommendations += other_categories[:remaining]
            
    recommendations_html = ""

    for recommended in recommendations:
        recommendations_html += f"""
        <div class="recommendation">
            <a href="/item/{recommended['id']}">
                <img src="{recommended['image']}" alt="{recommended['alt']}">
                <p>{recommended['name']}</p>
            </a>
        </div>
        """
    
    # load comments for the current item
    comments = load_comments_for_item(page_id)
    comments_html = ""

    if len(comments) == 0:
        comments_html = "<p>No comments yet.</p>"
    else:
        for current_comment in comments:
            commenter_name = tools.escape_html(current_comment["name"])
            comment_text = tools.escape_html(current_comment["comment"])

            comments_html += f"""
                <div class="comment">
                    <h3>{commenter_name}</h3>
                    <p>{comment_text}</p>
                </div>
            """
            
    # display server side validation errors and preserve submitted form values
    escaped_name = tools.escape_html(name) 
    escaped_comment = tools.escape_html(comment)

    error_html = ""
    if error_message:
        error_html = f'<p class="form-error">{tools.escape_html(error_message)}</p>'
        
    recommendations_section = "" 

    if recommendations: # only show the recommendations section if there are recommended items
        recommendations_section = f"""
        <section class="recommendations">
            <h2>Recommended Albums</h2>
            <div class="recommendations-list">
                {recommendations_html}
            </div>
        </section>
        """
    
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Item Details</title>
        <link rel="stylesheet" href="/main.css">
        <script src="/comments.js" defer></script>
        <script src="/collection.js" defer></script>
    </head>
    <body>
        <header>
            <h1>Item Details</h1>
            <nav>
                <a href="/home">Home</a>
                <a href="/browse">Browse Items</a>
                <a href="/collection">Collection</a>
                <a href="/admin/moderate">Admin</a>
            </nav>
        </header>

        <main>
            <div class="item-layout">
                <div class="item-left">
                    <section class="item-details">
                        <h2>{item["name"]}</h2>
                        <img src="{item["image"]}" alt="{item["alt"]}">
                        <p class="category">{item["category"]}</p>
                        <p class="description">{item["description"]}</p>
                        <button class="collection-button" data-id="{item['id']}">
                            Save to Collection
                        </button>
                    </section>

                    <a class="back-button" href="/browse">Back to Browse</a>
                </div>
                {recommendations_section} 
            </div>

            <div class="comments-bottom">
                <section class="comments-list">
                    <h2>Comments</h2>
                    {comments_html}
                </section>
                
                <section class="comments-form">
                    <h2>Leave a Comment</h2>
                    {error_html}
                    
                    <form action="/item/{page_id}" method="POST">
                        <label for="name">Name (up to 80 characters):</label>
                        <input type="text" id="name" name="name" value="{escaped_name}">

                        <label for="comment">Comment:</label>
                        <textarea id="comment" name="comment" rows="4">{escaped_comment}</textarea>
                        <p id="character-counter">Characters left: 500</p>


                        <button type="submit">Submit Comment</button>
                    </form>
                </section>
            </div>
        </main>
    
    </body>
    </html>
    """
    return html
