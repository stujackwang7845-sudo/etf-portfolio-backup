# ETF 投資組合自動備份 - GitHub Actions

## 專案說明

此專案使用 **GitHub Actions** 每週一至五自動擷取 ETF 投資組合資料並上傳到 Google Drive，即使您的電腦關機也能正常運作。

## 功能特色

✅ **完全自動化** - 每週一至五 17:30 自動執行  
✅ **雲端運行** - 在 GitHub 伺服器上執行，無需本地電腦  
✅ **自動備份** - 直接上傳到 Google Drive  
✅ **完全免費** - 使用 GitHub Actions 免費額度

## 快速開始

### 1. 建立 GitHub Repository

1. 登入 [GitHub](https://github.com)
2. 點擊右上角 "+" → "New repository"
3. Repository name: `etf-portfolio-backup`
4. 設為 **Private**
5. 點擊 "Create repository"

### 2. 上傳程式碼

將以下檔案上傳到 repository：
```
.github/workflows/daily_fetch.yml
fetch_and_save.py
requirements.txt
README.md (本檔案)
SETUP_GUIDE.md
```

### 3. 設定 Google Drive 憑證

**方法 A：使用 Google Drive API（推薦）**

1. 前往 [Google Cloud Console](https://console.cloud.google.com/)
2. 建立新專案
3. 啟用 Google Drive API
4. 建立服務帳號
5. 下載 JSON 金鑰檔案
6. 將整個 JSON 內容複製

**方法 B：使用 rclone**

詳見 `SETUP_GUIDE.md`

### 4. 設定 GitHub Secrets

1. 在 GitHub repository，點擊 "Settings"
2. 左側選單點擊 "Secrets and variables" → "Actions"
3. 點擊 "New repository secret"
4. Name: `GOOGLE_DRIVE_CREDENTIALS`
5. Value: 貼上 JSON 憑證內容
6. 點擊 "Add secret"

### 5. 測試執行

1. 在 repository，點擊 "Actions"
2. 左側選擇 "Daily ETF Portfolio Fetch"
3. 點擊 "Run workflow" → "Run workflow"
4. 等待約 2-3 分鐘
5. 檢查 Google Drive 是否有新檔案

## 自動排程

設定完成後，GitHub Actions 會自動在：
- **每週一至五**
- **台北時間 17:30**（收盤後）
- 自動執行擷取並上傳

## 檔案結構

```
etf-portfolio-backup/
├── .github/
│   └── workflows/
│       └── daily_fetch.yml          # GitHub Actions 設定
├── fetch_and_save.py                # 資料擷取腳本
├── requirements.txt                 # Python 套件
├── README.md                        # 本檔案
├── SETUP_GUIDE.md                   # 詳細設定指南
└── ETF_Investment_Portfolio_*.xlsx  # 產生的資料檔案
```

## 本地同步

在本地電腦的應用程式啟動時，會自動從 Google Drive 同步最新資料。

## 疑難排解

**Q: GitHub Actions 執行失敗？**  
A: 檢查 Actions 頁面的執行記錄，查看錯誤訊息。

**Q: 檔案沒有上傳到 Google Drive？**  
A: 確認 `GOOGLE_DRIVE_CREDENTIALS` 設定正確，並且服務帳號有資料夾存取權限。

**Q: 如何修改執行時間？**  
A: 編輯 `.github/workflows/daily_fetch.yml` 中的 `cron` 設定。

## 進階設定

- **修改執行時間**: 編輯 workflow 的 cron 設定
- **手動執行**: 在 Actions 頁面點擊 "Run workflow"
- **查看執行記錄**: Actions 頁面有完整的執行日誌

## 授權

僅供個人使用。
