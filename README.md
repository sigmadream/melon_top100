# MelonTop100

This is a simple package that brings up the Top 100 list of Melon, a music site in Korea.

If you use the `get_songs()` function, you can check Melon's Top 100 songs in the form of a list, and the items in the list are provided as a dictionary containing information such as song name and singer.

## Use

```python
from melon_top100 import get_songs

top100 = get_songs()
```