# MelonTop100

This is a simple package that brings up the Top 100 list of Melon, a music site in Korea.

If you use the `get_songs()` function, you can check Melon's Top 100 songs in the form of a list, and the items in the list are provided as a dictionary containing information such as song name and singer.

## Setup(Dev)

```
$ python -m venv venv
$ .\venv\Scripts\activate
(venv) $ python -m pip install -U pip setuptools wheel pip
(venv) $ python -m pip install -U build twine
(venv) $ python -m build .
(venv) $ python -m pip install .\dist\melon_top100-1.0.0-py3-none-any.whl --force-reinstall
```

## Use

```python
$ pip install melon-top100
$ python

from melon_top100 import get_songs, get_like_count

>>> top100 = get_songs()
... {'song_no': '34754292', 'title': 'TOMBOY', 'album': 'I NEVER DIE', 'artis '(여자)아이들'}, ...


>>> get_like_count(34754292)
{'34754292': 137492}
```
