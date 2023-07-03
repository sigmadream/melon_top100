import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/72.0.3626.121 Safari/537.36"
    ),
}

def get_songs():
    res = requests.get("http://www.melon.com/chart/index.htm", headers=headers)
    res.raise_for_status()
    html = res.text
    soup = BeautifulSoup(html, "html.parser")  # HTML Parser
    tr_tag_list = soup.select(".d_song_list tbody tr")

    song_list = []

    for rank, tr_tag in enumerate(tr_tag_list, 1):
        song_no = tr_tag["data-song-no"]
        song_tag = tr_tag.select_one("a[href*=playSong]")
        album_tag = tr_tag.select_one(".wrap_song_info a[href*=goAlbumDetail]")
        artist_tag = tr_tag.select_one("a[href*=goArtistDetail]")

        song = {
            "song_no": song_no,
            "title": song_tag.text,
            "album": album_tag.text,
            "artist": artist_tag.text,
        }
        song_list.append(song)

    return song_list


def get_like_count(song_no_list):
    api_url = "https://www.melon.com/commonlike/getSongLike.json"
    params = {"contsIds": song_no_list}
    res = requests.get(api_url, params=params, headers=headers)
    res.raise_for_status()
    response = res.json()
    like_list = response["contsLike"]
    like_dict = {str(song["CONTSID"]): song["SUMMCNT"] for song in like_list}
    return like_dict
