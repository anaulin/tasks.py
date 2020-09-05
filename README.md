# tasks.py <!-- omit in toc -->

Python-based task scripts, for running via [pyinvoke](http://www.pyinvoke.org/).

- [Installation](#installation)
- [Running](#running)
  - [Available tasks](#available-tasks)
- [Environment and dependencies setup](#environment-and-dependencies-setup)

## Installation

Requires Python 3.

Install dependencies with `pip` or `easy_install`:
```
pip install -r requirements.txt
```

## Running

Run tasks via the `invoke` command (or `inv`, for short).

List available tasks:
```
$ inv -l
```

To get more help about a specific task:
```
$ inv -h <task-name>
```

To invoke a task:
```
$ inv <task-name>
```

### Available tasks

```
$ inv -l

Available tasks:

  backup                 Copies the origin_file into the backups directory, adding a timestamp suffix to the
                         filename
  deploy                 Deploy blog.
  extract-clippings      Use the local clippings.py installation to extract clippings from the attached Kindle.
  mastodon-login         Logs into Mastodon and creates local credentials files.
  publish                Publishes the given entry and deploys it.
  send-to-indiewebnews   Sends webmention to news.indieweb.org, adds appropriate syndication URLs.
  send-to-indiewebxyz    Adds appropriate syndication URLs and submits the entry to the chosen indieweb.xyz sub.
  start-reading          Start a draft entry about this book.
  toot-entry             Posts a toot about the given blog entry.
```

## Environment and dependencies setup

Create new virtual env:
```
python3 -m venv .venv
```

Activate virtual env:
```
source .venv/bin/activate
```

Install requirements:
```
pip install -r requirements.txt
```

Run the tests:
```
pytest
```
