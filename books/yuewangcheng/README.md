# 美丽的越王城

根据 `~/Downloads/zuowen.jpg` 中的同名作文制作的 8 页横版绘本，地点为杭州湘湖越王城山。绘本中的作文文字严格逐字保留，只做分页和换行，不做润色、事实改写或增删。

## 阅读

在线阅读：https://blog.coderhuo.tech/picture-books/books/yuewangcheng/

也可打开本目录的 `offline.html` 离线阅读。点击左右按钮或使用键盘方向键翻页；手机端支持左右滑动。

## 打印 / 导出 PDF

点击页面右上角的打印机按钮。打印设置为 A4 横向、无边距，并开启“背景图形”；每一页对应绘本的一页。

## 文件

- `index.html`：轻量在线版，引用书内 JPEG 图片，避免一次下载整个内嵌文件。
- `offline.html`：自包含离线版，六幅插画均已内嵌。
- `美丽的越王城.pdf`：8 页 A4 横向打印版。
- `cover.jpg`：书架首页使用的封面。
- `book.source.html`：绘本排版源文件。
- `book.fragment.html`：内嵌插画的 body-only 版本，用于交互式预览。
- `assets/`：GPT-Image-2.6 Sunburst 生成的六幅原始插画。
- `assets/optimized/`：在线版引用、离线版内嵌的高质量 JPEG 图片。
- `manifest.json`：插画模型、生成结果与逐图实景参考链接。
- `verify_text.py`：逐页比对原作文，任何正文增删改都会使检查失败。
- `build_book.py`：先运行原文校验，再生成在线版、离线版、预览片段和书架封面。

## 实景参考

插画不是景区照片复刻，而是以实景校正建筑和地貌后进行水彩创作：城山怀古牌坊与城山广场、夯土城垣及马门、越王祠钟楼、城山古道、山顶俯瞰湘湖。

- https://hznews.hangzhou.com.cn/wghz/content/2023-06/29/content_8567307.htm
- https://tidenews.com.cn/news.html?id=3306979
- https://www.sohu.com/a/288705985_109593

重新构建：

```bash
cd /Users/huo/work/picture-books/books/yuewangcheng
python3 build_book.py
```
