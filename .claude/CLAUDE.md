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

## PR 規範
1. 每次修改完成後直接用 `git` 指令開 PR（沒有 gh CLI，用 push 後給連結）
2. PR 描述必須包含：
   - **修改內容**：具體改了什麼
   - **原因**：為什麼要改（如有需要）
   - **Trade-off / 優缺點**：如果有取捨決策
   - **可能風險**：如果有潛在問題
3. PR 開完後透過 Telegram 通知主宰大人，附上 PR 連結
4. 不要等主宰大人問，主動做完整個流程

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
