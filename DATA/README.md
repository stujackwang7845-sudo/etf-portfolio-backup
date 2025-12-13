# ETF 投資組合追蹤系統 - 完整使用指南

## 🎉 系統已完成自動化！

### ✅ 自動備份（無需人工操作）

**GitHub Actions 自動執行：**
- ⏰ **時間**：每週一至五 17:30（台北時間）
- 🤖 **完全自動**：無需電腦開機
- ☁️ **雲端執行**：在 GitHub 伺服器上運行
- 📦 **自動儲存**：直接提交到 GitHub repository

**查看自動執行記錄：**
1. 前往：https://github.com/jacksonng4885/etf-portfolio-backup
2. 點擊 "Actions" 標籤
3. 查看每次執行的歷史記錄

---

## 💻 本地應用程式使用

### 第一次啟動

1. **開啟應用程式**
   ```bash
   cd "e:\Vibe Coding\etf\981a"
   python main.py
   ```

2. **自動同步**
   - 程式啟動時會自動檢查 GitHub
   - 如有新資料會自動下載並匯入資料庫
   - 顯示同步結果

3. **查看資料**
   - 每日變化：比較最新兩天的資料
   - 日期區間分析：選擇任意兩天比較
   - 個股歷史：查看個別股票的持股趨勢

### 日常使用

**每次開啟應用程式：**
1. 自動從 GitHub 同步最新資料
2. 匯入新的日期到本地資料庫
3. 立即可以查看分析

**手動同步（選用）：**
```bash
cd "e:\Vibe Coding\etf\981a"
python github_sync.py
```

---

## 📊 功能說明

### 1. 每日變化分析
- 顯示最新一天的完整持股
- 自動比較前後兩天的變化：
  - 🆕 新增持股
  - ❌ 移除持股
  - ⬆️ 增加部位
  - ⬇️ 減少部位

### 2. 日期區間分析
- 選擇任意兩個日期比較
- 自動檢查日期有效性
- 顯示詳細的變化分析

### 3. 個股歷史追蹤
- 輸入股票代號（例如：2330）
- 顯示該股票的持股數量趨勢圖
- 可查看長期持股變化

---

## 🔄 資料流程

```
網站資料 (ezmoney.com.tw)
    ↓
GitHub Actions (週一至五 17:30 自動執行)
    ↓
擷取最新資料 → 產生 Excel
    ↓
提交到 GitHub repository
    ↓
本地應用程式啟動
    ↓
從 GitHub 下載新資料
    ↓
匯入本地 SQLite 資料庫
    ↓
在 UI 中查看分析
```

---

## 📁 資料位置

### GitHub 雲端備份
- URL: https://github.com/jacksonng4885/etf-portfolio-backup
- 所有歷史 Excel 檔案
- 完整的版本控制記錄

### 本地資料
- **Excel 檔案**：`e:\Vibe Coding\etf\981a\data\*.xlsx`
- **SQLite 資料庫**：`e:\Vibe Coding\etf\981a\data\portfolio_history.db`

---

## ⚙️ 進階操作

### 手動觸發資料擷取

如果想立即擷取最新資料：
1. 前往 GitHub repository
2. Actions → Daily ETF Portfolio Fetch
3. Run workflow → Run workflow

### 查看歷史資料

**方法 1：從 GitHub 下載**
1. 前往 repository
2. 點擊想要的 Excel 檔案
3. 點擊 "Download"

**方法 2：從本地查看**
```bash
cd "e:\Vibe Coding\etf\981a\data"
# 查看所有 Excel 檔案
dir ETF_Investment_Portfolio_*.xlsx
```

### 重新匯入所有歷史資料

如果需要重建資料庫：
```bash
cd "e:\Vibe Coding\etf\981a"
python import_historical_data.py
```

---

## 🆘 常見問題

**Q: 資料多久更新一次？**
A: 每週一至五 17:30 自動更新（台灣股市交易日）

**Q: 電腦沒開機會怎樣？**
A: 沒關係！GitHub Actions 在雲端執行，完全不需要您的電腦開機

**Q: 如何確認自動化正常運作？**
A: 
1. 查看 GitHub repository，應該每天有新的 Excel 檔案
2. 查看 Actions 頁面，應該顯示執行成功

**Q: 如果某天沒有資料怎麼辦？**
A: 
- 檢查 Actions 執行記錄
- 如果失敗，可以手動執行一次
- 本地應用程式會自動跳過缺失的日期

**Q: 資料會佔用很多空間嗎？**
A: 不會，每個 Excel 檔案約 10-20 KB，一年約 2-3 MB

---

## 📈 未來擴充

系統已經建立完整的自動化pipeline，未來可以輕鬆擴充：
- 📧 新增電子郵件通知
- 📊 更多統計分析功能
- 🔔 持股重大變化警報
- 📱 網頁版查看介面

---

## 🎊 完成！

恭喜！您的 ETF 投資組合追蹤系統已經完全自動化！

**現在您只需要：**
1. 打開應用程式
2. 自動同步最新資料
3. 查看分析結果

所有的資料擷取和備份都會在背景自動完成！📊✨
