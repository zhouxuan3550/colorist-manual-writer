#!/usr/bin/env python3
"""Static checks for colorist-manual-writer article drafts."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


BANNED_TERMS = [
    "说白了",
    "意味着什么",
    "这意味着",
    "本质上",
    "换句话说",
    "不可否认",
    "综上所述",
    "总的来说",
    "首先",
    "其次",
    "最后",
    "值得注意的是",
    "不难发现",
    "让我们来看看",
    "接下来让我们",
]

VAGUE_TOOL_TERMS = ["AI工具", "某个模型", "相关技术"]

STRONG_CATCHPHRASES = [
    "尼玛",
    "不是哥们",
    "这玩意",
    "坦率的讲",
    "我是真的觉得",
    "太牛逼",
    "太特么",
    "卧槽",
    "给我整不会",
    "给我一下子",
    "更干懵",
    "比较骚",
    "有个屁",
]

INDUSTRY_TERMS = [
    "影视幕后",
    "后期",
    "剪辑",
    "调色",
    "修图",
    "摄影",
    "分镜",
    "景别",
    "构图",
    "景深",
    "对焦",
    "时间线",
    "素材",
    "工程文件",
    "节点",
    "LUT",
    "降噪",
    "肤色",
    "暗部",
    "声音设计",
    "拟音",
    "字幕",
    "VFX",
    "B-Roll",
    "杜比视界",
    "HDR",
    "DaVinci",
    "Resolve",
    "FCPX",
]


def strip_code_blocks(text: str) -> str:
    return re.sub(r"```.*?```", "", text, flags=re.S)


def visible_len(text: str) -> int:
    return len(re.sub(r"\s+", "", text))


def paragraphs(text: str) -> list[str]:
    body = strip_code_blocks(text)
    paras = [p.strip() for p in re.split(r"\n\s*\n", body) if p.strip()]
    skipped_prefixes = ("#", "-", "*", ">", "|")
    return [
        p
        for p in paras
        if not p.startswith(skipped_prefixes)
        and not re.match(r"^\d+[.、]", p)
        and len(p) > 2
    ]


def is_single_sentence_para(para: str) -> bool:
    compact = re.sub(r"\s+", "", para)
    if len(compact) > 80:
        return False
    marks = re.findall(r"[。！？?!…]+", compact)
    return len(marks) <= 1


def count_hits(text: str, terms: list[str]) -> dict[str, int]:
    return {term: text.count(term) for term in terms if text.count(term)}


def line_numbers(text: str, needle: str) -> list[int]:
    return [i for i, line in enumerate(text.splitlines(), start=1) if needle in line]


def main() -> int:
    parser = argparse.ArgumentParser(description="Check a 调色师手册 article draft.")
    parser.add_argument("file", nargs="?", help="Article file. Reads stdin when omitted.")
    parser.add_argument(
        "--industry",
        action="store_true",
        help="Require at least one影视/后期/摄影修图 industry term.",
    )
    args = parser.parse_args()

    if args.file:
        text = Path(args.file).read_text(encoding="utf-8")
        label = args.file
    else:
        text = sys.stdin.read()
        label = "stdin"

    clean = strip_code_blocks(text)
    paras = paragraphs(text)
    single_flags = [is_single_sentence_para(p) for p in paras]
    single_count = sum(single_flags)
    ratio = single_count / len(paras) if paras else 0

    max_run = 0
    run = 0
    for flag in single_flags:
        run = run + 1 if flag else 0
        max_run = max(max_run, run)

    banned = count_hits(clean, BANNED_TERMS)
    vague_tools = count_hits(clean, VAGUE_TOOL_TERMS)
    catchphrases = count_hits(clean, STRONG_CATCHPHRASES)
    catchphrase_total = sum(catchphrases.values())
    length_units = max(1, visible_len(clean) / 1000)
    catchphrase_rate = catchphrase_total / length_units

    fixed_tail = any(term in clean for term in ["作者：", "投稿或爆料", "wzglyay", "virxact", "转发三连"])
    quality_report = "## 质检报告" in clean or "**L1 硬性规则**" in clean
    industry_hits = count_hits(clean, INDUSTRY_TERMS)

    warnings: list[str] = []
    if ratio > 0.25:
        warnings.append(f"单句段落比例偏高：{single_count}/{len(paras)} = {ratio:.0%}")
    if max_run > 2:
        warnings.append(f"连续单句段落过多：最长连续 {max_run} 段")
    if banned:
        details = ", ".join(f"{k}×{v}" for k, v in banned.items())
        warnings.append(f"禁用词命中：{details}")
    if vague_tools:
        details = ", ".join(f"{k}×{v}" for k, v in vague_tools.items())
        warnings.append(f"空泛工具名命中：{details}")
    if catchphrase_rate > 5:
        details = ", ".join(f"{k}×{v}" for k, v in catchphrases.items())
        warnings.append(f"强口癖过密：约 {catchphrase_rate:.1f}/千字，{details}")
    if fixed_tail:
        warnings.append("检测到固定尾部/署名/投稿信息，确认用户是否明确要求完整发布稿")
    if quality_report:
        warnings.append("检测到质检报告残留，普通草稿不应输出质检报告")
    if args.industry and not industry_hits:
        warnings.append("未检测到影视后期/摄影修图行业底色词，相关选题可能需要补行业落点")

    print(f"检查对象：{label}")
    print(f"段落数：{len(paras)}")
    print(f"单句段落：{single_count} ({ratio:.0%})")
    print(f"最长连续单句段落：{max_run}")
    print(f"强口癖：{catchphrase_total}，约 {catchphrase_rate:.1f}/千字")
    if industry_hits:
        details = ", ".join(f"{k}×{v}" for k, v in sorted(industry_hits.items()))
        print(f"行业词：{details}")

    if warnings:
        print("\n警告：")
        for item in warnings:
            print(f"- {item}")
        return 1

    print("\n通过：未发现主要结构风险。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
