# 提案：使用 codex exec 將下載的論文圖表翻譯為繁體中文（台灣用語）

## 為什麼做

文章中所包含的 7 張研究圖表均為英文標籤與文字（例如座標軸名稱、圖例、柱狀圖標註、圖表內文等）。為了讓繁體中文讀者能更直覺理解圖表內容，需利用 `codex exec`（結合多模態/圖像編輯能力或重繪機制）將所有圖檔中的英文字詞翻譯並替換為精確的繁體中文（台灣用語）。

## 要改什麼

- 檢視 `assets/` 中的 7 張圖表（`figure-1` 至 `figure-7`）中的英文標註與文字內容。
- 使用 `codex exec` 逐一針對各圖檔進行翻譯與圖像後製處理，產出繁體中文版圖檔（命名如 `figure-1-vulnerabilities-vs-tokens-zh.png` 或替換原檔並保留備份）。
- 確保所有專有名詞符合台灣慣用詞彙（如：`Pull Request` -> `PR / 合併請求`、`Tokens` -> `Token`、`Swarm` -> `群體 / 代理群`、`Turf war` -> `地盤爭奪戰` 等）。
- 更新 `multiagent-systems.md` 中的圖檔參照或提供雙語對照配置。
- 檢查所有翻譯後圖表的清晰度與排版工整度。

## 影響範圍

| 檔案 | 動作 | 說明 |
|------|------|------|
| `assets/figure-*-zh.png` | 新增 | 繁體中文翻譯後之各張圖表 |
| `multiagent-systems.md` | 修改 | 更新圖表連結至繁體中文版圖檔（或雙語展示） |
| `sdd/translate-figures-zhtw/proposal.md` | 新增 | 本次需求之提案規格書 |
| `sdd/translate-figures-zhtw/tasks.md` | 新增 | 本次需求之任務清單與驗收條件 |
