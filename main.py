# ===== 메인 실행 + 스케줄러 =====
import asyncio
import schedule
import time
import os
from config import SCHEDULE_TIME, DOWNLOAD_PATH
from lms_crawler import crawl_lms, load_file_metadata, get_all_courses
from drive_uploader import upload_to_drive_with_path, get_drive_service, get_or_create_folder, ROOT_FOLDER
from email_notifier import send_kakao_message

async def run_job():
    print("\n" + "="*50)
    print("LMS 자동 저장 시작!")
    print("="*50)

    # 1. LMS에서 새 파일 수집
    new_files = await crawl_lms()

    # 2. 파일 메타데이터 로드
    file_metadata = load_file_metadata()

    # 3. 모든 과목 폴더 생성 (파일 없어도)
    print("\n[Drive 과목 폴더 생성]")
    all_courses = await get_all_courses()
    service = get_drive_service()
    root_id = get_or_create_folder(service, ROOT_FOLDER)
    for course_name in all_courses:
        get_or_create_folder(service, course_name.strip()[:40], root_id)

    # 4. 로컬 파일 전체를 Drive에 동기화
    print("\n[Drive 동기화 시작]")
    uploaded_count = 0
    skipped_count = 0

    if os.path.exists(DOWNLOAD_PATH):
        for file_name in os.listdir(DOWNLOAD_PATH):
            file_path = os.path.join(DOWNLOAD_PATH, file_name)
            if not os.path.isfile(file_path):
                continue

            meta = file_metadata.get(file_name, {})
            course_name = meta.get('course', '기타')
            folder_path = meta.get('folder_path', [])

            result = upload_to_drive_with_path(
                file_path, file_name, course_name, folder_path
            )
            if result == 'exists':
                skipped_count += 1
            elif result:
                uploaded_count += 1

    print(f"[Drive 동기화 완료] 신규 {uploaded_count}개 업로드, 기존 {skipped_count}개 스킵")

    # 5. 이메일 알림
    if new_files:
        message = f"📚 DGIST LMS 새 파일!\n\n총 {len(new_files)}개\n\n"
        for r in new_files[:10]:
            message += f"📖 [{r['course'][:15]}]\n{r['name']}\n\n"
        if len(new_files) > 10:
            message += f"... 외 {len(new_files)-10}개\n"
        send_kakao_message(message)
    else:
        send_kakao_message("📚 DGIST LMS\n새로운 파일이 없습니다.")

    print("\n✅ 모든 작업 완료!")

def job():
    asyncio.run(run_job())

if __name__ == "__main__":
    print(f"LMS 자동 저장 프로그램 시작!")
    print(f"매일 {SCHEDULE_TIME}에 자동 실행됩니다.")
    print("지금 바로 실행하려면 Enter, 스케줄만 등록하려면 Ctrl+C")

    try:
        input()
        job()
    except KeyboardInterrupt:
        pass

    schedule.every().day.at(SCHEDULE_TIME).do(job)
    print(f"\n스케줄 등록 완료! ({SCHEDULE_TIME} 자동 실행)")

    while True:
        schedule.run_pending()
        time.sleep(60)