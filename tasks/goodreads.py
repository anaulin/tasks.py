"""GoodReads-related operations."""
import csv
import requests
import toml

from datetime import datetime
from . import entry

DEFAULT_BLOG_DST = "/Users/anaulin/src/github.com/anaulin/blog/"
CONTENT_SUBDIR = "/content/blog/"
IMG_SUBDIR = "/static/img/"


def import_to_blog(goodreads_csv,
    dst=DEFAULT_BLOG_DST, img_dir=IMG_SUBDIR, content_dir=CONTENT_SUBDIR):
    """Imports a GoodReads library export CSV into Hugo posts with book metadata.
    """
    with open(goodreads_csv) as library:
        reader = csv.DictReader(library)
        for row in reader:
            _to_blog_entry(row, dst, img_dir, content_dir)


def _to_blog_entry(row, dst_dir, img_dir, content_dir):
    if "https://anaulin.org" in row["My Review"]:
        return

    if not row["My Review"] or not row["My Review"].strip():
        return

    book_slug = entry.to_slug(row['Title'])
    date = _get_date(row)
    cover_img = _get_cover_for_isbn(
        row['ISBN'], book_slug, f"{dst_dir}{img_dir}")
    meta = {
        "title": f"Book Notes: {row['Title']}",
        "date": date,
        "tags": ["books"],
        "book": {
            "title": row["Title"],
            "author": row["Author"],
            "url": f"https://www.goodreads.com/book/show/{row['Book Id']}",
            "end": date,
            "rating": row["My Rating"],
            "image": f"/img/{cover_img}"
        }
    }

    content = row["My Review"]

    filename = f"{dst_dir}{content_dir}book-notes-{book_slug}.md"
    with open(filename, 'w') as outfile:
        outfile.write("+++\n")
        outfile.write(toml.dumps(meta))
        outfile.write("+++\n")
        outfile.write(content)


def _get_date(row):
    raw_date = row["Date Read"] if row["Date Read"] else row["Date Added"]
    return datetime.strptime(raw_date, '%Y/%m/%d')

def _get_cover_for_isbn(mangled_isbn, slug, dst_dir):
    isbn = mangled_isbn.replace('=', '').replace('"', '')
    url = f"http://covers.openlibrary.org/b/isbn/{isbn}-L.jpg"
    res = requests.get(url)
    if (res.status_code != 200
        or 'content-type' not in res.headers
            or res.headers['Content-Type'] != 'image/jpeg'):
        return ""

    img_name = f"book-{slug}.jpg"
    with open(f"{dst_dir}{img_name}", 'wb') as fd:
        for chunk in res.iter_content():
            fd.write(chunk)

    return img_name
