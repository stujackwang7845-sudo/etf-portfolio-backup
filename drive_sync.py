"""
Google Drive 同步模組 - 從 Google Drive 下載最新 ETF 資料
作為 GitHub 同步的備援方案
"""
import os
import shutil
import gdown
from pathlib import Path
from datetime import datetime
from data_manager import DataManager
import config

class GoogleDriveSync:
    """從 Google Drive 同步 ETF 資料"""
    
    def __init__(self, folder_url="https://drive.google.com/drive/folders/1mK6gf2kYPA2Mkh-JqG5J197nJQ8KONOd?usp=sharing"):
        self.folder_url = folder_url
        self.temp_dir = config.BASE_DIR / "temp_drive_download"
        
    def download_files(self):
        """從 Google Drive 下載資料夾"""
        try:
            print(f"正在從 Google Drive 下載資料: {self.folder_url}")
            
            # 建立暫存目錄
            if self.temp_dir.exists():
                shutil.rmtree(self.temp_dir)
            self.temp_dir.mkdir(parents=True, exist_ok=True)
            
            # 使用 gdown 下載整個資料夾
            # --folder 參數用於下載資料夾
            # output 參數指定下載路徑
            gdown.download_folder(url=self.folder_url, output=str(self.temp_dir), quiet=False, use_cookies=False)
            
            print(f"✅ Google Drive 下載完成: {self.temp_dir}")
            return True
            
        except Exception as e:
            print(f"❌ Google Drive 下載失敗: {e}")
            return False
            
    def sync_to_database(self):
        """同步最新資料到本地資料庫"""
        print("="*60)
        print("Google Drive 資料同步 (備援)")
        print("="*60)
        
        # 下載檔案
        if not self.download_files():
            return False
            
        # 尋找所有 Excel 檔案
        excel_files = sorted(self.temp_dir.glob('**/*.xlsx'))
        
        if not excel_files:
            print("⚠️  Google Drive 中沒有找到 Excel 檔案")
            return False
            
        print(f"找到 {len(excel_files)} 個 Excel 檔案")
        
        # 取得本地資料庫已有的日期
        manager = DataManager()
        existing_dates = set(manager.get_all_dates())
        
        imported_count = 0
        skipped_count = 0
        
        from import_historical_data import parse_excel_file
        
        for filepath in excel_files:
            try:
                # 檢查檔名格式
                if not filepath.name.startswith('ETF_Investment_Portfolio_'):
                    continue
                    
                # 解析 Excel 以取得日期
                portfolio_data = parse_excel_file(str(filepath))
                date = portfolio_data['date']
                
                # 檢查是否已存在
                if date in existing_dates:
                    skipped_count += 1
                    continue
                
                print(f"\n匯入新資料: {filepath.name} ({date})")
                
                # 1. 複製檔案到 data 目錄 (保留一份副本)
                target_path = config.DATA_DIR / filepath.name
                shutil.copy2(filepath, target_path)
                print(f"  已複製到 data 目錄")
                
                # 2. 匯入資料庫
                manager._save_to_database(date, portfolio_data['holdings'])
                
                # 3. 儲存資產配置
                if 'asset_allocation' in portfolio_data:
                    manager.save_fund_statistics(date, portfolio_data['asset_allocation'])
                
                print(f"  ✅ 已匯入資料庫")
                imported_count += 1
                
            except Exception as e:
                print(f"  ❌ 處理失敗 {filepath.name}: {e}")
        
        # 清理暫存檔
        try:
            shutil.rmtree(self.temp_dir)
            print("\n已清理暫存檔案")
        except:
            pass
            
        print("\n" + "="*60)
        print(f"備援同步完成")
        print(f"  新增: {imported_count} 個日期")
        print(f"  跳過: {skipped_count} 個日期")
        print("="*60)
        
        return imported_count > 0

if __name__ == '__main__':
    drive_sync = GoogleDriveSync()
    drive_sync.sync_to_database()
