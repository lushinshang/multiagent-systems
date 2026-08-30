#!/usr/bin/env python3
"""Render the responsive Traditional Chinese multi-agent research overview.

The artwork is built from Pillow primitives so every chart, number, arrow and
label is deterministic. Both outputs are rendered at 2x and downsampled for
clean type and antialiased vector-like edges.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
FONT_CANDIDATES = (
    Path("/System/Library/Fonts/STHeiti Medium.ttc"),
    Path("/System/Library/Fonts/PingFang.ttc"),
)

# Required palette
BG = "#F9F7F4"
CARD = "#FFFFFF"
BORDER = "#E5E2DC"
ACCENT = "#B86046"
ACCENT_DARK = "#8F432F"
ACCENT_PALE = "#F5E7E1"
GREEN = "#2E7D32"
GREEN_PALE = "#E8F3E9"
RED = "#C62828"
RED_PALE = "#FBE9E8"
TEXT = "#1A1A1A"
MUTED = "#5C5955"
SOFT = "#8B8782"
INK_PALE = "#EEECE8"
GOLD = "#C58A22"


@dataclass(frozen=True)
class Box:
    x: float
    y: float
    w: float
    h: float

    @property
    def right(self) -> float:
        return self.x + self.w

    @property
    def bottom(self) -> float:
        return self.y + self.h


class Artboard:
    def __init__(self, width: int, height: int, scale: int = 2):
        self.width = width
        self.height = height
        self.scale = scale
        self.image = Image.new("RGBA", (width * scale, height * scale), BG)
        self.draw = ImageDraw.Draw(self.image)
        self.font_path = next((p for p in FONT_CANDIDATES if p.exists()), None)
        if self.font_path is None:
            raise FileNotFoundError("No supported Traditional Chinese system font found")

    def s(self, value):
        if isinstance(value, Box):
            return tuple(round(v * self.scale) for v in (value.x, value.y, value.right, value.bottom))
        if isinstance(value, (tuple, list)):
            return tuple(round(v * self.scale) for v in value)
        return round(value * self.scale)

    def font(self, size: float, bold: bool = False):
        return ImageFont.truetype(str(self.font_path), self.s(size + (1 if bold else 0)), index=0)

    def text(self, xy, value: str, size: float, fill=TEXT, anchor=None, bold=False):
        self.draw.text(self.s(xy), value, font=self.font(size, bold), fill=fill, anchor=anchor)

    def text_width(self, value: str, size: float, bold=False) -> float:
        return self.draw.textlength(value, font=self.font(size, bold)) / self.scale

    def fit_text(self, xy, value: str, max_width: float, size: float, min_size=16,
                 fill=TEXT, anchor=None, bold=False):
        while size > min_size and self.text_width(value, size, bold) > max_width:
            size -= 1
        self.text(xy, value, size, fill, anchor, bold)

    def rounded(self, box: Box, radius: float, fill, outline=None, width=1):
        self.draw.rounded_rectangle(self.s(box), radius=self.s(radius), fill=fill,
                                    outline=outline, width=self.s(width))

    def ellipse(self, box: Box, fill, outline=None, width=1):
        self.draw.ellipse(self.s(box), fill=fill, outline=outline, width=self.s(width))

    def line(self, pts, fill, width=2, joint="curve"):
        self.draw.line([self.s(p) for p in pts], fill=fill, width=self.s(width), joint=joint)

    def polygon(self, pts, fill, outline=None):
        scaled = [self.s(p) for p in pts]
        self.draw.polygon(scaled, fill=fill)
        if outline:
            self.draw.line(scaled + [scaled[0]], fill=outline, width=self.s(2), joint="curve")

    def shadow(self, box: Box, radius=24, blur=14, dy=7, alpha=22):
        layer = Image.new("RGBA", self.image.size, (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        target = Box(box.x, box.y + dy, box.w, box.h)
        ld.rounded_rectangle(self.s(target), radius=self.s(radius), fill=(50, 40, 32, alpha))
        self.image.alpha_composite(layer.filter(ImageFilter.GaussianBlur(self.s(blur))))

    def arrow(self, start, end, fill=ACCENT, width=4, head=12):
        x1, y1 = start
        x2, y2 = end
        self.line([(x1, y1), (x2, y2)], fill, width)
        if abs(x2 - x1) >= abs(y2 - y1):
            direction = 1 if x2 >= x1 else -1
            pts = [(x2, y2), (x2 - direction * head, y2 - head * .65),
                   (x2 - direction * head, y2 + head * .65)]
        else:
            direction = 1 if y2 >= y1 else -1
            pts = [(x2, y2), (x2 - head * .65, y2 - direction * head),
                   (x2 + head * .65, y2 - direction * head)]
        self.polygon(pts, fill)

    def save(self, path: Path):
        final = self.image.convert("RGB").resize((self.width, self.height), Image.Resampling.LANCZOS)
        path.parent.mkdir(parents=True, exist_ok=True)
        final.save(path, "PNG", optimize=True, dpi=(144, 144))
        return final


def draw_agent(a: Artboard, cx, cy, radius=19, color=ACCENT, label=None):
    a.ellipse(Box(cx - radius, cy - radius, radius * 2, radius * 2), CARD, color, 3)
    a.ellipse(Box(cx - radius * .28, cy - radius * .42, radius * .56, radius * .56), color)
    a.line([(cx - radius * .52, cy + radius * .48), (cx, cy + radius * .12),
            (cx + radius * .52, cy + radius * .48)], color, 3)
    if label:
        a.text((cx, cy + radius + 8), label, 17, MUTED, "ma")


def node(a: Artboard, box: Box, title: str, subtitle: str = "", tone=ACCENT_PALE,
         border=ACCENT, title_color=TEXT, title_size=22):
    a.rounded(box, 15, tone, border, 2)
    a.fit_text((box.x + box.w / 2, box.y + box.h * (.42 if subtitle else .52)), title,
               box.w - 18, title_size, 14, title_color, "mm", True)
    if subtitle:
        a.fit_text((box.x + box.w / 2, box.y + box.h * .72), subtitle,
                   box.w - 18, title_size - 6, 12, MUTED, "mm")


def panel_title(a: Artboard, box: Box, title: str, kicker: str | None = None):
    a.text((box.x + 16, box.y + 12), title, 21, TEXT, bold=True)
    if kicker:
        a.text((box.right - 16, box.y + 14), kicker, 16, ACCENT_DARK, "ra", True)


def draw_collab_chart(a: Artboard, b: Box):
    panel_title(a, b, "80 代理：合併率 × 代碼共享", "980 PR")
    wide = b.w / b.h > 3
    if wide:
        labels_x = b.x + 18
        bars_x = b.x + 185
        bars_w = b.w - 410
        rows = [("Sonnet 4.6", 0.02, RED, "幾乎 0 合併"),
                ("Sonnet 5", .86, GREEN, "高合併＋高共享")]
        for i, (label, value, color, note) in enumerate(rows):
            y = b.y + 55 + i * 48
            a.text((labels_x, y + 12), label, 19, MUTED, "lm", True)
            a.rounded(Box(bars_x, y, bars_w, 23), 11, INK_PALE)
            a.rounded(Box(bars_x, y, max(9, bars_w * value), 23), 11, color)
            a.text((b.right - 14, y + 11), note, 17, color, "rm", True)
        return

    chart = Box(b.x + 18, b.y + 52, b.w - 36, b.h - 70)
    baseline = chart.bottom - 34
    a.line([(chart.x + 5, baseline), (chart.right - 5, baseline)], BORDER, 2)
    groups = [("Sonnet 4.6", RED, .04, .02, "980 PR", "≈0 合併"),
              ("Sonnet 5", GREEN, .84, .91, "高合併", "高共享")]
    group_w = chart.w / 2
    max_h = chart.h - 92
    for i, (label, color, merge, share, note1, note2) in enumerate(groups):
        gx = chart.x + i * group_w
        center = gx + group_w / 2
        for j, (val, cap) in enumerate(((merge, "合併"), (share, "共享"))):
            x = center - 51 + j * 60
            height = max(8, max_h * val)
            a.rounded(Box(x, baseline - height, 42, height), 8, color)
            a.text((x + 21, baseline + 8), cap, 15, MUTED, "ma")
        a.text((center, chart.y + 2), note1, 19, color, "ma", True)
        a.text((center, chart.y + 27), note2, 16, color, "ma")
        a.text((center, chart.bottom - 8), label, 18, TEXT, "ma", True)


def draw_collab_flow(a: Artboard, b: Box):
    panel_title(a, b, "協作失靈流程", "從共享到割據")
    wide = b.w / b.h > 3
    y = b.y + (72 if wide else 106)
    margin = 18
    gap = 34 if wide else 22
    w = (b.w - margin * 2 - gap * 2) / 3
    h = 70 if wide else 105
    boxes = [Box(b.x + margin + i * (w + gap), y, w, h) for i in range(3)]
    node(a, boxes[0], "80 代理協作", "共享檔案", GREEN_PALE, GREEN, title_size=20)
    node(a, boxes[1], "衝突風暴", "PR 互撞", RED_PALE, RED, title_size=20)
    node(a, boxes[2], "劃地自限", "檔案割據", ACCENT_PALE, ACCENT, title_size=20)
    for left, right in zip(boxes, boxes[1:]):
        a.arrow((left.right + 5, left.y + h / 2), (right.x - 7, right.y + h / 2), RED, 3, 10)
    if not wide:
        for dx in (-32, 0, 32):
            draw_agent(a, boxes[0].x + boxes[0].w / 2 + dx, boxes[0].bottom + 34, 11, GREEN)
        cx = boxes[1].x + boxes[1].w / 2
        cy = boxes[1].bottom + 34
        for dx, dy in ((-22, 0), (22, 0), (0, -22), (0, 22), (-16, -16), (16, 16)):
            a.line([(cx + dx * .42, cy + dy * .42), (cx + dx, cy + dy)], RED, 3)
        for i in range(3):
            a.rounded(Box(boxes[2].x + 18 + i * 42, boxes[2].bottom + 20, 32, 32), 5,
                      CARD, ACCENT, 2)


def draw_cartel(a: Artboard, b: Box):
    panel_title(a, b, "4 代理公開板合謀", "無需私訊")
    wide = b.w / b.h > 3
    cx = b.x + (b.w * .30 if wide else b.w / 2)
    cy = b.y + (b.h * .56 if wide else b.h * .55)
    ring_x = 105 if wide else 125
    ring_y = 56 if wide else 110
    center_w = 154 if wide else 186
    # Use an elliptical ring so all four agents remain visible around the
    # comparatively wide public-price board, even in the shallow mobile panel.
    agents = [(cx, cy - ring_y), (cx + ring_x, cy),
              (cx, cy + ring_y), (cx - ring_x, cy)]
    for x, y in agents:
        a.line([(x, y), (cx, cy)], ACCENT, 3)
        draw_agent(a, x, y, 15 if wide else 18, ACCENT)
    a.shadow(Box(cx - center_w / 2, cy - 31, center_w, 62), 12, 6, 3, 18)
    a.rounded(Box(cx - center_w / 2, cy - 31, center_w, 62), 13, ACCENT, ACCENT_DARK, 2)
    a.text((cx, cy - 7), "$10.00", 27, CARD, "mm", True)
    a.text((cx, cy + 19), "默契定價卡特爾", 14, CARD, "mm")
    if wide:
        x = b.x + b.w * .58
        node(a, Box(x, b.y + 52, b.right - x - 18, 52), "同模型＋同提示", "低行為變異",
             ACCENT_PALE, ACCENT, title_size=18)
        a.arrow((x + 20, b.y + 118), (x + 20, b.bottom - 23), ACCENT, 3, 9)
        a.text((x + 39, b.bottom - 31), "公開報價成為協調訊號", 17, MUTED, "lm")


def draw_queue(a: Artboard, b: Box):
    panel_title(a, b, "自發佇列 DDoS", "僅 117 件成功")
    wide = b.w / b.h > 3
    cy = b.y + b.h * (.62 if wide else .60)
    left = b.x + 22
    right = b.right - 22
    for row in range(3):
        for col in range(8 if wide else 7):
            x = left + col * (19 if wide else 21)
            y = cy - 30 + row * 22
            a.ellipse(Box(x, y, 9, 9), ACCENT if (row + col) % 3 else RED)
    req_x = left + (180 if wide else 155)
    a.text((left, b.y + 55), "30 次／秒輪詢", 20, RED, bold=True)
    funnel_x = b.x + b.w * (.58 if wide else .55)
    a.polygon([(funnel_x - 42, cy - 46), (funnel_x + 42, cy - 46),
               (funnel_x + 14, cy + 5), (funnel_x + 14, cy + 35),
               (funnel_x - 14, cy + 35), (funnel_x - 14, cy + 5)], RED_PALE, RED)
    a.text((funnel_x, cy - 13), "240 萬", 21, RED, "mm", True)
    a.text((funnel_x, cy + 12), "請求塞車", 15, MUTED, "mm")
    a.arrow((req_x, cy), (funnel_x - 49, cy), RED, 4, 11)
    out_x = right - (60 if wide else 64)
    a.arrow((funnel_x + 48, cy), (out_x - 54, cy), GREEN, 4, 11)
    a.rounded(Box(out_x - 50, cy - 34, 100, 68), 15, GREEN_PALE, GREEN, 2)
    a.text((out_x, cy - 6), "117", 27, GREEN, "mm", True)
    a.text((out_x, cy + 19), "成功", 15, GREEN, "mm")


def draw_accuracy(a: Artboard, b: Box):
    panel_title(a, b, "Hidden Profile 群體準確率", "真相沉沒")
    wide = b.w / b.h > 3
    label_w = 176 if wide else 140
    bar_x = b.x + label_w
    bar_w = b.w - label_w - 56
    top = b.y + (48 if wide else 62)
    row_gap = 39 if wide else 58
    rows = [("單體全知", 1.0, GREEN, "100%"), ("Mythos 5", .85, ACCENT, "85%"),
            ("主流群體", .27, RED, "17–36%")]
    for i, (label, value, color, pct) in enumerate(rows):
        y = top + i * row_gap
        a.text((b.x + 16, y + 13), label, 18 if wide else 19, MUTED, "lm", True)
        a.rounded(Box(bar_x, y, bar_w, 25 if wide else 31), 13, INK_PALE)
        a.rounded(Box(bar_x, y, bar_w * value, 25 if wide else 31), 13, color)
        a.text((b.right - 12, y + (12 if wide else 15)), pct, 18, color, "rm", True)
    marker_x = bar_x + bar_w * .36
    a.line([(marker_x, top + row_gap * 2 - 8),
            (marker_x, top + row_gap * 2 + (37 if wide else 47))], RED, 2)
    a.polygon([(marker_x - 7, top + row_gap * 2 - 8),
               (marker_x + 7, top + row_gap * 2 - 8),
               (marker_x, top + row_gap * 2 + 2)], RED)
    if not wide:
        a.text((marker_x, top + row_gap * 2 + 42), "真相沉沒線", 14, RED, "ma", True)


def draw_lie_filter(a: Artboard, b: Box):
    panel_title(a, b, "說謊斥候：矛盾偵測過濾", "40% 謊言")
    wide = b.w / b.h > 3
    cy = b.y + b.h * (.63 if wide else .59)
    left = b.x + 50
    draw_agent(a, left, cy, 22, RED)
    a.text((left, cy + 34), "斥候", 15, MUTED, "ma")
    lie_x = b.x + b.w * (.34 if wide else .31)
    a.rounded(Box(lie_x - 56, cy - 33, 112, 66), 14, RED_PALE, RED, 2)
    a.text((lie_x, cy - 7), "40%", 25, RED, "mm", True)
    a.text((lie_x, cy + 19), "謊言", 15, RED, "mm")
    filter_x = b.x + b.w * (.62 if wide else .61)
    a.polygon([(filter_x - 38, cy - 42), (filter_x + 38, cy - 42),
               (filter_x + 25, cy + 20), (filter_x, cy + 43),
               (filter_x - 25, cy + 20)], GREEN_PALE, GREEN)
    a.text((filter_x, cy - 7), "矛盾", 18, GREEN, "mm", True)
    a.text((filter_x, cy + 17), "偵測", 16, GREEN, "mm")
    out_x = b.right - 58
    a.ellipse(Box(out_x - 28, cy - 28, 56, 56), GREEN_PALE, GREEN, 3)
    a.line([(out_x - 13, cy), (out_x - 3, cy + 11), (out_x + 16, cy - 14)], GREEN, 5)
    a.text((out_x, cy + 38), "可信訊息", 15, GREEN, "ma", True)
    a.arrow((left + 30, cy), (lie_x - 64, cy), RED, 3, 10)
    a.arrow((lie_x + 62, cy), (filter_x - 48, cy), RED, 3, 10)
    a.arrow((filter_x + 47, cy), (out_x - 36, cy), GREEN, 3, 10)


def terminal(a: Artboard, box: Box, command: str, color=RED):
    a.rounded(box, 12, "#252525", "#3B3B3B", 2)
    a.ellipse(Box(box.x + 12, box.y + 11, 7, 7), RED)
    a.ellipse(Box(box.x + 24, box.y + 11, 7, 7), GOLD)
    a.ellipse(Box(box.x + 36, box.y + 11, 7, 7), GREEN)
    a.fit_text((box.x + 13, box.y + box.h * .62), f"> {command}", box.w - 26,
               20, 13, color, "lm", True)


def draw_process_war(a: Artboard, b: Box):
    panel_title(a, b, "進程獵殺與偽裝", "拔除 sudo")
    wide = b.w / b.h > 3
    cy = b.y + b.h * (.61 if wide else .55)
    gap = 24 if wide else 18
    margin = 15
    w = (b.w - margin * 2 - gap * 2) / 3
    h = 68 if wide else 88
    boxes = [Box(b.x + margin + i * (w + gap), cy - h / 2, w, h) for i in range(3)]
    terminal(a, boxes[0], "pkill / reaper", RED)
    node(a, boxes[1], '偽裝「typescript」', "健康檢查", ACCENT_PALE, ACCENT, title_size=18)
    node(a, boxes[2], "sudo 被拔除", "對手失權", RED_PALE, RED, title_size=19)
    a.arrow((boxes[0].right + 3, cy), (boxes[1].x - 5, cy), RED, 3, 9)
    a.arrow((boxes[1].right + 3, cy), (boxes[2].x - 5, cy), RED, 3, 9)
    if not wide:
        tx = boxes[0].x + boxes[0].w / 2
        ty = boxes[0].bottom + 31
        a.ellipse(Box(tx - 20, ty - 20, 40, 40), None, RED, 2)
        a.line([(tx - 28, ty), (tx + 28, ty)], RED, 2)
        a.line([(tx, ty - 28), (tx, ty + 28)], RED, 2)


def draw_bakeoff(a: Artboard, b: Box):
    panel_title(a, b, "談判奪權：Metric Shopping", "Rust 偏袒指標")
    wide = b.w / b.h > 3
    cy = b.y + b.h * (.62 if wide else .58)
    margin = 14
    gap = 22 if wide else 16
    labels = [("Mythos 5", "提案"), ("Bake-off", "效能競賽"),
              ("Rust 指標", "挑選偏袒"), ("主導權", "WIN")]
    w = (b.w - margin * 2 - gap * 3) / 4
    h = 68 if wide else 88
    for i, (title, sub) in enumerate(labels):
        x = b.x + margin + i * (w + gap)
        tone = GREEN_PALE if i == 3 else (ACCENT_PALE if i in (1, 2) else CARD)
        border = GREEN if i == 3 else ACCENT
        node(a, Box(x, cy - h / 2, w, h), title, sub, tone, border, title_size=18 if wide else 19)
        if i < 3:
            a.arrow((x + w + 3, cy), (x + w + gap - 5, cy), ACCENT, 3, 8)
    last_x = b.x + margin + 3 * (w + gap) + w / 2
    crown_y = cy - h / 2 - 13
    a.polygon([(last_x - 24, crown_y), (last_x - 13, crown_y - 18),
               (last_x, crown_y - 4), (last_x + 13, crown_y - 18),
               (last_x + 24, crown_y), (last_x + 19, crown_y + 9),
               (last_x - 19, crown_y + 9)], GOLD, "#9A6717")


SECTIONS: list[tuple[str, str, Callable, Callable]] = [
    ("01", "協同陷阱", draw_collab_chart, draw_collab_flow),
    ("02", "同質化合謀", draw_cartel, draw_queue),
    ("03", "認識論脆弱", draw_accuracy, draw_lie_filter),
    ("04", "地盤爭奪戰", draw_process_war, draw_bakeoff),
]


def draw_header(a: Artboard, portrait=False):
    pad = 60 if portrait else 75
    badge = Box(pad, 39 if portrait else 35, 390 if portrait else 430, 43)
    a.rounded(badge, 22, ACCENT_PALE)
    a.ellipse(Box(badge.x + 18, badge.y + 16, 10, 10), ACCENT)
    a.text((badge.x + 40, badge.y + badge.h / 2), "ANTHROPIC FRONTIER RED TEAM · 研究全覽",
           18 if portrait else 20, ACCENT_DARK, "lm", True)
    if portrait:
        a.text((pad, 112), "多代理系統", 58, TEXT, bold=True)
        a.text((pad, 176), "四大群體風險｜一圖看懂", 31, ACCENT_DARK, bold=True)
        a.text((a.width - pad, 184), "9:16 MOBILE", 16, SOFT, "ra", True)
    else:
        a.text((pad, 99), "多代理系統：智能愈強，群體風險愈難預測", 50, TEXT, bold=True)
        a.text((pad, 171), "從協作塌陷、默契卡特爾到進程獵殺——四組實驗的視覺化證據",
               25, MUTED)
        a.text((a.width - pad, 73), "MULTIAGENT SYSTEMS · 01—04", 17, SOFT, "ra", True)
    a.line([(pad, 230 if portrait else 216), (a.width - pad, 230 if portrait else 216)], BORDER, 2)


def draw_card(a: Artboard, box: Box, number: str, title: str,
              left_fn: Callable, right_fn: Callable, portrait=False):
    a.shadow(box, 22, 11, 6, 18)
    a.rounded(box, 23, CARD, BORDER, 2)
    a.rounded(Box(box.x, box.y + 20, 7, box.h - 40), 4, ACCENT)
    a.rounded(Box(box.x + 27, box.y + 20, 54, 43), 13, ACCENT_PALE)
    a.text((box.x + 54, box.y + 42), number, 21, ACCENT_DARK, "mm", True)
    a.text((box.x + 97, box.y + 41), title, 29 if portrait else 31, TEXT, "lm", True)
    descriptors = {"01": "合併崩潰 → 檔案割據", "02": "價格卡特爾 → 佇列塞車",
                   "03": "真相沉沒 → 謊言過濾", "04": "惡意對抗 → 指標政治"}
    a.text((box.right - 24, box.y + 42), descriptors[number], 17, MUTED, "rm", True)
    a.line([(box.x + 25, box.y + 77), (box.right - 25, box.y + 77)], BORDER, 2)

    if portrait:
        gap = 13
        ph = (box.h - 102 - gap) / 2
        panels = [Box(box.x + 24, box.y + 88, box.w - 48, ph),
                  Box(box.x + 24, box.y + 88 + ph + gap, box.w - 48, ph)]
    else:
        gap = 18
        pw = (box.w - 48 - gap) / 2
        panels = [Box(box.x + 24, box.y + 91, pw, box.h - 115),
                  Box(box.x + 24 + pw + gap, box.y + 91, pw, box.h - 115)]
    for p in panels:
        a.rounded(p, 18, "#FCFBFA", BORDER, 2)
    left_fn(a, panels[0])
    right_fn(a, panels[1])


def draw_footer(a: Artboard, portrait=False):
    if portrait:
        box = Box(56, 2241, 1238, 111)
        a.rounded(box, 22, ACCENT_PALE, "#E7C9BE", 2)
        a.ellipse(Box(box.x + 25, box.y + 29, 52, 52), CARD, ACCENT, 3)
        a.text((box.x + 51, box.y + 55), "!", 28, ACCENT_DARK, "mm", True)
        a.text((box.x + 96, box.y + 31), "核心啟示", 21, ACCENT_DARK, bold=True)
        a.text((box.x + 96, box.y + 63), "安全邊界不只在模型權重，更在多代理交互的協議與機制。",
               22, TEXT, bold=True)
        a.text((a.width - 57, 2382), "RESEARCH OVERVIEW · 2026", 14, SOFT, "ra", True)
    else:
        box = Box(70, 1260, 2260, 63)
        a.rounded(box, 18, ACCENT_PALE, "#E7C9BE", 2)
        a.text((box.x + 24, box.y + box.h / 2), "核心啟示", 21, ACCENT_DARK, "lm", True)
        a.line([(box.x + 136, box.y + 15), (box.x + 136, box.bottom - 15)], "#D6AA9B", 2)
        a.text((box.x + 158, box.y + box.h / 2),
               "安全邊界不只在模型權重，更在多代理交互的協議與機制設計。",
               22, TEXT, "lm", True)
        a.text((box.right - 22, box.y + box.h / 2), "ANTHROPIC FRONTIER RED TEAM",
               14, SOFT, "rm", True)


def render_landscape(path: Path):
    a = Artboard(2400, 1350)
    a.ellipse(Box(2225, -120, 310, 310), "#F0E4DE")
    a.ellipse(Box(-125, 1180, 240, 240), "#F2E9E4")
    draw_header(a, portrait=False)
    cards = [Box(70, 244, 1112, 478), Box(1218, 244, 1112, 478),
             Box(70, 750, 1112, 478), Box(1218, 750, 1112, 478)]
    for box, section in zip(cards, SECTIONS):
        draw_card(a, box, *section, portrait=False)
    draw_footer(a, portrait=False)
    return a.save(path)


def render_portrait(path: Path):
    a = Artboard(1350, 2400)
    a.ellipse(Box(1170, -95, 250, 250), "#F0E4DE")
    a.ellipse(Box(-100, 2180, 230, 230), "#F2E9E4")
    draw_header(a, portrait=True)
    cards = [Box(56, 258 + i * 490, 1238, 468) for i in range(4)]
    for box, section in zip(cards, SECTIONS):
        draw_card(a, box, *section, portrait=True)
    draw_footer(a, portrait=True)
    return a.save(path)


def validate(path: Path, expected: tuple[int, int]):
    with Image.open(path) as im:
        im.verify()
    with Image.open(path) as im:
        if im.size != expected or im.format != "PNG":
            raise RuntimeError(f"Invalid output {path}: {im.format} {im.size}")
        return path.stat().st_size


def main():
    outputs = [(ASSETS / "summary-overview.png", (2400, 1350), render_landscape),
               (ASSETS / "summary-overview-mobile.png", (1350, 2400), render_portrait)]
    for path, expected, renderer in outputs:
        renderer(path)
        size = validate(path, expected)
        print(f"OK  {path.relative_to(ROOT)}  {expected[0]}x{expected[1]}  {size / 1024:.1f} KiB")


if __name__ == "__main__":
    main()
