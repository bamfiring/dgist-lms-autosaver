# ===== DGIST LMS AutoSaver 설치 마법사 =====
import os
import sys
import json
import subprocess

def print_banner():
    print("""
╔══════════════════════════════════════════════════════╗
║         DGIST LMS AutoSaver 설치 마법사              ║
║         처음 사용자를 위한 자동 설정 프로그램         ║
╚══════════════════════════════════════════════════════╝
""")

def print_step(step, title):
    print(f"\n{'='*54}")
    print(f"  STEP {step}: {title}")
    print(f"{'='*54}")

def input_with_guide(prompt, secret=False):
    """입력 받기"""
    if secret:
        print("  (입력한 내용이 보입니다. 주변을 확인하세요)")
    return input(prompt).strip()

def check_requirements():
    """필수 패키지 확인 및 설치"""
    print_step(0, "필수 패키지 설치 확인")
    packages = [
        'playwright',
        'google-auth',
        'google-auth-oauthlib',
        'google-api-python-client',
        'schedule',
        'google-genai',
        'aiohttp'
    ]
    for pkg in packages:
        print(f"  설치 확인 중: {pkg}...", end='', flush=True)
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'install', pkg, '-q'],
            capture_output=True
        )
        print(" ✅")

    print("\n  Playwright 브라우저 설치 중...")
    subprocess.run([sys.executable, '-m', 'playwright', 'install', 'chromium'], capture_output=True)
    print("  ✅ 완료!")

def get_lms_info():
    """LMS 로그인 정보 입력"""
    print_step(1, "DGIST LMS 로그인 정보")
    print("""
  LMS 로그인 정보를 입력해주세요.
  (lms.dgist.ac.kr 에서 직접 로그인하는 아이디/비밀번호)
""")
    lms_id = input_with_guide("  LMS 아이디: ")
    lms_pw = input_with_guide("  LMS 비밀번호: ", secret=True)
    return lms_id, lms_pw

def get_gemini_key():
    """Gemini API 키 입력"""
    print_step(2, "Gemini API 키 설정 (AI 요약 기능)")
    print("""
  Gemini API는 무료로 사용할 수 있습니다!

  [발급 방법]
  1. 브라우저에서 https://aistudio.google.com/apikey 접속
  2. Google 계정으로 로그인
  3. "Create API Key" 클릭
  4. 생성된 키 복사 (AIza... 로 시작)

  ⚠️  지금 브라우저에서 위 주소를 열어 키를 발급받으세요!
""")
    input("  발급 완료 후 Enter 키를 누르세요...")
    key = input_with_guide("  Gemini API 키 입력: ")
    return key

def get_google_drive_credentials():
    """Google Drive credentials.json 설정"""
    print_step(3, "Google Drive 연동 설정")
    print("""
  Google Drive에 자동으로 파일을 저장하기 위한 설정입니다.

  [설정 방법]
  1. https://console.cloud.google.com 접속 (Google 계정 로그인)
  2. 상단 "프로젝트 선택" → "새 프로젝트" 클릭
     - 프로젝트 이름: LMS-AutoSaver → "만들기"
  3. 왼쪽 메뉴 "API 및 서비스" → "라이브러리"
     - "Google Drive API" 검색 → "사용" 클릭
  4. "API 및 서비스" → "사용자 인증 정보"
     - "사용자 인증 정보 만들기" → "OAuth 클라이언트 ID"
     - (처음이면 "동의 화면 구성" 먼저: User Type "외부", 앱 이름 "LMS-AutoSaver")
     - 앱 유형: "데스크톱 앱" 선택 → "만들기"
  5. 생성된 항목 오른쪽 ⬇️ 클릭하여 JSON 다운로드
  6. 다운로드된 파일을 이 폴더(C:\\lms-autosaver)에 복사
     파일 이름을 "credentials.json" 으로 변경

  6. Google Cloud Console → "API 및 서비스" → "OAuth 동의 화면"
     → "테스트 사용자" → "ADD USERS" → 본인 Gmail 추가
""")
    input("  설정 완료 후 Enter 키를 누르세요...")

    cred_path = r"C:\lms-autosaver\credentials.json"
    while not os.path.exists(cred_path):
        print(f"\n  ❌ credentials.json 파일을 찾을 수 없습니다.")
        print(f"  C:\\lms-autosaver\\ 폴더에 credentials.json 파일을 복사해주세요.")
        input("  복사 완료 후 Enter 키를 누르세요...")

    print("  ✅ credentials.json 확인 완료!")

def get_email_info():
    """이메일 알림 설정"""
    print_step(4, "이메일 알림 설정 (새 파일 업로드시 알림)")
    print("""
  새 파일이 업로드되면 Gmail로 알림을 보내드립니다.
  Gmail 앱 비밀번호가 필요합니다. (일반 비밀번호 아님!)

  [Gmail 앱 비밀번호 발급 방법]
  1. https://myaccount.google.com/apppasswords 접속
  2. 앱 이름: "LMS알리미" 입력
  3. "만들기" 클릭
  4. 생성된 16자리 비밀번호 복사 (공백 제거)
  
  ⚠️  2단계 인증이 설정된 Google 계정만 사용 가능합니다.
""")
    input("  발급 완료 후 Enter 키를 누르세요...")
    email = input_with_guide("  Gmail 주소: ")
    app_pw = input_with_guide("  앱 비밀번호 (공백 없이): ", secret=True)
    return email, app_pw

def get_schedule_time():
    """자동 실행 시간 설정"""
    print_step(5, "자동 실행 시간 설정")
    print("""
  매일 몇 시에 자동으로 LMS를 확인할까요?
  (새 파일이 있으면 자동으로 Drive에 저장됩니다)
""")
    while True:
        time_input = input_with_guide("  실행 시간 입력 (예: 08:00): ")
        try:
            h, m = time_input.split(':')
            if 0 <= int(h) <= 23 and 0 <= int(m) <= 59:
                return time_input
        except:
            pass
        print("  ❌ 올바른 형식으로 입력해주세요 (HH:MM)")

def create_config(lms_id, lms_pw, gemini_key, email, app_pw, schedule_time):
    """config.py 생성"""
    config_content = f'''# ===== 설정 파일 (자동 생성) =====

# LMS 로그인 정보
LMS_ID = "{lms_id}"
LMS_PASSWORD = "{lms_pw}"

# Gemini API
GEMINI_API_KEY = "{gemini_key}"

# 이메일 알림
EMAIL_ADDRESS = "{email}"
EMAIL_PASSWORD = "{app_pw}"
EMAIL_TO = "{email}"

# 파일 저장 경로
DOWNLOAD_PATH = r"C:\\lms-autosaver\\downloads"

# 스케줄 시간
SCHEDULE_TIME = "{schedule_time}"

# LMS URL
LMS_URL = "https://lms.dgist.ac.kr"
LOGIN_URL = "https://saml.dgist.ac.kr/authentication/idpw/idPwLogin.html?agentId=-100000&useOauth=0"
'''
    with open(r"C:\lms-autosaver\config.py", 'w', encoding='utf-8') as f:
        f.write(config_content)
    print("\n  ✅ config.py 생성 완료!")

def test_lms_login(lms_id, lms_pw):
    """LMS 로그인 테스트"""
    print_step(6, "LMS 로그인 테스트")
    print("  브라우저를 열어 로그인을 확인합니다...")

    import asyncio
    from playwright.async_api import async_playwright

    async def test():
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            page = await browser.new_page()
            await page.goto("https://saml.dgist.ac.kr/authentication/idpw/idPwLogin.html?agentId=-100000&useOauth=0")
            await page.wait_for_load_state('networkidle')
            await page.fill('input[placeholder="Login ID"]', lms_id)
            await page.fill('input[type="password"]', lms_pw)
            await page.click('button:has-text("Login")')
            await page.wait_for_load_state('networkidle')
            import asyncio as a
            await a.sleep(3)

            current_url = page.url
            print(f"  현재 URL: {current_url}")
            await browser.close()

            # saml 로그인 페이지가 아니면 성공
            return 'idPwLogin' not in current_url

    result = asyncio.run(test())
    if result:
        print("  ✅ LMS 로그인 성공!")
        return True
    else:
        print("  ❌ 로그인 실패! 아이디/비밀번호를 확인해주세요.")
        return False
    
def initialize_data_files():
    """데이터 파일 초기화"""
    os.makedirs(r"C:\lms-autosaver\downloads", exist_ok=True)

    for fname in ['downloaded_files.json', 'file_metadata.json']:
        fpath = os.path.join(r"C:\lms-autosaver", fname)
        if not os.path.exists(fpath):
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write('[]' if fname == 'downloaded_files.json' else '{}')

def setup_scheduler(schedule_time):
    """Windows 작업 스케줄러 등록"""
    print_step(7, "자동 실행 스케줄러 등록")
    print(f"""
  매일 {schedule_time}에 자동으로 LMS를 확인합니다.
  (컴퓨터가 켜져 있을 때만 실행됩니다)
""")
    answer = input("  지금 바로 스케줄러를 등록할까요? (y/n): ").strip().lower()
    if answer != 'y':
        print("  스케줄러 등록을 건너뜁니다.")
        print("  나중에 등록하려면 관리자 PowerShell에서:")
        print(f"  .\\schedule_setup.ps1 -Time {schedule_time}AM")
        return

    import subprocess
    time_fmt = schedule_time.replace(':', '') 
    hour = int(schedule_time.split(':')[0])
    ampm = 'AM' if hour < 12 else 'PM'
    if hour > 12:
        hour -= 12
    time_str = f"{hour:02d}:{schedule_time.split(':')[1]}{ampm}"

    script_path = r"C:\lms-autosaver\schedule_setup.ps1"
    result = subprocess.run(
        ['powershell', '-ExecutionPolicy', 'Bypass', '-File', script_path, '-Time', time_str],
        capture_output=True, text=True
    )
    if '완료' in result.stdout:
        print(f"  ✅ 스케줄러 등록 완료! 매일 {schedule_time}에 자동 실행됩니다.")
    else:
        print("  ⚠️  관리자 권한이 필요합니다.")
        print("  PowerShell을 관리자 권한으로 열고 아래 명령어를 실행하세요:")
        print(f"  cd C:\\lms-autosaver")
        print(f"  .\\schedule_setup.ps1 -Time {time_str}")

def print_completion():
    """설치 완료 메시지"""
    print(f"""
╔══════════════════════════════════════════════════════╗
║              🎉 설치 완료! 🎉                        ║
╚══════════════════════════════════════════════════════╝

  이제 아래 명령어로 프로그램을 실행하세요:

  cd C:\\lms-autosaver
  python main.py

  ✅ 처음 실행시 Google Drive 인증 창이 뜹니다.
     브라우저에서 "계속" → Google 계정 로그인 → 허용

  📁 파일은 Google Drive의 "DGIST_LMS_파일" 폴더에 저장됩니다.
  📧 새 파일 업로드시 이메일로 알림이 옵니다.
  ⏰ 매일 설정한 시간에 자동으로 실행됩니다.

""")

def main():
    print_banner()

    print("  이 프로그램은 DGIST LMS의 강의 자료를")
    print("  자동으로 Google Drive에 정리해드립니다.\n")
    print("  설치에 약 5-10분이 소요됩니다.")
    input("\n  시작하려면 Enter 키를 누르세요...")

    # 0. 패키지 설치
    check_requirements()

    # 1. LMS 정보
    while True:
        lms_id, lms_pw = get_lms_info()

        # 로그인 테스트
        if test_lms_login(lms_id, lms_pw):
            break
        print("\n  다시 입력해주세요.")

    # 2. Google Drive
    get_google_drive_credentials()

    # 3. 이메일
    email, app_pw = get_email_info()

    # 4. 스케줄
    schedule_time = get_schedule_time()

    # config.py 생성
    create_config(lms_id, lms_pw, gemini_key, email, app_pw, schedule_time)

    # 데이터 파일 초기화
    initialize_data_files()

    # 스케줄러 등록
    setup_scheduler(schedule_time)
    
    # 완료
    print_completion()

if __name__ == "__main__":
    main()