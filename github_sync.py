"""
GitHub 同步模組 - 從 GitHub 下載最新 ETF 資料並匯入資料庫
"""
import requests
import os
from pathlib import Path
from datetime import datetime
from data_manager import DataManager
try:
    from drive_sync import GoogleDriveSync
except ImportError:
    GoogleDriveSync = None
import config


class GitHubSync:
    """從 GitHub repository 同步 ETF 資料"""
    
    def __init__(self, repo_owner="stujackwang7845-sudo", repo_name="etf-portfolio-backup"):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.api_base = f"https://api.github.com/repos/{repo_owner}/{repo_name}"
        self.raw_base = f"https://raw.githubusercontent.com/{repo_owner}/{repo_name}/main"
        
    def get_latest_files(self):
        """取得 repository 中所有 Excel 檔案列表"""
        try:
            url = f"{self.api_base}/contents/DATA"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            files = response.json()
            excel_files = [
                f for f in files 
                if f['name'].startswith('ETF_Investment_Portfolio_') 
                and f['name'].endswith('.xlsx')
            ]
            
            # 按日期排序（從檔名提取）
            excel_files.sort(key=lambda x: x['name'], reverse=True)
            
            return excel_files
            
        except Exception as e:
            print(f"❌ 取得檔案列表失敗: {e}")
            try:
                if 'response' in locals():
                    print(f"Status Code: {response.status_code}")
                    print(f"Response: {response.text[:200]}")
            except:
                pass
            return []
    
    def download_file(self, filename, save_dir=None):
        """下載單一 Excel 檔案"""
        if save_dir is None:
            save_dir = config.DATA_DIR
        
        try:
            url = f"{self.raw_base}/DATA/{filename}"
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            filepath = save_dir / filename
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            print(f"✅ 下載成功: {filename}")
            return filepath
            
        except Exception as e:
            print(f"❌ 下載失敗 {filename}: {e}")
            return None
    
    def sync_to_database(self):
        """同步最新資料到本地資料庫"""
        print("="*60)
        print("GitHub 資料同步")
        print("="*60)
        
        # 取得 GitHub 上的檔案列表
        print("\n檢查 GitHub repository...")
        github_files = self.get_latest_files()
        
        if not github_files:
            print("⚠️  GitHub repository 沒有找到資料檔案，將嘗試備援方案")

        
        print(f"找到 {len(github_files)} 個檔案")
        
        # 取得本地資料庫已有的日期
        manager = DataManager()
        existing_dates = set(manager.get_all_dates())
        
        # 檢查並下載新檔案
        downloaded = 0
        skipped = 0
        
        for file_info in github_files:
            filename = file_info['name']
            
            # 從檔名提取日期
            date_str = filename.replace('ETF_Investment_Portfolio_', '').replace('.xlsx', '')
            date = f"{date_str[:4]}/{date_str[4:6]}/{date_str[6:8]}"
            
            # 檢查是否已存在
            if date in existing_dates:
                skipped += 1
                continue
            
            # 下載檔案
            print(f"\n下載新資料: {filename}")
            filepath = self.download_file(filename)
            
            if filepath:
                # 匯入資料庫（使用現有的 import_historical_data 邏輯）
                try:
                    from import_historical_data import parse_excel_file
                    portfolio_data = parse_excel_file(str(filepath))
                    
                    # 1. 儲存持股資料
                    manager._save_to_database(portfolio_data['date'], portfolio_data['holdings'])
                    
                    # 2. 儲存資產配置 (基金統計資料)
                    if 'asset_allocation' in portfolio_data:
                        manager.save_fund_statistics(portfolio_data['date'], portfolio_data['asset_allocation'])
                    
                    downloaded += 1
                    print(f"  ✅ 已匯入資料庫: {date}")
                except Exception as e:
                    print(f"  ❌ 匯入失敗: {e}")
        
        # 顯示結果
        print("\n" + "="*60)
        print(f"同步完成！")
        print(f"  新增: {downloaded} 個日期")
        print(f"  跳過: {skipped} 個日期（已存在）")
        print(f"  資料庫總計: {len(manager.get_all_dates())} 個日期")
        print("="*60)
        
        if downloaded == 0 and GoogleDriveSync:
            print("\nGitHub 未發現新資料或下載失敗，嘗試使用 Google Drive 備援...")
            try:
                drive_sync = GoogleDriveSync()
                return drive_sync.sync_to_database()
            except Exception as e:
                print(f"備援同步失敗: {e}")
                
        return downloaded > 0


if __name__ == '__main__':
    sync = GitHubSync()
    sync.sync_to_database()
