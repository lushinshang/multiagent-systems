#!/usr/bin/env python3
"""Localize Figure 2 while preserving all plotted pixels and model names."""

from argparse import ArgumentParser
from pathlib import Path

from localize_figure_common import LABEL_COLOR, TITLE_COLOR, clear, draw_centered, font_at, load_source, paste_vertical_label, save_png


def localize(source: Path, output: Path) -> None:
    image, draw, font_path = load_source(source)

    for box in (
        (400, 12, 690, 51),
        (1405, 12, 1668, 51),
        (385, 658, 700, 706),
        (1380, 658, 1698, 706),
        (8, 188, 54, 486),
        (990, 170, 1028, 505),
    ):
        clear(draw, box)

    title_font = font_at(font_path, 27)
    axis_font = font_at(font_path, 21)
    draw_centered(draw, (544, 34), "已合併 PR 比例", title_font, TITLE_COLOR)
    draw_centered(draw, (1536, 34), "程式碼共享程度", title_font, TITLE_COLOR)
    draw_centered(draw, (541, 673), "模擬中的代理數量", axis_font, LABEL_COLOR)
    draw_centered(draw, (1537, 673), "模擬中的代理數量", axis_font, LABEL_COLOR)
    paste_vertical_label(image, (31, 338), "PR 已合併比例", font_path, 21)
    paste_vertical_label(image, (1014, 338), "代理程式碼共享程度中位數", font_path, 20)

    save_png(image, source, output, font_path)


def main() -> None:
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=Path("assets/en/figure-2-pr-merge-fraction-and-code-sharing.png"))
    parser.add_argument("--output", type=Path, default=Path("assets/figure-2-pr-merge-fraction-and-code-sharing-zh.png"))
    args = parser.parse_args()
    localize(args.input, args.output)


if __name__ == "__main__":
    main()
