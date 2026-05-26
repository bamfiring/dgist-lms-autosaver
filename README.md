# DGIST LMS AutoSaver 📚

DGIST LMS의 강의 자료를 자동으로 Google Drive에 정리해주는 프로그램입니다.

## 기능
- LMS 자동 로그인 및 파일 탐색
- 강의별, 주차별 폴더 자동 분류
- Google Drive 자동 업로드
- 공지사항 첨부파일 자동 저장
- 새 파일 업로드 시 이메일 알림
- 매일 지정한 시간에 자동 실행

## 설치 방법

### 필요 사항
- Windows 10/11
- Python 3.10 이상
- Google 계정
- DGIST LMS 계정

### 설치 순서

**1. 저장소 다운로드**

```
git clone https://github.com/YOUR_USERNAME/dgist-lms-autosaver.git
cd dgist-lms-autosaver
```

**2. setup.py 실행**

```
python setup.py
```

**3. 안내에 따라 설정**
- DGIST LMS 아이디/비밀번호 입력
- Gemini API 키 발급 및 입력
- Google Drive 연동 설정
- Gmail 앱 비밀번호 설정
- 자동 실행 시간 설정

**4. 프로그램 실행**

```
python main.py
```

## API 키 발급 방법

### Gemini API (무료)
1. https://aistudio.google.com/apikey 접속
2. Google 계정 로그인
3. "Create API Key" 클릭

### Google Drive API
1. https://console.cloud.google.com 접속
2. 새 프로젝트 생성 (LMS-AutoSaver)
3. Google Drive API 활성화
4. OAuth 클라이언트 ID 생성 (데스크톱 앱)
5. credentials.json 다운로드 → 프로젝트 폴더에 저장
6. Google Cloud Console → OAuth 동의 화면 → 테스트 사용자 → 본인 Gmail 추가

### Gmail 앱 비밀번호
1. https://myaccount.google.com/apppasswords 접속
2. 앱 이름 입력 후 생성
3. 16자리 비밀번호 복사 (공백 제거)

## 파일 구조

```
dgist-lms-autosaver/
├── setup.py          # 최초 1회 설정 마법사
├── main.py           # 메인 실행 파일
├── lms_crawler.py    # LMS 파일 탐색
├── drive_uploader.py # Google Drive 업로드
├── email_notifier.py # 이메일 알림
└── config.example.py # 설정 파일 예시
```

## 주의사항
- `config.py`, `credentials.json` 은 절대 공유하지 마세요.
- 개인정보가 포함되어 있습니다.
- `.gitignore` 에 의해 자동으로 GitHub 업로드에서 제외됩니다.

## 자동 실행 설정 (Windows)

setup.py 실행 시 자동으로 설정되지만, 수동으로 등록하려면:

1. PowerShell을 **관리자 권한**으로 실행
2. 아래 명령어 입력:
cd dgist-lms-autosaver
.\schedule_setup.ps1 -Time 08:00AM
- 컴퓨터가 켜져 있을 때 매일 지정한 시간에 자동 실행
- 시간 변경: `-Time 09:00AM` 처럼 원하는 시간으로 변경
