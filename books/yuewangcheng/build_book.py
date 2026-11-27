import base64
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "book.source.html"
OUTPUT = ROOT / "index.html"
FRAGMENT_OUTPUT = ROOT / "book.fragment.html"
COVER_OUTPUT = ROOT / "cover.jpg"
OPTIMIZED = ROOT / "assets" / "optimized"


def main():
    OPTIMIZED.mkdir(parents=True, exist_ok=True)
    html = SOURCE.read_text()
    names = sorted(set(re.findall(r'src="assets/([^"]+\.png)"', html)))
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
        encoded = base64.b64encode(target.read_bytes()).decode("ascii")
        html = html.replace(f'src="assets/{name}"', f'src="data:image/jpeg;base64,{encoded}"')

    COVER_OUTPUT.write_bytes((OPTIMIZED / "01-cover.jpg").read_bytes())
    unresolved = re.findall(r'(?:src|href)="(?!data:|#)([^"]+)"', html)
    if unresolved:
        raise RuntimeError(f"Unresolved external assets: {unresolved}")
    FRAGMENT_OUTPUT.write_text(html)
    document = (
        '<!doctype html>\n<html lang="zh-CN">\n<head>\n'
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        '<meta name="theme-color" content="#e9e4d9">\n'
        '<meta name="description" content="根据同名作文创作的杭州湘湖越王城山秋日绘本。">\n'
        '<title>美丽的越王城 · 湘湖秋日绘本</title>\n'
        '</head>\n<body>\n' + html + '\n</body>\n</html>\n'
    )
    OUTPUT.write_text(document)
    print(f"Built {OUTPUT} and {FRAGMENT_OUTPUT} with six embedded illustrations.")


if __name__ == "__main__":
    main()
