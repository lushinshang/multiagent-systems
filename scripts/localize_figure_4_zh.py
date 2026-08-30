#!/usr/bin/env python3
"""Localize Figure 4 while preserving every curve and shaded plot pixel."""

from argparse import ArgumentParser
from pathlib import Path

from localize_figure_common import LABEL_COLOR, LEGEND_COLOR, TITLE_COLOR, clear, draw_centered, draw_left_centered, font_at, load_source, paste_vertical_label, save_png


def localize(source: Path, output: Path) -> None:
    image, draw, font_path = load_source(source)

    for box in (
        (850, 15, 1250, 67),
        (745, 1136, 1355, 1185),
        (8, 447, 61, 776),
        (500, 979, 674, 1014),
        (500, 1016, 674, 1051),
    ):
        clear(draw, box)

    title_font = font_at(font_path, 34)
    axis_font = font_at(font_path, 28)
    baseline_font = font_at(font_path, 18)
    draw_centered(draw, (1051, 45), "輕信度曲線", title_font, TITLE_COLOR)
    draw_centered(draw, (1051, 1159), "不可信斥候說謊比率", axis_font, LABEL_COLOR)
    paste_vertical_label(image, (42, 611), "路徑決策準確率", font_path, 28)
    draw_left_centered(draw, (510, 997), "全部信任基準線", baseline_font, LEGEND_COLOR)
    draw_left_centered(draw, (510, 1034), "識別說謊者基準線", baseline_font, LEGEND_COLOR)

    save_png(image, source, output, font_path)


def main() -> None:
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=Path("assets/en/figure-4-gullibility-curve.png"))
    parser.add_argument("--output", type=Path, default=Path("assets/figure-4-gullibility-curve-zh.png"))
    args = parser.parse_args()
    localize(args.input, args.output)


if __name__ == "__main__":
    main()
