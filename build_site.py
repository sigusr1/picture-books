import html
import json
from pathlib import Path
from string import Template
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent


def book_card(book):
    slug = quote(book["slug"], safe="")
    directory = ROOT / "books" / book["slug"]
    cover = book.get("cover", "cover.jpg")
    required = [directory / "index.html", directory / cover]
    pdf = book.get("pdf")
    if pdf:
        required.append(directory / pdf)
    missing = [str(path.relative_to(ROOT)) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(f"{book['slug']}: missing {', '.join(missing)}")
    pdf_link = (
        f'<a class="pdf-link" href="books/{slug}/{quote(pdf)}">下载 PDF</a>'
        if pdf else ""
    )
    return f"""
      <article class="book-card">
        <a class="cover-link" href="books/{slug}/" aria-label="阅读《{html.escape(book['title'])}》">
          <img src="books/{slug}/{quote(cover)}" alt="《{html.escape(book['title'])}》封面" loading="lazy">
          <span class="read-badge">开始阅读 →</span>
        </a>
        <div class="book-info">
          <p class="subtitle">{html.escape(book.get('subtitle', ''))}</p>
          <h2><a href="books/{slug}/">{html.escape(book['title'])}</a></h2>
          <p class="description">{html.escape(book.get('description', ''))}</p>
          <div class="meta"><span>{book.get('pages', 0)} 页</span><span>{html.escape(book.get('date', ''))}</span>{pdf_link}</div>
        </div>
      </article>"""


def main():
    catalog = json.loads((ROOT / "catalog.json").read_text())
    books = catalog["books"]
    cards = "\n".join(book_card(book) for book in books)
    template = Template("""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#f3eee3">
  <meta name="description" content="可以在线阅读、打印和下载的绘本书架。">
  <title>$title</title>
  <style>
    * { box-sizing: border-box; }
    body { margin: 0; min-height: 100vh; color: #263d38; background: radial-gradient(circle at 8% 0%, #fffaf0, transparent 35%), #eee8dc; font-family: "Songti SC", "STSong", serif; }
    header, main, footer { width: min(1180px, calc(100% - 48px)); margin: 0 auto; }
    header { padding: clamp(46px, 8vw, 90px) 0 36px; }
    .kicker { color: #a94d35; font: 600 12px/1.5 -apple-system, BlinkMacSystemFont, "PingFang SC", sans-serif; letter-spacing: .22em; }
    h1 { margin: 12px 0 14px; font-size: clamp(42px, 7vw, 78px); line-height: 1.1; letter-spacing: .08em; }
    .intro { margin: 0; color: #68766d; font-size: clamp(14px, 1.6vw, 18px); line-height: 1.9; }
    .shelf-line { height: 1px; margin-top: 34px; background: linear-gradient(90deg, #a94d35 0 90px, rgba(38,61,56,.15) 90px); }
    .book-count { margin: 0 0 22px; color: #778078; font: 12px/1.5 -apple-system, BlinkMacSystemFont, "PingFang SC", sans-serif; letter-spacing: .12em; }
    .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(min(100%, 320px), 1fr)); gap: 28px; }
    .book-card { overflow: hidden; border: 1px solid rgba(45,61,53,.1); border-radius: 14px; background: rgba(255,251,242,.82); box-shadow: 0 12px 35px rgba(48,49,38,.08); }
    .cover-link { position: relative; display: block; aspect-ratio: 16/9; overflow: hidden; background: #d9d6c8; }
    .cover-link img { width: 100%; height: 100%; object-fit: cover; transition: transform .45s ease; }
    .cover-link:hover img { transform: scale(1.025); }
    .read-badge { position: absolute; right: 16px; bottom: 16px; padding: 9px 14px; border-radius: 30px; color: #fff9eb; background: rgba(32,55,48,.9); font: 12px/1.2 -apple-system, BlinkMacSystemFont, "PingFang SC", sans-serif; }
    .book-info { padding: 24px 26px 22px; }
    .subtitle { margin: 0 0 8px; color: #a94d35; font: 600 11px/1.5 -apple-system, BlinkMacSystemFont, "PingFang SC", sans-serif; letter-spacing: .12em; }
    h2 { margin: 0 0 12px; font-size: 28px; line-height: 1.3; }
    h2 a { color: inherit; text-decoration: none; }
    .description { min-height: 4.8em; margin: 0 0 20px; color: #5e6b64; font-size: 14px; line-height: 1.8; }
    .meta { display: flex; align-items: center; gap: 14px; padding-top: 15px; border-top: 1px solid rgba(45,61,53,.12); color: #7b827b; font: 11px/1.4 -apple-system, BlinkMacSystemFont, "PingFang SC", sans-serif; }
    .meta .pdf-link { margin-left: auto; color: #a94d35; text-decoration: none; }
    footer { padding: 42px 0 48px; color: #8a8e84; text-align: center; font-size: 12px; letter-spacing: .12em; }
    @media (max-width: 600px) { header, main, footer { width: calc(100% - 28px); } header { padding-top: 38px; } .grid { gap: 20px; } .description { min-height: 0; } }
    @media (prefers-reduced-motion: reduce) { .cover-link img { transition: none; } }
  </style>
</head>
<body>
  <header>
    <p class="kicker">PICTURE BOOKS</p>
    <h1>$title</h1>
    <p class="intro">把值得记住的风景与故事，做成可以在线阅读、打印和分享的绘本。</p>
    <div class="shelf-line"></div>
  </header>
  <main>
    <p class="book-count">共 $count 本</p>
    <div class="grid">$cards
    </div>
  </main>
  <footer>更多绘本，正在路上。</footer>
</body>
</html>
""")
    output = template.substitute(
        title=html.escape(catalog.get("title", "绘本书架")),
        count=len(books),
        cards=cards,
    )
    (ROOT / "index.html").write_text(output)
    print(f"Built bookshelf with {len(books)} book(s): {ROOT / 'index.html'}")


if __name__ == "__main__":
    main()
