# ===== Google Drive 업로드 =====
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/drive.file']
CREDENTIALS_PATH = r"C:\lms-autosaver\credentials.json"
TOKEN_PATH = r"C:\lms-autosaver\token.json"
ROOT_FOLDER = "DGIST_LMS_파일"

_service = None
_folder_cache = {}

def get_drive_service():
    global _service
    if _service:
        return _service
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())
    _service = build('drive', 'v3', credentials=creds)
    return _service

def get_or_create_folder(service, name, parent_id=None):
    cache_key = f"{parent_id}:{name}"
    if cache_key in _folder_cache:
        return _folder_cache[cache_key]

    query = f"name='{name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    if parent_id:
        query += f" and '{parent_id}' in parents"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get('files', [])
    if files:
        _folder_cache[cache_key] = files[0]['id']
        return files[0]['id']

    metadata = {'name': name, 'mimeType': 'application/vnd.google-apps.folder'}
    if parent_id:
        metadata['parents'] = [parent_id]
    folder = service.files().create(body=metadata, fields='id').execute()
    print(f"폴더 생성: {name}")
    _folder_cache[cache_key] = folder['id']
    return folder['id']

def file_exists_in_drive(service, file_name, folder_id):
    query = f"name='{file_name}' and '{folder_id}' in parents and trashed=false"
    results = service.files().list(q=query, fields="files(id)").execute()
    return len(results.get('files', [])) > 0

def upload_to_drive_with_path(file_path, file_name, course_name, folder_path):
    """
    folder_path: ['1주차', 'Week1_Ch1'] 같은 리스트
    Drive 구조: DGIST_LMS_파일 / 과목명 / 폴더경로... / 파일
    """
    try:
        service = get_drive_service()

        # 루트 → 과목 폴더
        root_id = get_or_create_folder(service, ROOT_FOLDER)
        course_clean = course_name.strip()[:40]
        current_id = get_or_create_folder(service, course_clean, root_id)

        # 하위 폴더 순서대로 생성
        import re

        for folder_name in folder_path:
            clean_name = folder_name.strip()[:50]
            if clean_name:
                # 숫자 앞에 0 패딩 (Week 1 → Week 01, 1주차 → 01주차)
                clean_name = re.sub(
                    r'(\b)(\d+)(\b)',
                    lambda m: m.group(1) + m.group(2).zfill(2) + m.group(3),
                    clean_name
                )
                current_id = get_or_create_folder(service, clean_name, current_id)

        # Drive에 이미 있으면 스킵
        if file_exists_in_drive(service, file_name, current_id):
            print(f"Drive에 이미 존재: {file_name}")
            return 'exists'

        file_metadata = {'name': file_name, 'parents': [current_id]}
        media = MediaFileUpload(file_path, resumable=True)
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, webViewLink'
        ).execute()

        path_str = '/'.join([course_clean] + folder_path)
        print(f"Drive 업로드 완료: {file_name} → {path_str}")
        return file.get('webViewLink', '')

    except Exception as e:
        print(f"Drive 업로드 실패 ({file_name}): {e}")
        return ''