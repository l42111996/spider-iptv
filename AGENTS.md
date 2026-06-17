# Repository Guidelines

## Project Structure & Module Organization

This repository is a Python 3 IPTV data processing project backed by MySQL.
Top-level scripts are the main source code:

- `main.py` runs the full pipeline in order: `startiptv.py`, `hotels.py`, `multicast.py`, then `iptvdata.py`.
- `tools.py` contains shared download, conversion, request, and utility helpers.
- `data/iptv_data.sql` initializes the MySQL schema.
- `source/download/`, `source/hotels/`, and `source/multicast/` store downloaded or curated `.txt` and `.m3u` channel sources.

Generated output is documented in `README.md` as `source/iptv.txt`. Treat large source lists as data assets, not application code.

## Build, Test, and Development Commands

- `python3 main.py` runs the complete IPTV processing workflow.
- `python3 startiptv.py` downloads seed sources and clears channel history.
- `python3 hotels.py`, `python3 multicast.py`, and `python3 iptvdata.py` run individual pipeline stages.
- `mysql -u <user> -p iptv < data/iptv_data.sql` initializes a local database.
- `pip3 install bs4 m3u8 requests mysql-connector-python` installs the known Python dependencies.

The project also requires FFmpeg for media probing or stream-related work. On Ubuntu/Debian, install it with `sudo apt install ffmpeg`.

## Coding Style & Naming Conventions

Use Python 3 with 4-space indentation. Keep script names lowercase and descriptive, matching the existing pattern (`hotels.py`, `multicast.py`). Prefer small helper functions in `tools.py` when behavior is reused across scripts. Existing comments and log output are mostly Chinese; keep new user-facing messages consistent with nearby code.

Avoid hardcoding new secrets. Existing database connection settings and API tokens should be moved to local configuration before production use.

## Testing Guidelines

There is currently no automated test suite. Before submitting changes, run the smallest affected script and then `python3 main.py` when pipeline behavior changes. For data-only updates, verify that `.txt` and `.m3u` files keep the existing `channel,url` or M3U formatting.

If adding tests, use `pytest`, place tests under `tests/`, and name files `test_<module>.py`.

## Commit & Pull Request Guidelines

Git history uses short descriptive messages such as `Update README.md`, `download files`, and `multicast files`. Keep commits focused and concise.

Pull requests should describe the affected pipeline stage, list required configuration or database changes, and note whether generated source files changed. Include sample commands run and any relevant output file paths.
