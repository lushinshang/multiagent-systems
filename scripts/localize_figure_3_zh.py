#!/usr/bin/env python3
"""Localize Figure 3 while preserving PR curves, ticks, and annotations."""

from argparse import ArgumentParser
from pathlib import Path

from localize_figure_common import LABEL_COLOR, LEGEND_COLOR, TITLE_COLOR, clear, draw_centered, draw_left_centered, font_at, load_source, paste_vertical_label, save_png


def localize(source: Path, output: Path) -> None:
    image, draw, font_path = load_source(source)

    clear(draw, (550, 6, 1450, 61))
    for box in (
        (340, 540, 483, 588),
        (985, 540, 1128, 588),
        (340, 1050, 483, 1100),
        (985, 1050, 1128, 1100),
        (1634, 1050, 1778, 1100),
        (8, 200, 59, 432),
        (8, 712, 59, 948),
    ):
        clear(draw, box)

    title_font = font_at(font_path, 31)
    axis_font = font_at(font_path, 27)
    draw_centered(draw, (1000, 34), "PR 活動隨時間變化（n = 80，基準提示詞）", title_font, TITLE_COLOR)
    for center in ((409, 566), (1057, 566), (409, 1077), (1057, 1077), (1706, 1077)):
        draw_centered(draw, center, "小時", axis_font, LABEL_COLOR)
    paste_vertical_label(image, (39, 317), "累計 PR 數量", font_path, 27)
    paste_vertical_label(image, (39, 829), "累計 PR 數量", font_path, 27)

    legend_rows = (
        ((1607, 258, 1910, 299), 279, "已開啟"),
        ((1607, 297, 1910, 337), 317, "已關閉"),
        ((1607, 335, 1910, 375), 355, "已關閉並合併"),
    )
    legend_font = font_at(font_path, 25)
    for box, center_y, text in legend_rows:
        clear(draw, box)
        draw_left_centered(draw, (1618, center_y), text, legend_font, LEGEND_COLOR)

    save_png(image, source, output, font_path)


def main() -> None:
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=Path("assets/en/figure-3-pr-progress-12hr.png"))
    parser.add_argument("--output", type=Path, default=Path("assets/figure-3-pr-progress-12hr-zh.png"))
    args = parser.parse_args()
    localize(args.input, args.output)


if __name__ == "__main__":
    main()
