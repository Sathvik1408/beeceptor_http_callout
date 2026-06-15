import pytest
from playwright.sync_api import sync_playwright


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
