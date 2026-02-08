import pytest
import responses
from requests.exceptions import HTTPError

from melon_top100.bugs import get_songs

SAMPLE_HTML = """
<table class="list trackList byChart">
<tbody>
<tr trackid="130013303" artistid="20067194" albumid="39572764" mvid="637549" multiartist="N" rowtype="track">
  <th scope="row">
    <p class="title">
      <a href="javascript:;" title="Adrenaline">Adrenaline</a>
    </p>
  </th>
  <td class="left">
    <p class="artist">
      <a href="https://music.bugs.co.kr/artist/20067194" title="ATEEZ">ATEEZ</a>
    </p>
  </td>
  <td class="left">
    <a class="album" href="https://music.bugs.co.kr/album/39572764" title="GOLDEN HOUR : Part.4">GOLDEN HOUR : Part.4</a>
  </td>
</tr>
<tr trackid="130013304" artistid="20067195" albumid="39572765" mvid="637550" multiartist="N" rowtype="track">
  <th scope="row">
    <p class="title">
      <a href="javascript:;" title="Second Song">Second Song</a>
    </p>
  </th>
  <td class="left">
    <p class="artist">
      <a href="https://music.bugs.co.kr/artist/20067195" title="Artist B">Artist B</a>
    </p>
  </td>
  <td class="left">
    <a class="album" href="https://music.bugs.co.kr/album/39572765" title="Album B">Album B</a>
  </td>
</tr>
</tbody>
</table>
"""


@responses.activate
def test_get_songs():
    responses.add(
        responses.GET,
        "https://music.bugs.co.kr/chart/track/realtime/total",
        body=SAMPLE_HTML,
        status=200,
    )

    songs = get_songs()

    assert len(songs) == 2
    assert songs[0] == {
        "track_id": "130013303",
        "title": "Adrenaline",
        "artist": "ATEEZ",
        "album": "GOLDEN HOUR : Part.4",
    }
    assert songs[1]["track_id"] == "130013304"


@responses.activate
def test_get_songs_empty():
    empty_html = '<table class="list trackList byChart"><tbody></tbody></table>'
    responses.add(
        responses.GET,
        "https://music.bugs.co.kr/chart/track/realtime/total",
        body=empty_html,
        status=200,
    )

    songs = get_songs()

    assert songs == []


@responses.activate
def test_get_songs_skips_incomplete_row():
    html = """
    <table class="list trackList byChart">
    <tbody>
    <tr trackid="99999" artistid="1" albumid="1" rowtype="track">
      <th scope="row">
        <p class="title">
          <a href="javascript:;" title="Incomplete">Incomplete</a>
        </p>
      </th>
    </tr>
    </tbody>
    </table>
    """
    responses.add(
        responses.GET,
        "https://music.bugs.co.kr/chart/track/realtime/total",
        body=html,
        status=200,
    )

    songs = get_songs()

    assert songs == []


@responses.activate
def test_get_songs_http_error():
    responses.add(
        responses.GET,
        "https://music.bugs.co.kr/chart/track/realtime/total",
        status=500,
    )

    with pytest.raises(HTTPError):
        get_songs()
