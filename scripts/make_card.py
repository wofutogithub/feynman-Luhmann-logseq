#!/usr/bin/env python3
"""从 cards.json 批量生成 Logseq 兼容卡片 markdown。

用法:
    python3 make_card.py cards.json [输出目录]

cards.json 结构（数组）:
[
  {
    "type": "quote|concept|method|question",
    "book": "预测之书",
    "title": "反脆弱",            # concept 卡用；其余卡取 seq
    "seq": "01",                  # quote/method/question 卡序号，缺省按顺序补零
    "source": "第4章 p.87",
    "tags": ["思维模型", "塔勒布"],
    "quote": "原文金句...",       # quote 卡
    "content": "要点行1\n要点行2", # concept/method/question 卡正文
    "links": ["概念-预测之书-系统韧性"]  # [[双链]]
  }
]

生成文件名: 类型-《书名》-序号.md 或 概念-《书名》-标题.md
"""
import json
import os
import re
import sys


def sanitize(text: str) -> str:
    """去掉文件名非法字符，保留《》中文书名号。"""
    text = re.sub(r'[\\/:*?"<>|]', '', text)
    return text.strip()


TYPE_LABELS = {'quote': '金句', 'concept': '概念', 'method': '方法', 'question': '疑问'}


def render_card(card: dict, index: int) -> tuple[str, str]:
    ctype = card.get('type', 'quote')
    label = TYPE_LABELS.get(ctype, ctype)
    book = card.get('book', '').strip()
    title = card.get('title', '').strip()
    seq = card.get('seq', f"{index:02d}")

    if ctype == 'concept':
        page_name = f"概念-《{book}》-{title}" if book else f"概念-{title}"
    else:
        page_name = f"{label}-《{book}》-{seq}" if book else f"{label}-{seq}"
    filename = sanitize(page_name) + '.md'

    lines = [f"# {page_name}", ""]
    lines.append(f"- card-type:: {ctype}")
    if book:
        lines.append(f"- book:: [[《{book}》]]")
    if card.get('source'):
        lines.append(f"- source:: {card['source']}")
    if card.get('tags'):
        tags = ' '.join('#' + str(t) for t in card['tags'])
        lines.append(f"- tags:: {tags}")
    lines.append("")

    if card.get('quote'):
        lines.append(f"> {card['quote']}")
    if card.get('content'):
        for ln in str(card['content']).split('\n'):
            lines.append(f"- {ln}")
    if card.get('links'):
        for ln in card['links']:
            lines.append(f"- [[{ln}]]")

    return filename, '\n'.join(lines) + '\n'


def main() -> int:
    if len(sys.argv) < 2:
        print("用法: python3 make_card.py cards.json [输出目录]")
        return 1
    with open(sys.argv[1], encoding='utf-8') as f:
        data = json.load(f)
    outdir = sys.argv[2] if len(sys.argv) > 2 else '03-卡片'
    os.makedirs(outdir, exist_ok=True)

    cards = data if isinstance(data, list) else data.get('cards', [])
    for i, card in enumerate(cards, 1):
        filename, content = render_card(card, i)
        path = os.path.join(outdir, filename)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ {path}")
    print(f"共生成 {len(cards)} 张卡片 → {outdir}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
