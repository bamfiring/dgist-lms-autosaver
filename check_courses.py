import asyncio
import re
import html
import json
from playwright.async_api import async_playwright
from config import LMS_ID, LMS_PASSWORD, LOGIN_URL, LMS_URL

async def check():
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

        # 프로그래밍만 집중 확인
        test_courses = [
            ('_20961_1', '프로그래밍'),
            ('_21002_1', '일반생물학실험'),
        ]

        for cid, cname in test_courses:
            print(f"\n{'='*50}")
            print(f"{cname}")

            # 1. 토론 게시글 안에 파일 있는지
            print("\n[토론 게시글 확인]")
            discuss_api = await page.request.get(
                f'{LMS_URL}/learn/api/public/v1/courses/{cid}/discussions?limit=100'
            )
            if discuss_api.status == 200:
                ddata = await discuss_api.json()
                for d in ddata.get('results', []):
                    did = d.get('id', '')
                    dtitle = d.get('title', '')
                    print(f"  토론: {dtitle}")

                    # 토론 게시글 목록
                    posts_api = await page.request.get(
                        f'{LMS_URL}/learn/api/public/v1/courses/{cid}/discussions/{did}/posts?limit=20'
                    )
                    print(f"    게시글 API 상태: {posts_api.status}")
                    if posts_api.status == 200:
                        pdata = await posts_api.json()
                        posts = pdata.get('results', [])
                        print(f"    게시글 수: {len(posts)}")
                        for post in posts[:3]:
                            body = post.get('body', '')
                            files = re.findall(r'data-bbfile="([^"]+)"', body)
                            if files:
                                print(f"    파일 있음!")
                                for f in files:
                                    try:
                                        fi = json.loads(html.unescape(f))
                                        print(f"      - {fi.get('fileName') or fi.get('linkName')}")
                                    except: pass

            # 2. 성적부/과제 첨부파일 확인
            print("\n[성적부/과제 확인]")
            grade_api = await page.request.get(
                f'{LMS_URL}/learn/api/public/v1/courses/{cid}/gradebook/columns?limit=100'
            )
            if grade_api.status == 200:
                gdata = await grade_api.json()
                for col in gdata.get('results', []):
                    col_id = col.get('id', '')
                    col_name = col.get('name', '')
                    col_type = col.get('contentId', '')
                    print(f"  과제: {col_name} (contentId: {col_type})")

                    # 과제 콘텐츠 첨부파일 확인
                    if col_type:
                        attach_api = await page.request.get(
                            f'{LMS_URL}/learn/api/public/v1/courses/{cid}/contents/{col_type}/attachments'
                        )
                        print(f"    첨부파일 API 상태: {attach_api.status}")
                        if attach_api.status == 200:
                            adata = await attach_api.json()
                            for att in adata.get('results', []):
                                print(f"    파일: {att.get('fileName')}")

        input("\n확인 후 Enter...")
        await browser.close()

asyncio.run(check())