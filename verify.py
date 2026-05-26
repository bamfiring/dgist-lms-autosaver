import asyncio
import re
import html
import json
from playwright.async_api import async_playwright
from config import LMS_ID, LMS_PASSWORD, LOGIN_URL, LMS_URL

async def verify():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        print("로그인 중...")
        await page.goto(LOGIN_URL)
        await page.wait_for_load_state('networkidle')
        await asyncio.sleep(2)
        await page.fill('input[placeholder="Login ID"]', LMS_ID)
        await page.fill('input[type="password"]', LMS_PASSWORD)
        await page.click('button:has-text("Login")')
        await page.wait_for_load_state('networkidle')
        await asyncio.sleep(5)
        await page.goto(f"{LMS_URL}/ultra/institution-page")
        await page.wait_for_load_state('networkidle')
        await asyncio.sleep(3)

        # 로컬 다운로드 파일 목록
        import os
        from config import DOWNLOAD_PATH
        local_files = set(os.listdir(DOWNLOAD_PATH))

        courses_api = await page.request.get(
            f'{LMS_URL}/learn/api/public/v1/users/me/courses?limit=100&fields=courseId,course.name'
        )
        data = await courses_api.json()

        total_lms = 0
        total_missing = 0

        for r in data.get('results', []):
            cid = r.get('courseId')
            cname = r.get('course', {}).get('name', '')
            course_short = cname[:30]

            lms_files = []

            # 1. 콘텐츠 파일 수집
            contents_api = await page.request.get(
                f'{LMS_URL}/learn/api/public/v1/courses/{cid}/contents?limit=100'
            )
            if contents_api.status == 200:
                cdata = await contents_api.json()
                await collect_content_files(page, cid, cdata.get('results', []), lms_files)

            # 2. 공지사항 파일 수집
            announce_api = await page.request.get(
                f'{LMS_URL}/learn/api/public/v1/courses/{cid}/announcements?limit=100'
            )
            if announce_api.status == 200:
                adata = await announce_api.json()
                for ann in adata.get('results', []):
                    body = ann.get('body', '')
                    matches = re.findall(r'data-bbfile="([^"]+)"', body)
                    for match in matches:
                        try:
                            decoded = html.unescape(match)
                            file_info = json.loads(decoded)
                            fname = file_info.get('fileName', '') or file_info.get('linkName', '') or file_info.get('alternativeText', '')
                            if fname:
                                lms_files.append(f"[공지] {fname}")
                        except:
                            pass

            # 비교
            missing = []
            for f in lms_files:
                clean = f.replace('[공지] ', '')
                if clean.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
                    continue
                if clean not in local_files:
                    missing.append(f)

            print(f"\n{'='*50}")
            print(f"{course_short}")
            print(f"  LMS 파일: {len(lms_files)}개 | 로컬: {len([f for f in lms_files if f.replace('[공지] ','') in local_files])}개 | 누락: {len(missing)}개")
            if missing:
                for m in missing:
                    print(f"  ❌ 누락: {m}")
            else:
                print(f"  ✅ 모두 있음")

            total_lms += len(lms_files)
            total_missing += len(missing)

        print(f"\n{'='*50}")
        print(f"총 LMS 파일: {total_lms}개 | 누락: {total_missing}개")

        await browser.close()

async def collect_content_files(page, course_id, contents, result, depth=0):
    if depth > 8:
        return

    from config import LMS_URL

    skip_types = ['resource/x-bb-bltiplacement-Zoom', 'resource/x-bb-externallink', 'resource/x-bb-asmt-test-link']

    for content in contents:
        content_id = content.get('id', '')
        content_title = content.get('title', '')
        content_type = content.get('contentHandler', {}).get('id', '')

        if content_type in skip_types:
            continue

        if 'class recording' in content_title.lower():
            continue
        if 'zoom' in content_title.lower():
            continue

        if 'resource/x-bb-file' in content_type or 'resource/x-bb-document' in content_type:
            attach_resp = await page.request.get(
                f'{LMS_URL}/learn/api/public/v1/courses/{course_id}/contents/{content_id}/attachments'
            )
            if attach_resp.status == 200:
                attach_data = await attach_resp.json()
                for att in attach_data.get('results', []):
                    fname = att.get('fileName', content_title)
                    if fname:
                        result.append(fname)
        else:
            sub_resp = await page.request.get(
                f'{LMS_URL}/learn/api/public/v1/courses/{course_id}/contents/{content_id}/children?limit=100'
            )
            if sub_resp.status == 200:
                sub_data = await sub_resp.json()
                sub_contents = sub_data.get('results', [])
                if sub_contents:
                    await collect_content_files(page, course_id, sub_contents, result, depth+1)

asyncio.run(verify())