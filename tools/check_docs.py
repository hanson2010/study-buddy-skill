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

# 高考的封闭学科集合，覆盖 3+3 与 3+1+2 两种模式。
# 九科是枚举上限；单个学生实际启用哪几科由其选科组合决定（见 SKILL.md「启用学科」）。
SUBJECTS = {
    "语文", "数学", "英语",           # 必考
    "物理", "化学", "生物",           # 理科选考
    "政治", "历史", "地理",           # 文科选考
}
SUBJECT_PLACEHOLDERS = {"[学科]", "[选考1]", "[选考2]", "[选考3]"}

# 「这份资料来自哪个原始文件」统一用 source_path
CANONICAL_SOURCE_KEY = "source_path"
DEPRECATED_SOURCE_KEYS = {"image_path", "source_file"}

# 编译连接键：raw/notes 记录用复数数组 topics，单值 topic 只允许出现在知识点档案里
CANONICAL_TOPICS_KEY = "topics"
TOPIC_SINGULAR_ALLOWED_FILES = {"templates/topic_templates.md"}

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
# 源层只有 raw/sources/YYYY/MM/ 与 raw/notes/YYYY/MM/ 两种写法
RE_RAW_PATH = re.compile(r"\braw/(?!(?:sources|notes)/YYYY/MM/)[\w/<>-]*")
RE_RAW_REAL_DATE = re.compile(r"raw/(?:sources|notes)/\d{4}/\d{2}/[\w.-]*")
# 编译层不得出现日期目录：按日期归档的记录属于源层 raw/notes/
# 学科编译层：subjects/<学科>/YYYY/...  升学编译层：colleges/YYYY/...
RE_LEGACY_SUBJECT_PATH = re.compile(r"subjects/[^/\s`）、，。]+/(?:YYYY|\d{4})\b[\w/<>-]*")
RE_LEGACY_COLLEGE_PATH = re.compile(r"colleges/(?:YYYY|\d{4})\b[\w/<>-]*")
RE_TOPIC_SINGULAR = re.compile(r"^\s*topic:\s")

CANONICAL_LOG_PATH = "output/YYYY/MM/YYYY-MM-DD-log.md"
CANONICAL_RAW_PATHS = ("raw/sources/YYYY/MM/", "raw/notes/YYYY/MM/")
# 目录树里单独出现的节点，不是完整路径
RAW_PATH_NODES = {"raw/", "raw/sources/", "raw/notes/"}


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
    """5. 日志路径与源层路径各只有固定几种写法。"""
    for num, line, _ in lines:
        for hit in RE_LOG_PATH.findall(line):
            if hit == "YYYY-MM-DD-log.md":
                continue  # 裸文件名（如目录树、示例）可接受
            if hit != CANONICAL_LOG_PATH:
                f.add("日志路径", path, num,
                      f"日志路径「{hit}」应为「{CANONICAL_LOG_PATH}」")

        for hit in RE_RAW_PATH.findall(line):
            if hit in RAW_PATH_NODES:
                continue  # 目录树里单独出现的节点可接受
            # 示例路径用真实年月（如 raw/sources/2026/07/photo.jpg）同样合法
            if RE_RAW_REAL_DATE.fullmatch(hit):
                continue
            expected = " 或 ".join(CANONICAL_RAW_PATHS)
            f.add("源层路径", path, num,
                  f"源层路径「{hit}」应为「{expected}」形式")


def check_compile_layer(path: Path, lines, f: Findings) -> None:
    """6. 编译层不得按日期分目录——那是源层 raw/notes/ 的职责。

    这是「源层与编译层分离」这条不变式的机械断言：迁移遗漏或规则回潮
    都会在文档里留下「学科目录/年份」或「colleges/年份」形式的路径。

    注意本检查按字面匹配，因此文档里不能写出反例的字面形式，否则会检查到
    自己；需要举例时改用 <年>/<月> 这类中文占位符。
    """
    for num, line, _ in lines:
        for pattern in (RE_LEGACY_SUBJECT_PATH, RE_LEGACY_COLLEGE_PATH):
            for hit in pattern.findall(line):
                f.add("编译层日期目录", path, num,
                      f"「{hit}」把日期目录放进了编译层；按日期归档的记录应在 raw/notes/YYYY/MM/ 下")


def check_topics_key(path: Path, lines, f: Findings) -> None:
    """7. 编译连接键统一用复数数组 topics。

    单值 topic: 会让一道命中多个知识点的题只编译进一个档案，其余档案
    永远收不到这条记录——这是最难靠肉眼发现的一类缺陷。
    知识点档案本身是围绕单个知识点组织的，故其模板文件豁免。
    """
    rel = path.relative_to(ROOT).as_posix()
    if any(rel.endswith(allowed) for allowed in TOPIC_SINGULAR_ALLOWED_FILES):
        return
    for num, line, _ in lines:
        if RE_TOPIC_SINGULAR.match(line):
            f.add("frontmatter 键名", path, num,
                  f"单值「topic:」应改为数组「{CANONICAL_TOPICS_KEY}:」")


def check_platform_urls(files: list[Path], f: Findings) -> None:
    """8. 同一个平台名不得对应多个不同 URL。"""
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
        check_compile_layer(path, lines, f)
        check_topics_key(path, lines, f)
    check_platform_urls(files, f)

    print(f"check_docs: 已检查 {len(files)} 个文件。")
    return f.report()


if __name__ == "__main__":
    sys.exit(main())
