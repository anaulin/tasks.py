# tasks.py <!-- omit in toc -->

Python-based task scripts, for running via [pyinvoke](http://www.pyinvoke.org/).

- [Installation](#installation)
- [Running](#running)
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
