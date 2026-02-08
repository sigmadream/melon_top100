import requests
from bs4 import BeautifulSoup

_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/72.0.3626.121 Safari/537.36"
    ),
}

_CHART_URL = "https://music.bugs.co.kr/chart/track/realtime/total"


def get_songs() -> list[dict[str, str]]:
    res = requests.get(_CHART_URL, headers=_HEADERS)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")
    rows = soup.select("table.byChart tbody tr")

    song_list: list[dict[str, str]] = []

    for row in rows:
        track_id = row.get("trackid")
        title_tag = row.select_one("p.title a")
        artist_tag = row.select_one("p.artist a")
        album_tag = row.select_one("a.album")

        if not (track_id and title_tag and artist_tag and album_tag):
            continue

        song_list.append(
            {
                "track_id": track_id,
                "title": title_tag.text.strip(),
                "artist": artist_tag.text.strip(),
                "album": album_tag.text.strip(),
            }
        )

    return song_list
