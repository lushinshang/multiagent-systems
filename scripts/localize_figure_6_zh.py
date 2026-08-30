#!/usr/bin/env python3
"""Localize Figure 6 while preserving stacked bars and value labels."""

from argparse import ArgumentParser
from pathlib import Path

from localize_figure_common import LEGEND_COLOR, TITLE_COLOR, clear, draw_centered, draw_left_centered, font_at, load_source, paste_vertical_label, save_png


def localize(source: Path, output: Path) -> None:
    image, draw, font_path = load_source(source)

    clear(draw, (540, 12, 1210, 68))
    clear(draw, (8, 490, 62, 713))

    title_font = font_at(font_path, 34)
    legend_font = font_at(font_path, 20)
    draw_centered(draw, (875, 45), "多代理地盤爭奪的最終結果", title_font, TITLE_COLOR)
    paste_vertical_label(image, (39, 601), "情境結果比例（%）", font_path, 28)

    legend_rows = (
        ((1705, 521, 1960, 560), 542, "未解決"),
        ((1705, 559, 1960, 597), 578, "武力解決（權限拔除）"),
        ((1705, 596, 1960, 634), 615, "被動放棄"),
        ((1705, 633, 1960, 670), 652, "達成停戰協議"),
    )
    for box, center_y, text in legend_rows:
        clear(draw, box)
        draw_left_centered(draw, (1718, center_y), text, legend_font, LEGEND_COLOR)

    save_png(image, source, output, font_path)


def main() -> None:
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=Path("assets/en/figure-6-turf-war-outcomes.png"))
    parser.add_argument("--output", type=Path, default=Path("assets/figure-6-turf-war-outcomes-zh.png"))
    args = parser.parse_args()
    localize(args.input, args.output)


if __name__ == "__main__":
    main()
