"""从 论文原文/ 目录提取 PDF 文本并生成内容摘要素材，供撰写论文中文导读使用。

用法：
    python tools/build_digest.py

输出：
    .tmp_extract/full/<论文名>.txt     —— 每篇 PDF 的全文
    .tmp_extract/digest/<论文名>.txt   —— 摘要 + 章节结构 + 关键数值句 + 结论片段

依赖：PyMuPDF（pip install pymupdf）
"""
import os
import re
import json

import pymupdf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "论文原文")
OUT_FULL = os.path.join(ROOT, ".tmp_extract", "full")
OUT_DIGEST = os.path.join(ROOT, ".tmp_extract", "digest")

HEAD_RES = [
    re.compile(r"^\d{1,2}(?:\.\d{1,2}){0,2}\.?\s+\S[^\n]{2,90}$", re.MULTILINE),
    re.compile(r"^(?:ABSTRACT|Abstract|Introduction|Related Work|Method\w*|Proposed \S[^\n]{0,70}|"
               r"Experiment\w*|Result\w*|Discussion|Conclusion\w*|REFERENCES)\s*$", re.MULTILINE),
    re.compile(r"^(?:摘要|关键词|引言|研究背景|相关工作|研究方法|实验与分析|实验结果|讨论|结论|结束语|参考文献|展望)\s*[:：]?\s*$",
               re.MULTILINE),
]
NUM_PAT = re.compile(
    r"[^。\n]{0,160}?(?:\d{1,3}\.\d{1,2}\s*%|mIoU|IoU|Kappa|OA\b|accuracy|outperform\w*|"
    r"improv\w+|精度|提高了?)[^。\n]{0,180}[。\n]",
    re.IGNORECASE,
)


def clean(text):
    text = re.sub(r"[ \t]+", " ", text)
    return re.sub(r"\n{2,}", "\n", text)


def main():
    if not os.path.isdir(SRC):
        raise SystemExit(f"未找到论文原文目录：{SRC}")
    os.makedirs(OUT_FULL, exist_ok=True)
    os.makedirs(OUT_DIGEST, exist_ok=True)

    index = []
    for name in sorted(os.listdir(SRC)):
        if not name.lower().endswith(".pdf"):
            continue
        doc = pymupdf.open(os.path.join(SRC, name))
        pages = [doc[i].get_text() for i in range(doc.page_count)]
        doc.close()

        flat = clean("\n".join(pages))
        stem = re.sub(r"[^\w\u4e00-\u9fff]+", "_", os.path.splitext(name)[0])[:75]

        with open(os.path.join(OUT_FULL, stem + ".txt"), "w", encoding="utf-8") as fh:
            fh.write(flat)

        heads = []
        for rx in HEAD_RES:
            heads.extend(h.strip() for h in rx.findall(flat) if h.strip())
        heads = list(dict.fromkeys(heads))[:40]
        nums = list(dict.fromkeys(m.group(0).strip() for m in NUM_PAT.finditer(flat)))[:20]

        digest = "\n".join([
            f"# SOURCE FILE: {name}",
            "\n## 首页文本（标题/作者/摘要）\n" + flat[:3200],
            "\n## 章节结构\n" + "\n".join("- " + h for h in heads),
            "\n## 关键数值/结论句\n" + "\n".join("- " + n for n in nums),
            "\n## 文末片段（结论区）\n" + flat[-5000:],
        ])
        with open(os.path.join(OUT_DIGEST, stem + ".txt"), "w", encoding="utf-8") as fh:
            fh.write(digest)

        index.append({"file": name, "stem": stem, "pages": len(pages), "chars": len(flat)})
        print(f"{len(pages):>3}p {len(flat):>7}ch  {stem}")

    with open(os.path.join(ROOT, ".tmp_extract", "_index.json"), "w", encoding="utf-8") as fh:
        json.dump(index, fh, ensure_ascii=False, indent=1)
    print(f"\n共处理 {len(index)} 篇，输出到 {os.path.join(ROOT, '.tmp_extract')}")


if __name__ == "__main__":
    main()
