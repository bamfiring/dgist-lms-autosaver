# ===== Gemini AI 요약 =====
import os
import time
from google import genai
from google.genai import types
from config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

def summarize_file(file_path, file_name):
    try:
        ext = os.path.splitext(file_name)[1].lower()

        if ext in ['.pdf', '.txt', '.md']:
            with open(file_path, 'rb') as f:
                file_data = f.read()

            # Rate limit 방지: 요청 전 대기
            time.sleep(10)

            if ext == '.pdf':
                response = client.models.generate_content(
                    model='gemini-2.0-flash',
                    contents=[
                        types.Part.from_bytes(data=file_data, mime_type='application/pdf'),
                        "이 파일의 핵심 내용을 한국어로 3줄로 요약해줘."
                    ]
                )
            else:
                text = file_data.decode('utf-8', errors='ignore')
                response = client.models.generate_content(
                    model='gemini-2.0-flash',
                    contents=f"이 파일의 핵심 내용을 한국어로 3줄로 요약해줘:\n\n{text[:2000]}"
                )
            return response.text

        elif ext in ['.pptx', '.docx']:
            return f"📎 {file_name}\n→ PPT/Word 파일은 Google Drive에서 확인하세요."
        else:
            return f"📎 {file_name}\n→ Google Drive에 업로드 완료!"

    except Exception as e:
        print(f"AI 요약 실패: {e}")
        return f"📎 {file_name}\n→ Drive에 업로드됨 (요약 생략)"