# Deployment Guide

This project can run as a two-service Docker Compose stack: a MySQL database and a Python application container. The application container stays alive after startup so a host scheduler can execute the crawl script on demand.

## Files and Layers

- `Dockerfile` has two layers:
  - `base`: installs system dependencies (`ffmpeg`, MySQL client) and Python packages from `requirements.txt`.
  - `app`: copies the repository code and exposes `docker-run.sh`.
- `docker-compose.yml` starts:
  - `mysql`: initializes the `iptv` database from `data/iptv_data.sql`.
  - `app`: runs the crawler code and mounts generated playlists to `/output`.
- `docker-run.sh` runs `python3 main.py`, then exports `source/iptv.txt` and `source/iptv.m3u` to `/output`.

## Required Configuration

Create a local `.env` file from the example:

```sh
cp .env.example .env
```

Set the Quake API token in `.env`:

```sh
QUAKE_API_TOKEN=your-quake-token
```

Optional tuning values:

```sh
IPTV_HOTEL_SCAN_WORKERS=32
IPTV_UDPXY_STATUS_WORKERS=20
```

Do not commit `.env`; it contains credentials.

## Output Directory

The compose file currently maps generated files to:

```text
/Users/king/Documents/iptv
```

After each successful run, expect:

- `/Users/king/Documents/iptv/iptv.txt`
- `/Users/king/Documents/iptv/iptv.m3u`

Change the `app.volumes` entry in `docker-compose.yml` if another host directory is needed.

## Build and Start

Build the image and start both services:

```sh
docker compose up -d --build
```

Check service status:

```sh
docker compose ps
```

The app container intentionally runs `tail -f /dev/null`; crawling starts only when `docker-run.sh` is executed.

## Run Once

Execute a full crawl and export generated playlists:

```sh
docker compose exec app /app/docker-run.sh
```

The script uses a lock directory at `/tmp/spider-iptv.lock`, so overlapping runs exit early.

## Suggested Scheduler

Use a host cron job or launchd timer to trigger the container script. Example cron entry:

```cron
0 3 * * * cd /Users/king/Documents/githubWorkspace/spider-iptv && docker compose exec -T app /app/docker-run.sh >> /Users/king/Documents/iptv/run.log 2>&1
```

This runs daily at 03:00 and writes logs beside the exported playlists.

## Troubleshooting

- If Quake is not configured, hotel scans still run, but multicast proxy discovery is skipped.
- If generated playlists contain only headers, the database may have valid channels that fail the export filter, such as low-resolution streams below `1280` width.
- Use `docker compose logs app` and `docker compose logs mysql` for container logs.
- Resetting the database requires removing the `iptv-mysql-data` Docker volume; this deletes stored crawl data.
