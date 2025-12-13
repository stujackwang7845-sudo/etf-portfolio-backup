"""
Upload Excel file to Google Drive
使用服務帳號憑證上傳檔案
"""
import os
import json
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account
import glob


def upload_to_drive():
    """上傳 Excel 檔案到 Google Drive"""
    
    # 讀取憑證
    credentials_json = os.environ.get('GOOGLE_CREDENTIALS')
    if not credentials_json:
        print("❌ 錯誤：找不到 GOOGLE_CREDENTIALS 環境變數")
        exit(1)
    
    folder_id = os.environ.get('FOLDER_ID')
    if not folder_id:
        print("❌ 錯誤：找不到 FOLDER_ID 環境變數")
        exit(1)
    
    # 寫入臨時憑證檔案
    creds_file = 'temp_credentials.json'
    try:
        with open(creds_file, 'w') as f:
            f.write(credentials_json)
        print("✅ 憑證檔案已建立")
    except Exception as e:
        print(f"❌ 無法寫入憑證檔案: {e}")
        exit(1)
    
    # 建立憑證
    try:
        credentials = service_account.Credentials.from_service_account_file(
            creds_file,
            scopes=['https://www.googleapis.com/auth/drive']  # 完整 Drive 權限
        )
        print("✅ 憑證已載入")
    except Exception as e:
        print(f"❌ 憑證載入失敗: {e}")
        if os.path.exists(creds_file):
            os.remove(creds_file)
        exit(1)
    
    # 建立 Drive API client
    service = build('drive', 'v3', credentials=credentials)
    
    # 找到所有 Excel 檔案
    excel_files = glob.glob('ETF_Investment_Portfolio_*.xlsx')
    
    if not excel_files:
        print("⚠️  找不到要上傳的 Excel 檔案")
        exit(0)
    
    print(f"找到 {len(excel_files)} 個檔案要上傳")
    
    for filepath in excel_files:
        filename = os.path.basename(filepath)
        print(f"\n上傳: {filename}")
        
        # 檢查檔案是否已存在
        query = f"name='{filename}' and '{folder_id}' in parents and trashed=false"
        results = service.files().list(q=query, fields="files(id, name)").execute()
        existing_files = results.get('files', [])
        
        if existing_files:
            # 更新現有檔案
            file_id = existing_files[0]['id']
            print(f"  檔案已存在，更新中... (ID: {file_id})")
            
            media = MediaFileUpload(filepath, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            updated_file = service.files().update(
                fileId=file_id,
                media_body=media
            ).execute()
            
            print(f"  ✅ 更新成功！")
        else:
            # 上傳新檔案
            print(f"  上傳新檔案...")
            
            file_metadata = {
                'name': filename,
                'parents': [folder_id]
            }
            
            media = MediaFileUpload(filepath, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            uploaded_file = service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, name'
            ).execute()
            
            print(f"  ✅ 上傳成功！File ID: {uploaded_file.get('id')}")
    
    print(f"\n🎉 所有檔案上傳完成！")
    
    # 清理臨時檔案
    if os.path.exists('temp_credentials.json'):
        os.remove('temp_credentials.json')
        print("🗑️  已清理臨時憑證檔案")


if __name__ == '__main__':
    upload_to_drive()

