# 绘本书架

一个可持续添加新书的静态绘本网站。仓库使用 GitHub Pages 托管，每本书有独立阅读链接，也可下载 PDF。

- 书架首页：https://sigusr1.github.io/picture-books/
- 《美丽的越王城》：https://sigusr1.github.io/picture-books/books/yuewangcheng/

## 当前书目

| 绘本 | 页数 | 阅读 | PDF |
|---|---:|---|---|
| 美丽的越王城 | 8 | `books/yuewangcheng/` | `books/yuewangcheng/美丽的越王城.pdf` |

## 添加下一本绘本

1. 新建 `books/<英文短名>/`，放入自包含的 `index.html` 和书架封面 `cover.jpg`；可选放入 PDF。
2. 在 `catalog.json` 的 `books` 数组增加书名、短名、简介、页数、封面和 PDF 文件名。
3. 在仓库根目录运行 `python3 build_site.py`，脚本会验证书目文件并重新生成书架首页。
4. 检查书架和新书页面后，再提交、推送更新。

每本书的插画和排版源文件也可保存在自己的目录中，互不影响。`**/assets/optimized/` 是构建缓存，不入库；书架使用的 `cover.jpg` 需要入库。

## 构建

```bash
python3 build_site.py
```

《美丽的越王城》的单书构建、插画模型和实景参考见 `books/yuewangcheng/README.md`。
