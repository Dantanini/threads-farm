# threads-farm — 脆脆找菜

## 專案資訊
- 台灣小農農產品搜尋平台
- 純靜態網頁，部署在 GitHub Pages
- repo: github.com/Dantanini/threads-farm-

## Git Flow
- `main` = 上線版本（GitHub Pages 部署）
- `develop` = 暫存測試
- `feature/xxx` = 功能分支

流程：
1. 從 develop 開 feature branch
2. 改完 commit + push
3. 開 PR 到 develop，通知主宰大人 review
4. 主宰大人 approve 後 merge 到 develop
5. develop 穩定後，主宰大人決定 merge 到 main 上線

不可直接 push 到 main 或 develop。

## Push 前必做
1. `git diff` 檢查所有變更內容
2. 確認沒有機敏資訊（token、password、secret、API key、bot token、chat ID、私人資料）
3. 有疑慮就停下來問主宰大人

## 不可上傳的內容
- `.env` 或任何環境變數檔
- API token / bot token / secret key
- 私人 chat ID、user ID
- `settings.local.json`
- 任何包含密碼或認證資訊的檔案
