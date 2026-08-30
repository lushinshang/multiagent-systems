#!/usr/bin/env python3
"""Localize Anthropic Figure 1 into Taiwan Traditional Chinese.

The script deliberately edits only the title, axis-label, and legend text
regions. Plot lines, symbols, tick labels, annotations, and the legend's
line-style samples remain pixel-identical to the English source.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


BASE_SIZE = (2000, 1200)
BACKGROUND = (252, 252, 251, 255)
TITLE_COLOR = (184, 96, 70, 255)
LABEL_COLOR = (82, 81, 78, 255)
LEGEND_COLOR = (11, 11, 11, 255)

FONT_CANDIDATES = (
    Path("/System/Library/Fonts/PingFang.ttc"),
    Path("/System/Library/Fonts/STHeiti Medium.ttc"),
    Path("/System/Library/Fonts/Supplemental/Arial Unicode.ttf"),
)


def find_cjk_font() -> Path:
    """Return the first installed font known to support Traditional Chinese."""
    for candidate in FONT_CANDIDATES:
        if candidate.is_file():
            return candidate
    choices = "\n  - ".join(str(p) for p in FONT_CANDIDATES)
    raise FileNotFoundError(f"找不到支援繁體中文的字體：\n  - {choices}")


def scaled_rect(box: tuple[int, int, int, int], sx: float, sy: float) -> tuple[int, int, int, int]:
    return tuple(round(v * (sx if i % 2 == 0 else sy)) for i, v in enumerate(box))  # type: ignore[return-value]


def font_at(font_path: Path, px: int, scale: float) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(font_path), max(1, round(px * scale)))


def draw_centered(
    draw: ImageDraw.ImageDraw,
    xy: tuple[float, float],
    text: str,
    font: ImageFont.FreeTypeFont,
    fill: tuple[int, int, int, int],
) -> None:
    # Center by the glyph's actual ink bounds. This avoids the unusually tall
    # ascender/descender metrics exposed by some macOS CJK font collections.
    bbox = draw.textbbox((0, 0), text, font=font)
    position = (
        xy[0] - (bbox[0] + bbox[2]) / 2,
        xy[1] - (bbox[1] + bbox[3]) / 2,
    )
    draw.text(position, text, font=font, fill=fill)


def localize(source: Path, output: Path) -> None:
    image = Image.open(source).convert("RGBA")
    width, height = image.size
    sx, sy = width / BASE_SIZE[0], height / BASE_SIZE[1]
    font_scale = min(sx, sy)
    font_path = find_cjk_font()
    draw = ImageDraw.Draw(image)

    # Remove only the original English title and axis labels.
    draw.rectangle(scaled_rect((640, 18, 1460, 68), sx, sy), fill=BACKGROUND)
    draw.rectangle(scaled_rect((640, 1132, 1470, 1184), sx, sy), fill=BACKGROUND)
    draw.rectangle(scaled_rect((8, 420, 64, 730), sx, sy), fill=BACKGROUND)

    title_font = font_at(font_path, 36, font_scale)
    axis_font = font_at(font_path, 29, font_scale)

    draw_centered(
        draw,
        (1052 * sx, 43 * sy),
        "發現之漏洞數量與抽樣 Token 數（百萬）",
        title_font,
        TITLE_COLOR,
    )
    draw_centered(
        draw,
        (1052 * sx, 1158 * sy),
        "累計抽樣輸出 Token 數（百萬）",
        axis_font,
        LABEL_COLOR,
    )

    # Render the y-axis label horizontally at 4× and rotate it for crisper CJK glyphs.
    y_text = "發現之漏洞數量"
    hi = 4
    y_font = ImageFont.truetype(str(font_path), round(29 * font_scale * hi))
    probe = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    bbox = probe.textbbox((0, 0), y_text, font=y_font)
    pad = round(6 * font_scale * hi)
    label = Image.new("RGBA", (bbox[2] - bbox[0] + 2 * pad, bbox[3] - bbox[1] + 2 * pad), (0, 0, 0, 0))
    label_draw = ImageDraw.Draw(label)
    label_draw.text((pad - bbox[0], pad - bbox[1]), y_text, font=y_font, fill=LABEL_COLOR)
    label = label.rotate(90, expand=True, resample=Image.Resampling.BICUBIC)
    label = label.resize((round(label.width / hi), round(label.height / hi)), Image.Resampling.LANCZOS)
    y_center = (36 * sx, 575 * sy)
    image.alpha_composite(label, (round(y_center[0] - label.width / 2), round(y_center[1] - label.height / 2)))

    # Clear each English legend label separately. The colored stars/line samples
    # at x=1325..1381 and the rounded legend border are intentionally untouched.
    legend_rows = ((818, 845), (854, 881), (891, 918), (927, 954), (964, 991), (1000, 1027), (1037, 1064))
    for top, bottom in legend_rows:
        draw.rectangle(scaled_rect((1390, top, 1954, bottom), sx, sy), fill=BACKGROUND)

    legend_font = font_at(font_path, 24, font_scale)
    legend_text = (
        "平行獨立代理：Claude Opus 4.8",
        "協同：Claude Opus 4.8",
        "協同群體與平行獨立代理共同發現之漏洞",
        "平行獨立代理：Claude Mythos Preview",
        "協同：Claude Mythos Preview",
        "協同：Claude Mythos Preview（僅核心漏洞）",
        "協同群體與平行獨立代理共同發現之漏洞",
    )
    row_centers = (832, 868, 905, 941, 978, 1014, 1051)
    assert len(legend_text) == len(row_centers)
    for text, center_y in zip(legend_text, row_centers):
        draw.text((1397 * sx, center_y * sy), text, font=legend_font, fill=LEGEND_COLOR, anchor="lm")

    output.parent.mkdir(parents=True, exist_ok=True)
    dpi = image.info.get("dpi", (72, 72))
    image.save(output, format="PNG", dpi=dpi, optimize=True)
    print(f"已輸出：{output}")
    print(f"尺寸：{width} × {height} px；字體：{font_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("assets/en/figure-1-vulnerabilities-vs-tokens.png"),
        help="英文來源 PNG",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("assets/figure-1-vulnerabilities-vs-tokens-zh.png"),
        help="繁體中文輸出 PNG",
    )
    args = parser.parse_args()
    localize(args.input, args.output)


if __name__ == "__main__":
    main()
