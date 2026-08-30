# 提案：分析 Anthropic 研究原文、Business Insider 報導與本導讀之關聯性

## 為什麼做

使用者詢問兩篇網址（Anthropic 官方研究文章與 Business Insider 新聞報導）與本導讀（`multiagent-systems.md` 及 `index.html`）之間的相互關聯。為了提供清晰、具結構化因果鏈與事實佐證的解答，需針對兩份來源文件進行源頭比對、引用鏈分析與報導切角比較。

## 要改什麼

- 爬梳並比對兩篇 URL 的發布背景、時間軸與內容本體：
  1. `https://www.anthropic.com/research/multiagent-systems`（Anthropic 官方第一手論文原文，發布於 2026-08-13）。
  2. `https://www.businessinsider.com/anthropic-ai-agents-sabotage-each-other-turf-war-2026-8`（Business Insider 於 2026-08-14 發布的科技媒體編譯報導）。
- 梳理兩者與本專案導讀（`multiagent-systems.md` / `index.html`）的映射關係：
  - 本導讀是以 Anthropic 官方論文為「第一手原始研究素材」。
  - Business Insider 報導則是科技外媒針對該篇論文中「地盤爭奪戰（Turf war）」與「互相破壞（Sabotage）」章節所做的「二手重點摘要報導」。
- 產出結構化的關聯分析報告與架構對照圖（Mermaid）。

## 影響範圍

| 檔案 | 動作 | 說明 |
|------|------|------|
| `sdd/compare-articles-relation/proposal.md` | 新增 | 本次分析之提案規格書 |
| `sdd/compare-articles-relation/tasks.md` | 新增 | 本次分析之任務拆解清單 |
