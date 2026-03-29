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
├── index.html                          # 單頁應用（搜尋 + 回報/檢舉）
├── data/
│   └── farmers.json                    # 小農資料（與 UI 分離）
├── scripts/
│   ├── validate_html.py                # CI：HTML 結構驗證
│   └── verify_farmers.py               # CI：小農資料比對 Threads
├── .github/
│   ├── release-drafter.yml             # Release notes 模板
│   └── workflows/
│       ├── validate.yml                # CI：資料驗證 pipeline
│       └── release-drafter.yml         # 自動生成 release notes
├── .claude/
│   └── CLAUDE.md                       # AI 協作規範
└── .gitignore
```

**刻意簡單的技術選擇：**
- 純靜態 HTML + JS，沒有 framework、沒有 build tool
- 資料存在 `data/farmers.json`，UI 動態載入
- 部署在 GitHub Pages，零成本
- 回報/檢舉透過 Google Form 收集，不需要後端
- Google Analytics 追蹤瀏覽數據

## 資料來源

1. **Threads 公開帖文** — 爬蟲（Python + Playwright）抓取整理帖和留言區自薦
2. **手動收集** — 從 Threads 上的小農帖文整理品項、價格、認證資訊
3. **小農自行回報** — 透過 Google Form 補充或更正資料

## CI/CD

每次 PR 自動執行：

| 檢查項目 | 說明 |
|---|---|
| JSON 格式驗證 | farmers.json 語法和必要欄位檢查 |
| Handle 重複檢查 | 防止同一帳號重複收錄 |
| HTML 結構驗證 | 確認 fetch 路徑正確、UI 元素完整 |
| 資料比對 Threads | 比對變動的小農品項是否與 Threads 頁面吻合（warning，不擋 merge） |
| 機敏資訊掃描 | 防止 token、密碼等意外上傳 |

上線流程使用 [Release Drafter](https://github.com/release-drafter/release-drafter) 自動從 PR 標題生成 release notes。

## 開發流程

- `main` — 上線版本（GitHub Pages 自動部署）
- `develop` — 測試暫存
- `feature/*` — 功能分支

所有變更走 PR，CI 通過後由 maintainer review merge。

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
  "min": "最低購買量",
  "verified": "YYYY-MM-DD"
}
```

`verified` 欄位：由 maintainer 確認資料正確後標記日期。修改資料時需清除此欄位。

## 免責聲明

本平台僅提供資訊彙整，不為任何賣家身份或品質背書。資料來自公開帖文及小農自行提供，實際品項、價格及供貨狀況請向賣家確認。
