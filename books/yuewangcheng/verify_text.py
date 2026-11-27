import html
import re
from pathlib import Path

SOURCE = Path(__file__).resolve().parent / "book.source.html"

EXPECTED = {
    1: "美丽的越王城",
    2: "看到这个题目，你们肯定觉得越王城就一座普通的古代城池。可是，你们想错了，越王城是一座建在城山上的城池！",
    3: "光是山脚下，就能让你惊讶不已。距今约二千五百年的建筑，竟然还完好的展现在那里！",
    4: "钟楼上的大铜钟，虽然已经生锈了，但是还能看清上面的文字，真是太神奇了！",
    5: "秋天的树叶与春天、夏天的样子全然不同。爬到半山腰，迎接我们的是美丽的枫叶，叶子们好像有的向朝阳借了一点橙，有的向夕阳借了一点红，还有的向大地借了一点棕。绚丽众多，堪称层林尽染。",
    6: "在山顶朝下看更为美丽。登上山顶，站在观景台上往下看，大树仿佛变成了西蓝花，房子就像一个个积木方块，人和汽车呢？更不用说，都变得像蚂蚁一样小。",
    7: "不禁让我想起了杜甫的诗句：会当凌绝顶，一览众山小。",
    8: "越王城山风景优美，古迹众多，真让人流连忘返。",
}


def normalize(value):
    return re.sub(r"\s+", "", html.unescape(value))


def main():
    source = SOURCE.read_text()
    actual = {}
    for page in EXPECTED:
        match = re.search(
            rf'<section\b[^>]*data-page="{page}"[^>]*>(.*?)</section>',
            source,
            re.S,
        )
        if not match:
            raise AssertionError(f"Missing page {page}")
        body = re.sub(
            r'<span\b[^>]*class="[^"]*page-number[^"]*"[^>]*>.*?</span>',
            "",
            match.group(1),
            flags=re.S,
        )
        actual[page] = normalize(re.sub(r"<[^>]+>", "", body))
        if actual[page] != normalize(EXPECTED[page]):
            raise AssertionError(
                f"Page {page} differs from the original essay:\n"
                f"expected: {normalize(EXPECTED[page])}\n"
                f"actual:   {actual[page]}"
            )
        print(f"page {page}: original text verified")


if __name__ == "__main__":
    main()
