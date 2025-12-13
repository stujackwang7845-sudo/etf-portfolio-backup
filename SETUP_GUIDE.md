# Google Drive API 設定詳細指南

## 步驟 1：建立 Google Cloud 專案

1. 前往 [Google Cloud Console](https://console.cloud.google.com/)
2. 點擊頂部的專案選擇器
3. 點擊 "New Project"（新增專案）
4. 專案名稱：`ETF Portfolio Backup`
5. 點擊 "Create"（建立）

## 步驟 2：啟用 Google Drive API

1. 在專案中，點擊左側選單的 "APIs & Services" → "Library"
2. 搜尋 "Google Drive API"
3. 點擊進入，然後點擊 "Enable"（啟用）

## 步驟 3：建立服務帳號

1. 左側選單點擊 "APIs & Services" → "Credentials"
2. 點擊頂部 "Create Credentials" → "Service account"
3. 服務帳號名稱：`etf-backup-service`
4. 點擊 "Create and Continue"
5. 角色設定可以跳過，直接點擊 "Done"

## 步驟 4：建立金鑰

1. 在 Credentials 頁面，找到剛建立的服務帳號
2. 點擊服務帳號進入詳細頁面
3. 點擊頂部 "Keys" 標籤
4. 點擊 "Add Key" → "Create new key"
5. 選擇 "JSON" 格式
6. 點擊 "Create"
7. JSON 檔案會自動下載

## 步驟 5：設定 Google Drive 資料夾權限

1. 開啟您下載的 JSON 檔案
2. 複製 `client_email` 的值（類似 `xxx@xxx.iam.gserviceaccount.com`）
3. 前往您的 [Google Drive 資料夾](https://drive.google.com/drive/folders/1Wdd7hLkXVjMU6oJo47Ij4papXiw-FhLz)
4. 右鍵點擊資料夾 → "Share"（共用）
5. 貼上服務帳號的 email
6. 權限設為 "Editor"（編輯者）
7. 取消勾選 "Notify people"
8. 點擊 "Share"

## 步驟 6：設定 GitHub Secret

1. 開啟下載的 JSON 檔案
2. 複製**整個 JSON 內容**
3. 前往您的 GitHub repository
4. 點擊 "Settings" → "Secrets and variables" → "Actions"
5. 點擊 "New repository secret"
6. Name: `GOOGLE_DRIVE_CREDENTIALS`
7. Value: 貼上完整的 JSON 內容
8. 點擊 "Add secret"

## 完成！

設定完成後，GitHub Actions 就能自動上傳檔案到您的 Google Drive 了。

## JSON 檔案範例

您的 JSON 檔案應該類似：
```json
{
  "type": "service_account",
  "project_id": "your-project-id",
  "private_key_id": "...",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "etf-backup-service@your-project.iam.gserviceaccount.com",
  "client_id": "...",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  ...
}
```

## 疑難排解

**Q: 上傳失敗，權限錯誤？**  
A: 確認服務帳號的 email 已加入 Google Drive 資料夾的共用清單。

**Q: JSON 格式錯誤？**  
A: 確認複製了完整的 JSON 內容，包括開頭的 `{` 和結尾的 `}`。

**Q: 在哪裡查看服務帳號的 email？**  
A: 開啟 JSON 檔案，找到 `client_email` 欄位。
