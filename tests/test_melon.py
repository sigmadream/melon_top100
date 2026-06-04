import pytest
import responses
from requests.exceptions import HTTPError

from melon_top100.melon import get_like_count, get_songs

SAMPLE_HTML = """
<div class="d_song_list">
<table>
<tbody>
<tr data-song-no="12345">
  <td>
    <div class="wrap_song_info">
      <a href="javascript:melon.play.playSong('12345');">첫 번째 노래</a>
      <a href="javascript:melon.link.goAlbumDetail('111');">첫 번째 앨범</a>
      <a href="javascript:melon.link.goArtistDetail('222');">가수A</a>
    </div>
  </td>
</tr>
<tr data-song-no="67890">
  <td>
    <div class="wrap_song_info">
      <a href="javascript:melon.play.playSong('67890');">두 번째 노래</a>
      <a href="javascript:melon.link.goAlbumDetail('333');">두 번째 앨범</a>
      <a href="javascript:melon.link.goArtistDetail('444');">가수B</a>
    </div>
  </td>
</tr>
</tbody>
</table>
</div>
"""

SAMPLE_LIKE_RESPONSE = {
    "contsLike": [
        {"CONTSID": 12345, "SUMMCNT": 5000},
        {"CONTSID": 67890, "SUMMCNT": 3000},
    ]
}


@responses.activate
def test_get_songs():
    responses.add(
        responses.GET,
        "http://www.melon.com/chart/index.htm",
        body=SAMPLE_HTML,
        status=200,
    )

    songs = get_songs()

    assert len(songs) == 2
    assert songs[0] == {
        "song_no": "12345",
        "title": "첫 번째 노래",
        "album": "첫 번째 앨범",
        "artist": "가수A",
    }
    assert songs[1]["song_no"] == "67890"


@responses.activate
def test_get_songs_empty():
    empty_html = '<div class="d_song_list"><table><tbody></tbody></table></div>'
    responses.add(
        responses.GET,
        "http://www.melon.com/chart/index.htm",
        body=empty_html,
        status=200,
    )

    songs = get_songs()

    assert songs == []


@responses.activate
def test_get_songs_skips_incomplete_row():
    html = """
    <div class="d_song_list">
    <table>
    <tbody>
    <tr data-song-no="11111">
      <td>
        <div class="wrap_song_info">
          <a href="javascript:melon.play.playSong('11111');">노래</a>
        </div>
      </td>
    </tr>
    </tbody>
    </table>
    </div>
    """
    responses.add(
        responses.GET,
        "http://www.melon.com/chart/index.htm",
        body=html,
        status=200,
    )

    songs = get_songs()

    assert songs == []


@responses.activate
def test_get_songs_http_error():
    responses.add(
        responses.GET,
        "http://www.melon.com/chart/index.htm",
        status=500,
    )

    with pytest.raises(HTTPError):
        get_songs()


@responses.activate
def test_get_like_count():
    responses.add(
        responses.GET,
        "https://www.melon.com/commonlike/getSongLike.json",
        json=SAMPLE_LIKE_RESPONSE,
        status=200,
    )

    result = get_like_count(12345)

    assert result == {"12345": 5000, "67890": 3000}


@responses.activate
def test_get_like_count_with_list():
    responses.add(
        responses.GET,
        "https://www.melon.com/commonlike/getSongLike.json",
        json=SAMPLE_LIKE_RESPONSE,
        status=200,
    )

    result = get_like_count([12345, 67890])

    assert result == {"12345": 5000, "67890": 3000}
    assert "contsIds=12345%2C67890" in responses.calls[0].request.url


@responses.activate
def test_get_like_count_http_error():
    responses.add(
        responses.GET,
        "https://www.melon.com/commonlike/getSongLike.json",
        status=403,
    )

    with pytest.raises(HTTPError):
        get_like_count(12345)


@pytest.mark.integration
def test_live_get_songs():
    songs = get_songs()
    assert isinstance(songs, list)
    assert len(songs) > 0

    first_song = songs[0]
    assert "song_no" in first_song
    assert "title" in first_song
    assert "album" in first_song
    assert "artist" in first_song
    assert first_song["song_no"].isdigit()
    assert len(first_song["title"].strip()) > 0
    assert len(first_song["album"].strip()) > 0
    assert len(first_song["artist"].strip()) > 0

