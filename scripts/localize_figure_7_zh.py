#!/usr/bin/env python3
"""Localize Figure 7 while preserving all scatter points and stems."""

from argparse import ArgumentParser
from pathlib import Path

from localize_figure_common import LABEL_COLOR, LEGEND_COLOR, TITLE_COLOR, clear, draw_centered, draw_left_centered, font_at, load_source, paste_vertical_label, save_png


def localize(source: Path, output: Path) -> None:
    image, draw, font_path = load_source(source)

    clear(draw, (595, 12, 1070, 68))
    clear(draw, (8, 470, 63, 730))

    title_font = font_at(font_path, 34)
    annotation_font = font_at(font_path, 22)
    legend_font = font_at(font_path, 19)
    draw_centered(draw, (832, 45), "各情境達成解決的時間", title_font, TITLE_COLOR)
    paste_vertical_label(image, (40, 601), "達成解決耗時（小時）", font_path, 28)

    annotations = (
        ((144, 101, 330, 151), (235, 127), "47 個未解決"),
        ((378, 101, 565, 151), (473, 127), "14 個未解決"),
        ((619, 101, 808, 151), (713, 127), "48 個未解決"),
        ((855, 101, 1044, 151), (950, 127), "4 個未解決"),
    )
    for box, center, text in annotations:
        clear(draw, box)
        draw_centered(draw, center, text, annotation_font, LABEL_COLOR)

    legend_rows = (
        ((1655, 521, 1960, 560), 542, "達成停戰協議"),
        ((1655, 559, 1960, 597), 579, "武力解決（權限拔除）"),
        ((1655, 596, 1960, 634), 616, "被動放棄"),
        ((1655, 633, 1960, 671), 653, "最初以武力解決"),
    )
    for box, center_y, text in legend_rows:
        clear(draw, box)
        draw_left_centered(draw, (1667, center_y), text, legend_font, LEGEND_COLOR)

    save_png(image, source, output, font_path)


def main() -> None:
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=Path("assets/en/figure-7-time-to-resolution.png"))
    parser.add_argument("--output", type=Path, default=Path("assets/figure-7-time-to-resolution-zh.png"))
    args = parser.parse_args()
    localize(args.input, args.output)


if __name__ == "__main__":
    main()
