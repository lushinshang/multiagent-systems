#!/usr/bin/env python3
"""Shared pixel-preserving helpers for Traditional Chinese figure localization."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


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
    for candidate in FONT_CANDIDATES:
        if candidate.is_file():
            return candidate
    choices = "\n  - ".join(str(path) for path in FONT_CANDIDATES)
    raise FileNotFoundError(f"找不到支援繁體中文的字體：\n  - {choices}")


def load_source(source: Path) -> tuple[Image.Image, ImageDraw.ImageDraw, Path]:
    image = Image.open(source).convert("RGBA")
    return image, ImageDraw.Draw(image), find_cjk_font()


def font_at(font_path: Path, px: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(font_path), px)


def clear(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int]) -> None:
    """Clear a known text-only box using the figure's exact background color."""
    draw.rectangle(box, fill=BACKGROUND)


def draw_centered(
    draw: ImageDraw.ImageDraw,
    center: tuple[float, float],
    text: str,
    font: ImageFont.FreeTypeFont,
    fill: tuple[int, int, int, int],
) -> None:
    bbox = draw.textbbox((0, 0), text, font=font)
    draw.text(
        (
            center[0] - (bbox[0] + bbox[2]) / 2,
            center[1] - (bbox[1] + bbox[3]) / 2,
        ),
        text,
        font=font,
        fill=fill,
    )


def draw_left_centered(
    draw: ImageDraw.ImageDraw,
    xy: tuple[float, float],
    text: str,
    font: ImageFont.FreeTypeFont,
    fill: tuple[int, int, int, int],
) -> None:
    bbox = draw.textbbox((0, 0), text, font=font)
    draw.text((xy[0] - bbox[0], xy[1] - (bbox[1] + bbox[3]) / 2), text, font=font, fill=fill)


def paste_vertical_label(
    image: Image.Image,
    center: tuple[float, float],
    text: str,
    font_path: Path,
    px: int,
    fill: tuple[int, int, int, int] = LABEL_COLOR,
) -> None:
    """Render at 4x before rotation for crisp vertical Traditional Chinese."""
    hi = 4
    font = ImageFont.truetype(str(font_path), px * hi)
    probe = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    bbox = probe.textbbox((0, 0), text, font=font)
    pad = 6 * hi
    label = Image.new(
        "RGBA",
        (bbox[2] - bbox[0] + 2 * pad, bbox[3] - bbox[1] + 2 * pad),
        (0, 0, 0, 0),
    )
    label_draw = ImageDraw.Draw(label)
    label_draw.text((pad - bbox[0], pad - bbox[1]), text, font=font, fill=fill)
    label = label.rotate(90, expand=True, resample=Image.Resampling.BICUBIC)
    label = label.resize((round(label.width / hi), round(label.height / hi)), Image.Resampling.LANCZOS)
    image.alpha_composite(label, (round(center[0] - label.width / 2), round(center[1] - label.height / 2)))


def save_png(image: Image.Image, source: Path, output: Path, font_path: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    dpi = Image.open(source).info.get("dpi", (72, 72))
    image.save(output, format="PNG", dpi=dpi, optimize=True)
    print(f"已輸出：{output}")
    print(f"尺寸：{image.width} × {image.height} px；字體：{font_path}")
