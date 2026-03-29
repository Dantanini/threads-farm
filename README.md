# 脆脆找菜 🥬

台灣小農農產品搜尋平台 — 把 Threads 上零散的小農資訊整理成可搜尋、可比較的清單。

**Live:** https://dantanini.github.io/threads-farm-/

## 為什麼做這個

Threads 上有很多台灣小農在賣菜，但資訊散落在各個帖文裡，一滑就掉，想找特定的菜或比價很困難。已經有人在整理（像脆菜市場），但都是帖文形式，還是不能搜尋。

這個專案把這些資訊結構化，讓消費者可以：
- 搜品項（櫛瓜、蒜頭、地瓜...）
- 篩地區（南投、雲林、屏東...）
- 比價格
- 看最低購買量
- 看認證標示（產銷履歷、農藥未檢出等）

## 架構

```
threads-farm-/
├── index.html          # 單頁應用（搜尋 + 回報/檢舉）
├── data/
│   └── farmers.json    # 小農資料（與 UI 分離）
├── .github/
│   └── workflows/
│       └── validate.yml  # CI：JSON 格式驗證 + 機敏資訊掃描
├── .claude/
│   └── CLAUDE.md       # AI 協作規範
└── .gitignore
```

**刻意簡單的技術選擇：**
- 純靜態 HTML + JS，沒有 framework、沒有 build tool
- 資料存在 `data/farmers.json`，UI 動態載入
- 部署在 GitHub Pages，零成本
- 回報/檢舉透過 Google Form 收集，不需要後端

## 資料來源

1. **Threads 公開帖文** — 爬蟲（Python + Playwright）抓取整理帖和留言區自薦
2. **手動收集** — 從 Threads 上的小農帖文整理品項、價格、認證資訊
3. **小農自行回報** — 透過 Google Form 補充或更正資料

## 開發流程

- `main` — 上線版本（GitHub Pages 自動部署）
- `develop` — 測試暫存
- `feature/*` — 功能分支

所有變更走 PR，CI 自動驗證 JSON 格式和機敏資訊掃描。

## 新增小農資料

編輯 `data/farmers.json`，每筆資料格式：

```json
{
  "handle": "@threads_handle",
  "name": "農場名稱",
  "product": "品項",
  "region": "產地",
  "price": "價格資訊",
  "buy": "購買方式",
  "cert": "認證標示",
  "min": "最低購買量"
}
```

## 免責聲明

本平台僅提供資訊彙整，不為任何賣家身份或品質背書。資料來自公開帖文及小農自行提供，實際品項、價格及供貨狀況請向賣家確認。
