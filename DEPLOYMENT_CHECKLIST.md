# GitHub Actions 自動化備份系統 - 部署完成指南

## 專案概述

成功建立 GitHub Actions 自動化系統，每週一至五 17:30 自動擷取 ETF 資料並上傳到 Google Drive。

---

## 已建立的檔案

### 1. `.github/workflows/daily_fetch.yml`
GitHub Actions 工作流程設定：
- 排程：週一至五 UTC 09:30（台北 17:30）
- 執行環境：Ubuntu + Python 3.11 + Chrome
- 自動上傳到您的 Google Drive 資料夾

### 2. `fetch_and_save.py`
獨立的資料擷取腳本：
- 使用 Selenium 擷取 ETF 資料
- 自動偵測資料日期
- 產生標準 Excel 格式
- 適合在 GitHub Actions 環境執行

### 3. `requirements.txt`
最小化相依套件：
- `selenium` - 網頁自動化
- `openpyxl` - Excel 檔案處理

### 4. `README_GITHUB.md`
專案說明文件

### 5. `SETUP_GUIDE.md`
Google Drive API 詳細設定指南

---

## 部署步驟

### 第一步：建立 GitHub Repository

1. 前往 https://github.com/new
2. Repository name: `etf-portfolio-backup`
3. 設為 **Private**（重要！）
4. 點擊 "Create repository"

### 第二步：上傳檔案

**方法 A：使用 GitHub 網頁介面**

1. 在新建的 repository 頁面
2. 點擊 "uploading an existing file"
3. 上傳以下檔案：
   - `.github/workflows/daily_fetch.yml`
   - `fetch_and_save.py`
   - `requirements.txt`
   - `README_GITHUB.md`
   - `SETUP_GUIDE.md`

**方法 B：使用 Git 命令**

```bash
cd "e:\Vibe Coding\etf\981a"
git init
git add .github fetch_and_save.py requirements.txt README_GITHUB.md SETUP_GUIDE.md
git commit -m "Initial commit: GitHub Actions automation"
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/etf-portfolio-backup.git
git branch -M main
git push -u origin main
```

### 第三步：設定 Google Drive API

詳細步驟請參考 `SETUP_GUIDE.md`：

**快速摘要：**
1. 建立 Google Cloud 專案
2. 啟用 Google Drive API
3. 建立服務帳號
4. 下載 JSON 金鑰
5. 將服務帳號 email 加入您的 [Google Drive 資料夾](https://drive.google.com/drive/folders/1Wdd7hLkXVjMU6oJo47Ij4papXiw-FhLz)

### 第四步：設定 GitHub Secret

1. 在 repository 頁面，點擊 "Settings"
2. 左側選單：Secrets and variables → Actions
3. 新增 Secret：
   - Name: `GOOGLE_DRIVE_CREDENTIALS`
   - Value: 完整的 JSON 內容
4. 儲存

### 第五步：測試執行

1. 點擊 "Actions" 標籤
2. 左側選擇 "Daily ETF Portfolio Fetch"
3. 點擊 "Run workflow" → "Run workflow"
4. 等待 2-3 分鐘
5. 檢查執行結果
6. 確認 Google Drive 有新檔案

---

## 自動執行排程

設定完成後，系統會自動在：
- **每週一**：09:30 UTC（17:30 台北時間）
- **每週二**：09:30 UTC（17:30 台北時間）
- **每週三**：09:30 UTC（17:30 台北時間）
- **每週四**：09:30 UTC（17:30 台北時間）
- **每週五**：09:30 UTC（17:30 台北時間）

執行以下動作：
1. 擷取最新 ETF 投資組合資料
2. 產生 Excel 檔案
3. 自動上傳到 Google Drive
4. 記錄執行結果

---

## 本地應用程式整合

下一步：修改本地 `main.py`，啟動時自動從 Google Drive 同步資料。

將在下一階段實作：
- 檢查 Google Drive 新檔案
- 自動下載並匯入資料庫
- 顯示同步狀態

---

## 監控與維護

### 查看執行記錄
1. GitHub repository → Actions
2. 查看每次執行的詳細日誌
3. 綠色勾勾 = 成功，紅色叉叉 = 失敗

### 手動執行
1. Actions → Daily ETF Portfolio Fetch
2. Run workflow → Run workflow

### 修改執行時間
編輯 `.github/workflows/daily_fetch.yml`：
```yaml
cron: '30 9 * * 1-5'  # UTC 時間
# 台北時間 = UTC + 8
```

---

## 費用說明

<function_calls>
<invoke name="write_to_file">
<parameter name="CodeContent"># GitHub Actions 部署檢查清單

## ✅ 已完成

- [x] 建立 `.github/workflows/daily_fetch.yml`
- [x] 建立 `fetch_and_save.py`
- [x] 更新 `requirements.txt`
- [x] 建立 `README_GITHUB.md`
- [x] 建立 `SETUP_GUIDE.md`

## 📋 待完成（需要您操作）

### 1. GitHub Repository
- [ ] 建立 GitHub repository（名稱：`etf-portfolio-backup`）
- [ ] 設為 Private
- [ ] 上傳所有檔案

### 2. Google Drive API
- [ ] 建立 Google Cloud 專案
- [ ] 啟用 Google Drive API
- [ ] 建立服務帳號
- [ ] 下載 JSON 金鑰
- [ ] 將服務帳號加入 Google Drive 資料夾

### 3. GitHub Secrets
- [ ] 設定 `GOOGLE_DRIVE_CREDENTIALS` secret

### 4. 測試
- [ ] 手動執行 workflow
- [ ] 確認 Google Drive 有檔案
- [ ] 檢查執行日誌

## 📁 要上傳的檔案

從 `e:\Vibe Coding\etf\981a` 上傳：
```
.github/workflows/daily_fetch.yml
fetch_and_save.py
requirements.txt
README_GITHUB.md
SETUP_GUIDE.md
```

## 🔗 重要連結

- GitHub: https://github.com/new
- Google Cloud Console: https://console.cloud.google.com/
- Google Drive 資料夾: https://drive.google.com/drive/folders/1Wdd7hLkXVjMU6oJo47Ij4papXiw-FhLz

## ⏰ 執行時間

週一至五 台北時間 17:30

## 📊 預期結果

每天會在 Google Drive 產生：
`ETF_Investment_Portfolio_YYYYMMDD.xlsx`

## 🆘 需要協助？

參考 `SETUP_GUIDE.md` 的詳細步驟
