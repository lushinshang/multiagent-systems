#!/usr/bin/env python3
"""Localize Figure 5 while preserving bars, error bars, and ceiling marks."""

from argparse import ArgumentParser
from pathlib import Path

from localize_figure_common import LEGEND_COLOR, TITLE_COLOR, clear, draw_centered, draw_left_centered, font_at, load_source, paste_vertical_label, save_png


def localize(source: Path, output: Path) -> None:
    image, draw, font_path = load_source(source)

    clear(draw, (790, 13, 1320, 70))
    clear(draw, (242, 92, 430, 127))
    clear(draw, (8, 155, 67, 1070))

    title_font = font_at(font_path, 35)
    legend_font = font_at(font_path, 25)
    draw_centered(draw, (1057, 45), "各模型群體決策準確率", title_font, TITLE_COLOR)
    draw_left_centered(draw, (258, 115), "單一代理上限", legend_font, LEGEND_COLOR)
    paste_vertical_label(image, (42, 622), "隱藏特徵群體決策準確率（%）", font_path, 28)

    save_png(image, source, output, font_path)


def main() -> None:
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=Path("assets/en/figure-5-hidden-profile-group-accuracy.png"))
    parser.add_argument("--output", type=Path, default=Path("assets/figure-5-hidden-profile-group-accuracy-zh.png"))
    args = parser.parse_args()
    localize(args.input, args.output)


if __name__ == "__main__":
    main()
