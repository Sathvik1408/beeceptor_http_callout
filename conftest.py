import json
from pathlib import Path

import pytest
from playwright.sync_api import sync_playwright
from requests.cookies import RequestsCookieJar


@pytest.fixture(scope="session")
def playwright():
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="function")
def browser(playwright):
    browser = playwright.chromium.launch(headless=False, slow_mo=500)
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def context(browser):
    context = browser.new_context(
        record_video_dir="videos/",
        record_video_size={"width": 1280, "height": 720}
    )
    cookies_path = Path(__file__).parent / "cookies.json"
    if cookies_path.exists():
        with open(cookies_path) as f:
            cookies = json.load(f)
        context.add_cookies(cookies)
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context):
    page = context.new_page()
    yield page
    page.close()


@pytest.fixture(scope="function")
def beeceptor_endpoint(page):
    page.goto("https://beeceptor.com")
    return page


@pytest.fixture(scope="function")
def cookies(context):
    jar = RequestsCookieJar()
    for c in context.cookies():
        jar.set(c["name"], c["value"], domain=c.get("domain"), path=c.get("path"))
    return jar
