from flask import Flask, request, Response, abort
import requests
from urllib.parse import urlparse, unquote

app = Flask(__name__)

def is_allowed_url(url: str) -> bool:
    try:
        p = urlparse(url)
        return p.scheme in ("http", "https") and p.netloc != ""
    except:
        return False

@app.route("/")
def index():
    return "m3u8-proxy çalışıyor. Kullanım: /proxy?url=<ENCODED_URL>"

@app.route("/proxy")
def proxy():
    url = request.args.get("url", "")
    if not url:
        return abort(400, "url parametresi eksik. Örnek: /proxy?url=https://example.com/playlist.m3u8")

    url = unquote(url)

    if not is_allowed_url(url):
        return abort(400, "Geçersiz URL.")

    try:
        r = requests.get(url, stream=True, timeout=20, headers={"User-Agent": "m3u8-proxy/1.0"})
    except requests.RequestException as e:
        return abort(502, f"Kaynağa erişilemedi: {e}")

    def generate():
        try:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    yield chunk
        finally:
            r.close()

    content_type = r.headers.get("Content-Type", "application/vnd.apple.mpegurl")
    headers = {
        "Content-Type": content_type,
        "Access-Control-Allow-Origin": "*",
        "Cache-Control": "no-cache",
    }

    return Response(generate(), headers=headers, status=r.status_code)

if __name__ == "__main__":
    # Lokal test için
    app.run(host="0.0.0.0", port=8080)
