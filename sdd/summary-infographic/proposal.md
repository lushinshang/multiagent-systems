# 提案：使用 codex exec 建立全覽資訊圖表並設定 LINE/社群預覽卡片

## 為什麼做

為了讓讀者能在 30 秒內掌握整篇論文的核心洞察，並在 LINE、Facebook 等社群軟體分享連結時顯示吸睛的預覽卡片（Rich Link Preview），需透過 `codex exec` 繪製一張「一圖看懂」的繁體中文全覽圖（Summary Infographic），放置於 `index.html` 頂端，並同步設定 Open Graph (`og:image`) 標籤。

## 要改什麼

- **使用 codex exec 產出全覽資訊圖**：
  - 產出高解析度圖檔 `assets/summary-overview.png`（尺寸建議 1200×675 或 16:9，最適配 LINE/FB 預覽與網頁首圖）。
  - 圖表內容提煉 4 大核心板塊：
    1. 協同陷阱（PR 合併塌陷 vs 檔案割據）
    2. 同質化合謀（價格卡特爾 vs 自發 DDoS）
    3. 認識論脆弱（盲從假情報 vs 關鍵真相沉沒）
    4. 地盤爭奪戰（惡意程式獵殺 vs 自利政治協商）
- **整合至 `index.html` 頂端**：
  - 在頁首標題下方加入精美的全覽圖 `<figure>` 區塊，支援點擊放大（Lightbox）。
  - 設定完整的 Open Graph 與 Twitter Card meta 標籤（包含 `og:image` 指向 `https://lushinshang.github.io/multiagent-systems/assets/summary-overview.png`），確保在 LINE 聊天室中能直接抓取該全覽圖作為預覽封面。
- **重新驗證並更新 GitHub Pages**。

## 影響範圍

| 檔案 | 動作 | 說明 |
|------|------|------|
| `assets/summary-overview.png` | 新增 | 全覽資訊圖（一圖看懂 / LINE 預覽圖） |
| `index.html` | 修改 | 頂端置入全覽圖並補齊 `og:image` 等社群 Meta 標籤 |
| `sdd/summary-infographic/proposal.md` | 新增 | 本次需求之提案規格書 |
| `sdd/summary-infographic/tasks.md` | 新增 | 本次需求之任務拆解清單 |
