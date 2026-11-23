

\# Dynamic Music Collection Web App



A full-stack web application built with Python, HTML, CSS, and JavaScript that allows users to browse, explore, and save their favorite music albums and EPs.



The application features a custom Python HTTP server, dynamically generated pages, genre-based filtering, album recommendations, user comments, and an administrative moderation system. It also uses REST-style API endpoints and browser localStorage to manage personalized music collections.



\## Technologies Used



| Category | Technologies |

|---|---|

| Backend | Python 3, Python HTTP Server |

| Frontend | HTML5, CSS3, JavaScript |

| Data Storage | JSON files, Browser localStorage |

| API | REST-style HTTP endpoints, Fetch API |

| Authentication | HTTP Basic Authentication |

| Version Control | Git, GitHub |



The backend is implemented using Python's built-in `http.server` module without external web frameworks such as Flask or Django.



\## Features



\### Dynamic Music Browsing



\- Browse a collection of music albums and EPs.

\- Filter albums by music genre.

\- Navigate through paginated results, displaying six albums per page.

\- View individual album pages with descriptions, images, and genre information.



\### Personalized Music Collection



\- Save albums to a personal collection.

\- Remove albums from the collection.

\- Persist saved albums using browser localStorage.

\- Dynamically retrieve saved album information using JavaScript's Fetch API.

\- Handle failed API requests with error messages and retry functionality.



\### Album Recommendations



\- Display up to four recommended albums on individual album pages.

\- Prioritize recommendations from the same genre.

\- Include albums from other genres when fewer than four matching albums are available.

\- Randomize recommendations to provide variety.



\### User Comments



\- Submit comments on individual album pages.

\- View comments associated with each album.

\- Validate comment submissions on both the client and server.

\- Enforce an 80-character limit for names and a 500-character limit for comments.

\- Store submitted comments in a JSON file.



\### Admin Comment Moderation



\- Access a protected administration page using HTTP Basic Authentication.

\- View submitted comments in a centralized table.

\- Delete comments using asynchronous HTTP DELETE requests.

\- Disemvowel comments using HTTP PUT requests.

\- Dynamically update the interface without reloading the page.



\## Project Architecture



The application uses a custom Python HTTP server with separate modules for routing, page generation, and data management.



\### Backend



\- `main.py` starts the HTTP server and processes incoming requests.

\- `router.py` handles HTTP routing and determines the appropriate response.

\- `database.py` manages reading and writing JSON data.

\- `browse\_page.py` generates album browsing pages with filtering and pagination.

\- `item\_page.py` generates individual album pages, recommendations, and comments.

\- `collection\_page.py` generates the personal collection page.

\- `admin\_page.py` generates the comment moderation interface.

\- `tools.py` provides utility functions for request parsing, HTML escaping, and authentication.



\### Frontend



\- HTML provides the structure of the web pages.

\- CSS handles styling and layout.

\- JavaScript manages interactive features, API requests, and browser storage.



\### Data Storage



The application uses two JSON files as a lightweight data store:



\- `items.json` stores album information.

\- `comments.json` stores user-submitted comments.



Saved album collections are stored separately in the user's browser using localStorage.



No external database server is required.



\## Getting Started



\### Prerequisites



Before running the application, make sure you have:



\- Python 3.10 or later

\- Git (optional, for cloning the repository)

\- A modern web browser



The application uses Python's standard library and does not require installing third-party Python packages.



\### 1. Download the Project



Clone the repository using Git:



```bash

git clone <repository-url>

```



Alternatively, download the project as a ZIP file and extract its contents.



\### 2. Navigate to the Project Directory



Open a terminal in the folder containing `main.py`.



```bash

cd "Dynamic Music Collection Web App"

```



\### 3. Start the Server



Run:



```bash

python main.py

```



The application starts on port 4131 by default.



You can also specify a different port:



```bash

python main.py --port 8080

```



\### 4. Open the Application



Open your browser and navigate to:



```text

http://localhost:4131

```



The application should now be running locally.



To stop the server, press `Ctrl + C` in the terminal.



\## Application Routes



| Method | Endpoint | Description |

|---|---|---|

| GET | `/home` | Display the homepage |

| GET | `/browse` | Browse available albums |

| GET | `/browse?category=...\&page=...` | Filter and paginate albums |

| GET | `/item/{id}` | View album details and comments |

| POST | `/item/{id}` | Submit an album comment |

| GET | `/collection` | View saved albums |

| GET | `/api/item/{id}` | Retrieve album information as JSON |

| GET | `/admin/moderate` | Access the protected moderation page |

| DELETE | `/api/admin/comments/{id}` | Delete a comment |

| PUT | `/api/admin/comments/{id}` | Modify a comment through the moderation API |



\## API Integration



The application implements REST-style endpoints to support asynchronous communication between the frontend and backend.



\### Retrieve Album Information



```http

GET /api/item/1

```



Returns the album's JSON data if the requested item exists.



The frontend uses this endpoint to retrieve saved albums when displaying the user's collection.



\### Delete a Comment



```http

DELETE /api/admin/comments/1

```



Deletes the specified comment.



A successful deletion returns HTTP status `204 No Content`.



\### Disemvowel a Comment



```http

PUT /api/admin/comments/1

Content-Type: application/json



{

&#x20; "disemvoweled": true

}

```



Removes vowels from the specified comment and returns the updated comment as JSON.



Administrative API endpoints require HTTP Basic Authentication.



\## Client-Side Storage



The application uses the browser's localStorage API to persist a user's saved music collection.



When an album is saved:



1\. JavaScript retrieves the existing collection from localStorage.

2\. The album ID is added to the collection.

3\. The updated collection is saved as JSON.

4\. The interface updates to reflect the saved state.



When the collection page loads, JavaScript retrieves the saved album IDs and fetches their information from the backend.



This allows saved albums to persist across browser sessions without requiring user accounts or a database.



\## Comment Management



Comments are stored in `comments.json`.



When a user submits a comment:



1\. The browser validates the form input.

2\. The server receives the POST request.

3\. The backend validates the submitted name and comment.

4\. The comment is assigned an ID and saved to the JSON file.

5\. The updated album page displays the comment.



Administrative users can moderate submitted comments through the protected administration interface.



\## Security Considerations



The project includes basic security measures such as:



\- HTTP Basic Authentication for administrative routes.

\- Client-side and server-side comment validation.

\- HTML escaping for user-submitted comments.

\- Request validation and HTTP error responses.



\*\*Note:\*\* The current implementation contains hardcoded administrative credentials in `tools.py`. These should be replaced with securely managed credentials before deploying the application publicly.



HTTP Basic Authentication should also only be used over HTTPS when handling real credentials.



This project is intended for local development and educational use rather than production deployment.



\## Project Structure



```text

Dynamic Music Collection Web App/

│

├── main.py

├── router.py

├── database.py

├── browse\_page.py

├── item\_page.py

├── collection\_page.py

├── admin\_page.py

├── tools.py

│

├── items.json

├── comments.json

├── comments\_empty.json

├── attributions.md

│

└── static/

&#x20;   ├── css/

&#x20;   │   └── main.css

&#x20;   │

&#x20;   ├── html/

&#x20;   │   ├── home.html

&#x20;   │   ├── admin.html

&#x20;   │   └── 404.html

&#x20;   │

&#x20;   ├── js/

&#x20;   │   ├── collection.js

&#x20;   │   ├── comments.js

&#x20;   │   └── admin.js

&#x20;   │

&#x20;   ├── images/

&#x20;   │   └── cd.png

&#x20;   │

&#x20;   └── fonts/

&#x20;       ├── Quicksand-VariableFont\_wght.ttf

&#x20;       └── OFL.txt

```



\## Future Improvements



Potential improvements include:



\- Migrating JSON file storage to a relational database.

\- Implementing secure user authentication and individual accounts.

\- Replacing hardcoded administrative credentials with environment-based configuration.

\- Adding search functionality for albums and artists.

\- Expanding music recommendations.

\- Improving responsive design and accessibility.

\- Adding automated unit and integration tests.

\- Deploying the application to a cloud hosting platform.



\## Author



\*\*Sean Nguyen\*\*



GitHub: \[seann1030](https://github.com/seann1030)



\## Attributions



See \[attributions.md](attributions.md) for project asset attributions.



