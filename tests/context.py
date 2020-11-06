"""Helper to import code under test into tests."""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tasks import entry
from tasks import goodreads
from tasks import webmention
