from typing import Union

import requests
from bs4 import BeautifulSoup

_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/72.0.3626.121 Safari/537.36"
    ),
}


def get_songs() -> list[dict[str, str]]:
    res = requests.get("http://www.melon.com/chart/index.htm", headers=_HEADERS)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")
    tr_tag_list = soup.select(".d_song_list tbody tr")

    song_list: list[dict[str, str]] = []

    for tr_tag in tr_tag_list:
        song_no = tr_tag["data-song-no"]
        song_tag = tr_tag.select_one("a[href*=playSong]")
        album_tag = tr_tag.select_one(
            ".wrap_song_info a[href*=goAlbumDetail], "
            ".wrap_song_info a[href*=albumId], "
            ".wrap_song_info a[href*='album/detail']"
        )
        artist_tag = tr_tag.select_one(
            "a[href*=goArtistDetail], "
            "a[href*=artistId], "
            "a[href*='artist/detail']"
        )

        if not (song_tag and album_tag and artist_tag):
            continue

        song_list.append(
            {
                "song_no": song_no,
                "title": song_tag.text,
                "album": album_tag.text,
                "artist": artist_tag.text,
            }
        )

    return song_list


def get_like_count(song_no_list: Union[int, list[int]]) -> dict[str, int]:
    api_url = "https://www.melon.com/commonlike/getSongLike.json"
    if isinstance(song_no_list, list):
        conts_ids = ",".join(str(n) for n in song_no_list)
    else:
        conts_ids = str(song_no_list)
    params = {"contsIds": conts_ids}
    res = requests.get(api_url, params=params, headers=_HEADERS)
    res.raise_for_status()
    response = res.json()
    like_list: list[dict] = response["contsLike"]
    return {str(song["CONTSID"]): song["SUMMCNT"] for song in like_list}


if __name__ == "__main__":
    songs = get_songs()
    print(songs)