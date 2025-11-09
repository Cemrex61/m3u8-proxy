# m3u8-proxy

Minimal Flask-based proxy to fetch and forward `.m3u8` playlists and segments.

## Usage

1. Deploy to Render as a **Web Service** (Python).
2. Ensure `requirements.txt` and `Procfile` are in the repo.
3. Start command: `gunicorn main:app` (Procfile included).
4. Example request:
   ```
   https://<your-render-url>/proxy?url=https%3A%2F%2Fornek.com%2Fplaylist.m3u8
   ```

## Notes
- This proxy forwards requests and responses; do not use for illegal/unauthorized content.
- Consider adding domain allowlist, rate-limiting, and caching for production.
