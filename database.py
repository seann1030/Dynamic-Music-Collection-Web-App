import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DEFAULT_DATA = ROOT / "items.json"

DEFAULT_COMMENTS = ROOT / "comments.json"


def load_items(path=DEFAULT_DATA):
    """reads a json file into your server. We will add more functions later to help you "fake" a proper database with a file."""
    return json.loads(Path(path).read_text(encoding="utf-8"))


def get_item(id, path=DEFAULT_DATA):
    """Reads the items file and returns either the item with matching `id`, or `None`
    **NOTE**: id matching is type sensitive.
    Unless your IDs are stored as string in the item file, you will likely need to perform a string->int conversion
    elsewhere in the code to get data to match."""
    for item in load_items(path=path):
        if item["id"] == id:
            return item
    return None


def load_all_comments(path=DEFAULT_COMMENTS):
    """reads the comments file and returns the list of comments"""
    with open(path, "r", encoding="utf-8") as f:
        comments = json.load(f)
        return comments


def load_comments_for_item(item_id, path=DEFAULT_COMMENTS):
    """reads the comments file and returns the list of comments matching a given id"""
    comments = load_all_comments(path)
    # filter comments list to only those with a matching item_id.
    comments = [c for c in comments if str(c["item_id"]) == str(item_id)]
    return comments


def save_comment(item_id, name, comment, path=DEFAULT_COMMENTS):
    """saves a single comment to the comments file. will simply add it to the end of the list.

    NOTE this modifies your comment file. You may wish to save a "clean" version."""

    comments = load_all_comments(path)

    comment = {
        "id": max((existing["id"] for existing in comments), default=0) + 1,
        "item_id": item_id,
        "name": name,
        "comment": comment,
    }

    comments.append(comment)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(comments, f)

    return comment["id"]

def delete_comment(comment_id, path=DEFAULT_COMMENTS):
    comments = load_all_comments()

    before_len = len(comments)
    comments = [
        comment for comment in comments if str(comment["id"]) != str(comment_id)
    ]
    after_len = len(comments)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(comments, f)
    # return True if a comment was removed, false if not.


def edit_comment(comment_id, new_name=None, new_comment=None, path=DEFAULT_COMMENTS):
    """Edit a comment. If new_name or new_comment are None, make no change to that field
    Returns True if a change was made."""
    made_edit = False
    comments = load_all_comments()
    for comment in comments:
        if str(comment["id"]) == str(comment_id):
            if new_name is not None:
                comment["name"] = new_name
                made_edit = True
            if new_comment is not None:
                comment["comment"] = new_comment
                made_edit = True

    with open(path, "w", encoding="utf-8") as f:
        json.dump(comments, f)
    return made_edit


def write_ids_on_v3_comment_file(path=DEFAULT_COMMENTS):
    """used to take a v3 style (no comment id) data file and upgrade it for v4 server use"""
    id = 1
    comments = load_all_comments()
    for comment in comments:
        comment["id"] = id
        id += 1
    with open(path, "w", encoding="utf-8") as f:
        json.dump(comments, f)

if __name__ == "__main__":

    response = input(
        f"Do you want to upgrade your v3 comments file ({DEFAULT_COMMENTS})? (y/N): "
    )
    if response.strip().lower() in ("y", "yes"):
        write_ids_on_v3_comment_file()
    elif response.strip().lower() in ("n", "no"):
        print("groovy. Later")
    else:
        print(
            "I didn't recognize your answer. please use y or yes or n or no next time"
        )
