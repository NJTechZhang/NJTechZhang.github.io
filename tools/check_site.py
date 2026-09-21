"""站点自检：内部链接有效性、导读页结构完整性、主页论文条目一致性。

用法：
    python tools/check_site.py
"""
import os
import re
from urllib.parse import unquote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP = re.compile(r"\\\.git\\|\\\.tmp_extract\\|\\论文原文\\")
REQUIRED = ["摘要", "研究背景与动机", "结论与意义", "一句话总结", "引用格式"]


def html_files():
    for dirpath, _dirnames, filenames in os.walk(ROOT):
        if SKIP.search(dirpath + "\\"):
            continue
        for fn in filenames:
            if fn.endswith(".html"):
                yield os.path.join(dirpath, fn)


def check_links():
    checked = bad = 0
    for page in html_files():
        html = open(page, encoding="utf-8").read()
        for m in re.finditer(r'(?:href|src)="([^"]+)"', html):
            url = m.group(1)
            if url.startswith(("http://", "https://", "mailto:", "data:", "#", "javascript:")):
                continue
            part = url.split("#")[0].split("?")[0]
            if not part:
                continue
            checked += 1
            target = os.path.normpath(os.path.join(os.path.dirname(page), unquote(part)))
            if not os.path.exists(target):
                bad += 1
                print(f"  [失效链接] {os.path.relpath(page, ROOT)} -> {url}")
    print(f"内部链接：检查 {checked} 个，失效 {bad} 个")
    return bad


def check_pages():
    papers = os.path.join(ROOT, "papers")
    problems = 0
    files = [f for f in sorted(os.listdir(papers)) if f.endswith(".html") and f != "index.html"]
    for fn in files:
        raw = open(os.path.join(papers, fn), "rb").read()
        txt = raw.decode("utf-8")
        issues = []
        if raw.startswith(b"\xef\xbb\xbf"):
            issues.append("含 BOM")
        if re.search(r"\{\{.*?\}\}", txt):
            issues.append("残留占位符")
        if not txt.rstrip().endswith("</html>"):
            issues.append("文件未正常结尾")
        for key in REQUIRED:
            if key not in txt:
                issues.append(f"缺章节「{key}」")
        for tag in ["section", "article", "div", "ul", "li", "p"]:
            o, c = len(re.findall(rf"<{tag}[\s>]", txt)), len(re.findall(rf"</{tag}>", txt))
            if o != c:
                issues.append(f"<{tag}> 不平衡 {o}/{c}")
        if "../assets/css/paper.css" not in txt:
            issues.append("缺样式引用")
        if issues:
            problems += 1
            print(f"  [{fn}] " + "; ".join(issues))
    print(f"导读页：检查 {len(files)} 个，问题 {problems} 个")
    return problems


def check_home():
    home = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
    items = re.findall(r'<div class="pub-title"><a href="(papers/[^"]+)">', home)
    print(f"主页论文条目：{len(items)} 条")
    miss = [s for s in items if not os.path.exists(os.path.join(ROOT, s))]
    pages = {f"papers/{f}" for f in os.listdir(os.path.join(ROOT, "papers"))
             if f.endswith(".html") and f != "index.html"}
    orphan = sorted(pages - set(items))
    print(f"  缺失页面：{len(miss)} 个" + (f" -> {miss}" if miss else ""))
    print(f"  未登记页面：{len(orphan)} 个" + (f" -> {orphan}" if orphan else ""))
    return len(miss) + len(orphan)


if __name__ == "__main__":
    total = check_links() + check_pages() + check_home()
    print("\n结论：" + ("全部通过 ✅" if total == 0 else f"发现 {total} 处问题 ❌"))
