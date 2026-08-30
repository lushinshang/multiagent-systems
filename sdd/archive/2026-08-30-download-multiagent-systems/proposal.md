# 提案：下載並轉換 Anthropic Multi-Agent Systems 研究文章為 Markdown

## 為什麼做

使用者需要將 Anthropic 發布之研究文章（`https://www.anthropic.com/research/multiagent-systems`）完整保存至本地工作目錄，內容需轉換為好閱讀的 Markdown 格式，並將網頁內含的所有圖片及影片等媒體素材下載到本地，以利離線閱讀與歸檔。

## 要改什麼

- 擷取 `https://www.anthropic.com/research/multiagent-systems` 的文章內容（包含標題、發布日期、章節內容、引用與註解）。
- 將文章內嵌的所有圖片與影片資源（如 png/jpg/webp/mp4 等）下載儲存至本地 `assets/` 資料夾。
- 將網頁內容轉換並整理為 HackMD 相容的 Markdown 文件（`multiagent-systems.md`），內嵌圖片/影片連結改為本地相對路徑。
- 檢查 Markdown 格式完整性、圖文對應正確性與本地媒體連結是否皆有效。

## 影響範圍

| 檔案 | 動作 | 說明 |
|------|------|------|
| `multiagent-systems.md` | 新增 | 轉換後的 Markdown 文章本文 |
| `assets/` | 新增 | 存放文章中下載的圖片與影片檔案 |
| `sdd/download-multiagent-systems/proposal.md` | 新增 | 本次需求之提案規格書 |
| `sdd/download-multiagent-systems/tasks.md` | 新增 | 本次需求之任務拆解與驗收清單 |
