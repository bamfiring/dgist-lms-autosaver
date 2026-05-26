# DGIST LMS AutoSaver 📚

DGIST LMS의 강의 자료를 자동으로 Google Drive에 정리해주는 프로그램입니다.

## 기능
- LMS 자동 로그인 및 파일 탐색
- 강의별, 주차별 폴더 자동 분류
- Google Drive 자동 업로드
- 공지사항 첨부파일 자동 저장
- 새 파일 업로드 시 이메일 알림
- 매일 지정한 시간에 자동 실행
- 누락 파일 검증 기능

---

## 설치 방법

### 준비물
- Windows 10/11
- DGIST LMS 아이디/비밀번호
- Google 계정 (Gmail)

---

### STEP 1. Python 설치
👉 https://www.python.org/downloads

1. "Download Python" 클릭
2. ⚠️ 설치 시 **"Add Python to PATH"** 체크 필수!
3. "Install Now" 클릭

---

### STEP 2. Git 설치
👉 https://git-scm.com

1. "Download for Windows" 클릭
2. 모든 옵션 기본값(Next)으로 진행
3. 설치 완료 후 **컴퓨터 재시작**

---

### STEP 3. 프로그램 다운로드 및 설치

PowerShell을 열고 순서대로 입력:

```powershell
git clone https://github.com/bamfiring/dgist-lms-autosaver.git
cd dgist-lms-autosaver
python setup.py
```

---

### STEP 4. setup.py 안내에 따라 설정

**① LMS 아이디/비밀번호 입력**
- lms.dgist.ac.kr 에서 직접 로그인하는 아이디/비번 입력

**② Gemini API 키 발급 (무료)**
1. https://aistudio.google.com/apikey 접속
2. Google 계정 로그인
3. "Create API Key" 클릭
4. 생성된 키 복사 (`AIza...` 로 시작)

**③ Google Drive 설정**
1. https://console.cloud.google.com 접속
2. 새 프로젝트 생성 → 이름: `LMS-AutoSaver`
3. "API 및 서비스" → "라이브러리" → `Google Drive API` 검색 → "사용"
4. "사용자 인증 정보" → "OAuth 클라이언트 ID" 만들기
   - 동의 화면 구성: User Type **"외부"**, 앱 이름 `LMS-AutoSaver`
   - 앱 유형: **"데스크톱 앱"** 선택
5. 생성된 JSON 파일 ⬇️ 다운로드
6. 파일 이름을 `credentials.json` 으로 변경
7. `dgist-lms-autosaver` 폴더에 복사
8. "OAuth 동의 화면" → "테스트 사용자" → 본인 Gmail 추가

**④ Gmail 앱 비밀번호 발급**
1. https://myaccount.google.com/apppasswords 접속
2. 앱 이름: `LMS알리미` 입력 후 "만들기"
3. 16자리 비밀번호 복사 (공백 제거)

**⑤ 자동 실행 시간 설정**
- 원하는 시간 입력 (예: `08:00`)

---

### STEP 5. 자동 실행 스케줄러 등록

setup.py 마지막에 스케줄러 등록 여부를 물어봅니다. **"y"** 입력하면 자동 등록.

수동으로 등록하려면 PowerShell을 **관리자 권한**으로 열고:

```powershell
cd dgist-lms-autosaver
.\schedule_setup.ps1 -Time 08:00AM
```

---

### STEP 6. 첫 실행

```powershell
python main.py
```

처음 실행 시 브라우저에서 Google 인증 창이 뜨면:
1. "계속" 클릭
2. Google 계정 로그인
3. "허용" 클릭

---

## 이후 사용법

- 매일 설정한 시간에 **자동으로 실행**됨
- 새 파일이 있으면 **Google Drive에 자동 저장**
- **이메일로 알림** 수신
- 수동 실행: `python main.py`

---

## Google Drive 저장 구조

```
DGIST_LMS_파일/
├── 일반화학Ⅰ/
│   ├── Assignments/
│   ├── Course Materials/
│   │   ├── Week1_Orientation&Ch1/
│   │   ├── Week2_Ch2&Ch3/
│   │   └── ...
│   ├── Quiz/
│   └── 공지사항(Announcements)/
├── 일반물리Ⅰ/
│   ├── 1주차/
│   ├── 2주차/
│   └── 공지사항(Announcements)/
├── 프로그래밍/
│   └── 공지사항(Announcements)/
└── ...
```

---

## 파일 구조

```
dgist-lms-autosaver/
├── setup.py            # 최초 1회 설정 마법사
├── main.py             # 메인 실행 파일
├── lms_crawler.py      # LMS 파일 탐색
├── drive_uploader.py   # Google Drive 업로드
├── email_notifier.py   # 이메일 알림
├── verify.py           # 누락 파일 검증
├── run.bat             # 자동 실행 배치 파일
├── schedule_setup.ps1  # 스케줄러 등록 스크립트
└── config.example.py   # 설정 파일 예시
```

---

## 주의사항
- `config.py`, `credentials.json` 은 절대 공유하지 마세요.
- 개인정보가 포함되어 있으며 `.gitignore` 에 의해 GitHub 업로드에서 자동 제외됩니다.
- 컴퓨터가 켜져 있을 때만 자동 실행됩니다.

---

## 문제 발생 시
👉 https://github.com/bamfiring/dgist-lms-autosaver/issues