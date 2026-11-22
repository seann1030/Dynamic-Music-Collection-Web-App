from database import load_items
import tools

PAGE_SIZE = 6

def browse_page(query_parameters: str) -> str:

    items = load_items() 

    parameters = tools.parse_query_parameters(query_parameters) # parse query parameters
    
    categories = sorted(set(item["category"] for item in items)) # get all available categories

    category = parameters.get("category", "All") # get selected category, default is All
    
    if category not in categories: # if category does not exist show all items
        category = "All"
        
    if category != "All": # filter items by selected category
        items = [item for item in items if item["category"] == category]
    
    page = 1 # default page
    
    if (parameters.get("page") or "").isdigit():
        page = int(parameters["page"])
        
        if page < 1:
            page = 1

    total_pages = len(items) // PAGE_SIZE

    if len(items) % PAGE_SIZE != 0: # check if there are remaining items
        total_pages = total_pages + 1
        
    if category != "All" and page > total_pages: # if the current page exceeds total pages for the selected category, reset to page 1
        page = 1

    start = (page - 1) * PAGE_SIZE # find where the current page starts and ends
    end = start + PAGE_SIZE

    page_items = items[start:end] # get items for current page

    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>My Favorite Albums &amp; EPs</title>
        <link rel="stylesheet" href="/main.css">
        <script src="/collection.js" defer></script>
    </head>
    <body>
    <header>
        <h1>My Favorite Albums &amp; EPs</h1>
        <nav>
            <a href="/home">Home</a>
            <a href="/browse">Browse Items</a>
            <a href="/collection">Collection</a>
            <a href="/admin/moderate">Admin</a>
        </nav>
    </header>
    """

    html += """
    <form class="category-filter" action="/browse" method="GET">
        <label for="category">Filter by Genre:</label>
        <select id="category" name="category">
    """

    if category == "All":
        html += '<option value="" selected>All Genres</option>'
    else:
        html += '<option value="">All Genres</option>'

    for option in categories:
        selected = "selected" if category == option else ""
        label = option + " Music"
        html += f'<option value="{option}" {selected}>{label}</option>'

    html += """
        </select>
        <button type="submit">Filter</button>
    </form>
    """
    
    html += '<div class="card_list">'

    if len(page_items) == 0:
        html += "<p>No items found</p>"
    
    for item in page_items: # generate item cards
        html += f"""
    <div class="card" data-id="{item['id']}">
        <h2><a href="/item/{item['id']}">{item["name"]}</a></h2>
        <img src="{item["image"]}" alt="{item["alt"]}">
        <p class="category">{item["category"]}</p>
        <p class="description">{item["description"]}</p>
        
        <button class="collection-button" data-id="{item['id']}">
            Save to Collection
        </button>
    </div>
    """
    html += "</div>"

    html += '<div class="pagination">'

    encoded_category = category.replace("&", "%26").replace(" ", "+") # encode category for URL

    if page > 1:
        html += f'<a href="/browse?category={encoded_category}&amp;page={page - 1}">Previous</a>'

    html += f"<p>Page {page} of {total_pages}</p>"

    if page < total_pages:
        html += f'<a href="/browse?category={encoded_category}&amp;page={page + 1}">Next</a>'

    html += "</div>"
    html += """
    </body>
    </html>
    """

    return html
