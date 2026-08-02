#!/usr/bin/env python3
"""StudyBuddy 文档一致性检查。

本仓库没有代码，文档即 prompt——任意两份文件之间的矛盾都是一个真实的行为缺陷。
本脚本用于机械地捕获这类缺陷。

用法：
    python tools/check_docs.py

退出码：0 表示无问题，1 表示发现问题。
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# 扫描范围：技能本体 + 仓库级说明文档
TARGETS = ["skills", "AGENTS.md", "CLAUDE.md", "README.md"]

SUBJECTS = {"语文", "数学", "英语", "物理", "化学", "生物"}
SUBJECT_PLACEHOLDERS = {"[学科]"}

# 「这份资料来自哪个原始文件」统一用 source_path
CANONICAL_SOURCE_KEY = "source_path"
DEPRECATED_SOURCE_KEYS = {"image_path", "source_file"}

CN_NUMERALS = "一二三四五六七八九十"

# 同名平台只允许有一个 URL
PLATFORMS = {
    "国家中小学智慧教育平台": re.compile(r"国家中小学智慧教育平台"),
    "北京中小学智慧教育平台": re.compile(r"北京中小学智慧教育平台"),
}

RE_HEADING_NUM = re.compile(r"^#{2,3}\s*([" + CN_NUMERALS + r"]+)、")
RE_LINK = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")
RE_SUBJECT = re.compile(r"^\s*subject:\s*(.+?)\s*(?:#.*)?$")
RE_SOURCE_KEY = re.compile(r"^\s*(" + "|".join(sorted(DEPRECATED_SOURCE_KEYS)) + r"):")
RE_SCRIPT_REF = re.compile(r"[\w./\\-]+\.py\b")
RE_URL = re.compile(r"https?://[^\s)\]、，。`\"'>]+")
RE_LOG_PATH = re.compile(r"[\w/<>-]*YYYY-MM-DD-log\.md")
# 原始资料目录只有 raw/YYYY/MM/ 一种写法
RE_RAW_PATH = re.compile(r"\braw/(?!YYYY/MM/)[\w/<>-]*")

CANONICAL_LOG_PATH = "output/YYYY/MM/YYYY-MM-DD-log.md"
CANONICAL_RAW_PATH = "raw/YYYY/MM/"


def cn_to_int(s: str) -> int:
    """把 一/二/…/十/十一/二十 之类的中文数字转成整数。"""
    if s == "十":
        return 10
    if "十" in s:
        left, _, right = s.partition("十")
        tens = CN_NUMERALS.index(left) + 1 if left else 1
        ones = CN_NUMERALS.index(right) + 1 if right else 0
        return tens * 10 + ones
    return CN_NUMERALS.index(s) + 1


def iter_lines(text: str):
    """产出 (行号, 行内容, 是否在代码围栏内)。

    区分围栏内外很关键：章节编号只看围栏外的标题（围栏内的是模板正文），
    而 frontmatter 模板恰恰都在围栏内。
    """
    in_fence = False
    for i, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            yield i, line, True
            continue
        yield i, line, in_fence


def md_files() -> list[Path]:
    out: list[Path] = []
    for t in TARGETS:
        p = ROOT / t
        if p.is_file() and p.suffix == ".md":
            out.append(p)
        elif p.is_dir():
            out.extend(sorted(p.rglob("*.md")))
    return sorted(set(out))


class Findings:
    def __init__(self) -> None:
        self.items: list[tuple[str, Path, int, str]] = []

    def add(self, check: str, path: Path, line: int, msg: str) -> None:
        self.items.append((check, path, line, msg))

    def report(self) -> int:
        if not self.items:
            print("check_docs: OK — 未发现文档一致性问题。")
            return 0
        by_check: dict[str, list] = {}
        for check, path, line, msg in self.items:
            by_check.setdefault(check, []).append((path, line, msg))
        for check in sorted(by_check):
            print(f"\n## {check}  ({len(by_check[check])})")
            for path, line, msg in by_check[check]:
                rel = path.relative_to(ROOT).as_posix()
                print(f"  {rel}:{line}: {msg}")
        print(f"\ncheck_docs: 发现 {len(self.items)} 个问题。")
        return 1


def check_links(path: Path, lines, f: Findings) -> None:
    """1. 每个相对链接和被当作可执行文件引用的脚本都必须存在。

    围栏内的链接是模板占位符（如 `[章节标题1](<YYYY-MM-DD>-<slug>.md)`、`[视频标题](链接)`），
    不是真实链接，跳过；脚本引用则围栏内外都要查——粘贴的命令行正是它们出没的地方。
    """
    for num, line, in_fence in lines:
        for _text, target in ([] if in_fence else RE_LINK.findall(line)):
            target = target.strip()
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            rel = target.split("#", 1)[0].strip()
            if not rel:
                continue
            resolved = (path.parent / rel).resolve()
            # README 里的链接是相对仓库根写的
            if not resolved.exists():
                alt = (ROOT / rel).resolve()
                if alt.exists():
                    continue
                f.add("链接失效", path, num, f"链接目标不存在：{target}")

        for script in RE_SCRIPT_REF.findall(line):
            norm = script.replace("\\", "/").lstrip("./")
            if not (ROOT / norm).exists():
                f.add("脚本缺失", path, num, f"引用了不存在的脚本：{script}")


def check_section_numbering(path: Path, lines, f: Findings) -> None:
    """2. 围栏外的中文编号标题必须从「一」开始且连续递增。"""
    seen: list[tuple[int, int]] = []  # (数值, 行号)
    for num, line, in_fence in lines:
        if in_fence:
            continue
        m = RE_HEADING_NUM.match(line)
        if m:
            seen.append((cn_to_int(m.group(1)), num))
    if not seen:
        return
    expected = 1
    for value, num in seen:
        if value != expected:
            if value < expected:
                f.add("章节编号", path, num,
                      f"编号重复或回退：出现「{CN_NUMERALS[value - 1]}」，预期「{CN_NUMERALS[expected - 1]}」")
            else:
                f.add("章节编号", path, num,
                      f"编号跳号：出现「{CN_NUMERALS[value - 1]}」，预期「{CN_NUMERALS[expected - 1]}」")
            expected = value + 1
        else:
            expected += 1


def check_subject_enum(path: Path, lines, f: Findings) -> None:
    """3. subject: 只能取六个学科中文名（模板占位符除外）。"""
    for num, line, _ in lines:
        m = RE_SUBJECT.match(line)
        if not m:
            continue
        value = m.group(1).strip().strip("\"'")
        if value in SUBJECTS or value in SUBJECT_PLACEHOLDERS or not value:
            continue
        f.add("subject 取值", path, num,
              f"subject 取值「{value}」不在六科枚举内；非学科文档请改用 doc_type")


def check_source_keys(path: Path, lines, f: Findings) -> None:
    """4. 原始文件路径统一用 source_path。"""
    for num, line, _ in lines:
        m = RE_SOURCE_KEY.match(line)
        if m:
            f.add("frontmatter 键名", path, num,
                  f"「{m.group(1)}」应统一为「{CANONICAL_SOURCE_KEY}」")


def check_paths(path: Path, lines, f: Findings) -> None:
    """5. 日志路径与原始资料路径各只有一种写法。"""
    for num, line, _ in lines:
        for hit in RE_LOG_PATH.findall(line):
            if hit == "YYYY-MM-DD-log.md":
                continue  # 裸文件名（如目录树、示例）可接受
            if hit != CANONICAL_LOG_PATH:
                f.add("日志路径", path, num,
                      f"日志路径「{hit}」应为「{CANONICAL_LOG_PATH}」")

        for hit in RE_RAW_PATH.findall(line):
            if hit == "raw/":
                continue  # 目录树里单独出现的 raw/ 节点可接受
            # 示例路径用真实年月（如 raw/2026/07/photo.jpg）同样合法
            if re.fullmatch(r"raw/\d{4}/\d{2}/[\w.-]*", hit):
                continue
            f.add("原始资料路径", path, num,
                  f"原始资料路径「{hit}」应为「{CANONICAL_RAW_PATH}」形式")


def check_platform_urls(files: list[Path], f: Findings) -> None:
    """6. 同一个平台名不得对应多个不同 URL。"""
    urls: dict[str, dict[str, tuple[Path, int]]] = {n: {} for n in PLATFORMS}
    for path in files:
        text = path.read_text(encoding="utf-8")
        for num, line, _ in iter_lines(text):
            for name, pat in PLATFORMS.items():
                if not pat.search(line):
                    continue
                for url in RE_URL.findall(line):
                    host = re.sub(r"^https?://", "", url).split("/", 1)[0]
                    urls[name].setdefault(host, (path, num))
    for name, found in urls.items():
        if len(found) > 1:
            for host, (path, num) in sorted(found.items()):
                f.add("平台 URL 冲突", path, num,
                      f"「{name}」出现多个不同域名，其一为 {host}")


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    files = md_files()
    if not files:
        print("check_docs: 未找到任何 Markdown 文件。", file=sys.stderr)
        return 1

    f = Findings()
    for path in files:
        lines = list(iter_lines(path.read_text(encoding="utf-8")))
        check_links(path, lines, f)
        check_section_numbering(path, lines, f)
        check_subject_enum(path, lines, f)
        check_source_keys(path, lines, f)
        check_paths(path, lines, f)
    check_platform_urls(files, f)

    print(f"check_docs: 已检查 {len(files)} 个文件。")
    return f.report()


if __name__ == "__main__":
    sys.exit(main())
