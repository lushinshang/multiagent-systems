# 提案：重構全覽圖為「高視覺化圖解（圖多於文）」並支援手機直式與桌面橫式雙版本

## 為什麼做

使用者反應現有全覽圖文字偏多，期望以「視覺圖解為核心、文字精簡為輔」，並同時支援：
1. **螢幕橫式版（16:9 Landscape）**：適用於桌面閱讀與 LINE / 社群預覽卡片。
2. **手機直式版（9:16 Portrait）**：針對手機直螢幕重新排版堆疊，讓行動讀者無須放大即可舒適閱讀全圖。

## 要改什麼

- **重構全覽圖視覺設計（圖多於文）**：
  - 核心設計理念：以具象圖解、迷你視覺圖表（Mini-charts / Visual Diagrams）、數據圖形化取代長條文字清單。
  - **板塊 1【協同陷阱】**：繪製「PR 合併瀑布塌陷圖」（876/980 PR 堆積 vs 0 合併）與「檔案割據 vs 協作共享」雙對比圖形。
  - **板塊 2【同質化合謀】**：繪製「多代理價格卡特爾環形網絡」與「每秒 30 次輪詢 DDoS 佇列塞車」示意圖形。
  - **板塊 3【認識論脆弱】**：繪製「說謊斥候濾網」與「隱藏特徵真相沉沒指標」（17%~36% vs 100% 條形對比）。
  - **板塊 4【地盤爭奪戰】**：繪製「進程獵殺惡意程式流程（pkill / reaper / 偽裝 TS）」與「Bake-off 指標政治談判」對抗圖解。
- **產出雙尺寸圖檔（使用 codex exec 繪製）**：
  - 橫式版（16:9）：`assets/summary-overview.png`（2400×1350 px）
  - 直式版（9:16）：`assets/summary-overview-mobile.png`（1350×2400 px）
- **網頁響應式 `<picture>` 整合與 Lightbox 適配**：
  - 使用 HTML5 `<picture>` 標籤，在手機窄視窗（`< 640px`）自動切換載入直式版本，桌面視窗載入橫式版本。
  - 燈箱（Lightbox）支援依當前螢幕尺寸載入對應清晰圖檔。
- **推送更新至 GitHub Pages**。

## 影響範圍

| 檔案 | 動作 | 說明 |
|------|------|------|
| `assets/summary-overview.png` | 修改 | 重繪為高視覺化橫式 16:9 全覽圖 |
| `assets/summary-overview-mobile.png` | 新增 | 針對手機直螢幕排版之直式 9:16 全覽圖 |
| `index.html` | 修改 | 採用 `<picture>` 標籤並適配雙版本與 Lightbox |
| `sdd/visual-summary-responsive/proposal.md` | 新增 | 提案規格書 |
| `sdd/visual-summary-responsive/tasks.md` | 新增 | 任務拆解清單 |
