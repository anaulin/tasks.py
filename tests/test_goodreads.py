import os
import tempfile

from .context import goodreads

TEST_GOODREADS_CSV = os.path.join(
    os.path.dirname(__file__), "test_goodreads_export.csv")


def test_import_to_blog():
    with tempfile.TemporaryDirectory() as tmp_dirname:
        goodreads.import_to_blog(
            TEST_GOODREADS_CSV, dst=tmp_dirname, img_dir="/", content_dir="/")
        assert 'book-no-time-to-spare-thinking-about-what-matters.jpg' in os.listdir(
            tmp_dirname)
        assert 'book-notes-no-time-to-spare-thinking-about-what-matters.md' in os.listdir(
            tmp_dirname)
