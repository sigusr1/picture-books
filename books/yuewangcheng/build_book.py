import base64
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "book.source.html"
WEB_OUTPUT = ROOT / "index.html"
OFFLINE_OUTPUT = ROOT / "offline.html"
FRAGMENT_OUTPUT = ROOT / "book.fragment.html"
COVER_OUTPUT = ROOT / "cover.jpg"
OPTIMIZED = ROOT / "assets" / "optimized"


def document(body):
    return (
        '<!doctype html>\n<html lang="zh-CN">\n<head>\n'
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        '<meta name="theme-color" content="#e9e4d9">\n'
        '<meta name="description" content="根据同名作文创作的杭州湘湖越王城山秋日绘本。">\n'
        '<title>美丽的越王城 · 湘湖秋日绘本</title>\n'
        '</head>\n<body>\n' + body + '\n</body>\n</html>\n'
    )


def main():
    subprocess.run([sys.executable, str(ROOT / "verify_text.py")], check=True)
    OPTIMIZED.mkdir(parents=True, exist_ok=True)
    web_html = SOURCE.read_text()
    embedded_html = web_html
    names = sorted(set(re.findall(r'src="assets/([^"]+\.png)"', web_html)))
    if len(names) != 6:
        raise RuntimeError(f"Expected six illustrations, found: {names}")

    for name in names:
        source = ROOT / "assets" / name
        if not source.exists():
            raise FileNotFoundError(source)
        target = OPTIMIZED / f"{Path(name).stem}.jpg"
        subprocess.run([
            "sips", "-s", "format", "jpeg", "-s", "formatOptions", "88",
            str(source), "--out", str(target),
        ], check=True, capture_output=True)
        web_html = web_html.replace(
            f'src="assets/{name}"', f'src="assets/optimized/{target.name}"'
        )
        encoded = base64.b64encode(target.read_bytes()).decode("ascii")
        embedded_html = embedded_html.replace(
            f'src="assets/{name}"', f'src="data:image/jpeg;base64,{encoded}"'
        )

    web_html = re.sub(r'(<img\b[^>]*?)\bsrc="', r'\1data-src="', web_html)
    COVER_OUTPUT.write_bytes((OPTIMIZED / "01-cover.jpg").read_bytes())
    unresolved = re.findall(r'(?:src|href)="(?!data:|#)([^"]+)"', embedded_html)
    if unresolved:
        raise RuntimeError(f"Unresolved external assets: {unresolved}")
    WEB_OUTPUT.write_text(document(web_html))
    OFFLINE_OUTPUT.write_text(document(embedded_html))
    FRAGMENT_OUTPUT.write_text(embedded_html)
    print(
        f"Built web {WEB_OUTPUT.stat().st_size} bytes, "
        f"offline {OFFLINE_OUTPUT.stat().st_size} bytes, and cover.jpg."
    )


if __name__ == "__main__":
    main()
