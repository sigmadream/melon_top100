## MelonTop100

한국 음악 사이트(멜론, 벅스)의 차트 정보를 쉽게 가져올 수 있는 Python 패키지입니다.

get_songs() 함수를 사용하면 각 사이트의 인기 차트 곡 목록을 리스트 형태로 조회할 수 있으며, 각 항목은 곡명, 아티스트, 앨범 등의 정보를 담은 딕셔너리로 제공됩니다.

이 패키지는 Python 3.9 이상 버전을 지원합니다.

## Setup(Dev)

개발자 환경 설정 및 테스트 실행 방법입니다.

```bash
$ uv sync
$ uv run pytest
$ uv run pytest --run-integration
$ uv run ruff check .
```

실제 음악 사이트에 직접 접근하여 크롤링 파싱 정상 작동 여부를 검증하려면 --run-integration 옵션을 붙여 통합 테스트를 실행해 주시기 바랍니다.

## Use

```python
$ pip install melon-top100
$ python

from melon_top100 import melon, bugs

# 멜론 Top 100
>>> melon.get_songs()
[{'song_no': '34754292', 'title': 'TOMBOY', 'album': 'I NEVER DIE', 'artist': '(여자)아이들'}, ...]

>>> melon.get_like_count(34754292)
{'34754292': 137492}

# 벅스 실시간 차트
>>> bugs.get_songs()
[{'track_id': '130013303', 'title': 'Adrenaline', 'artist': 'ATEEZ', 'album': 'GOLDEN HOUR : Part.4'}, ...]
```

## Ruff

이 프로젝트는 린터와 포매터로 Ruff(https://docs.astral.sh/ruff/)를 사용합니다. Ruff는 Rust로 작성된 Python 린터/포매터로, 기존 도구(flake8, isort, black 등)를 대체하면서도 압도적으로 빠른 속도를 제공합니다.

타입 힌트에 대해서는 개인적으로 선호하는 편은 아니지만, Ruff가 타입 힌트를 기반으로 더 정밀한 분석과 자동 수정을 제공하는 방향으로 발전하고 있어 그 가능성에 대한 기대감으로 적용했습니다.
