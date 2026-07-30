# followback

a tool to help you see who does not follow back on Instagram

## setup

```bash
python -m pip install uv
uv sync
```

## usage

The script requires an authenticated Instagram `sessionid` cookie.

```bash
uv run python followback.py <instagram_username> --sessionid <sessionid>
```

or with an environment variable:

```bash
INSTAGRAM_SESSIONID=<sessionid> uv run python followback.py <instagram_username>
```
