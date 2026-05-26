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

        cid = '_20961_1'

        announce_api = await page.request.get(
            f'{LMS_URL}/learn/api/public/v1/courses/{cid}/announcements?limit=100'
        )
        adata = await announce_api.json()

        for ann in adata.get('results', []):
            title = ann.get('title', '')
            body = ann.get('body', '')
            matches = re.findall(r'data-bbfile="([^"]+)"', body)

            if matches:
                print(f"\n✅ [{title}]")
                for match in matches:
                    try:
                        decoded = html.unescape(match)
                        file_info = json.loads(decoded)
                        print(f"  전체 데이터: {file_info}")
                    except Exception as e:
                        print(f"  파싱 실패: {e}")

        input("\n확인 후 Enter...")
        await browser.close()

asyncio.run(check())