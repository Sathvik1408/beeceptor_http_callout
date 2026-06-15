import json
import requests
import pytest

MOCK_SERVER = "get-dog-api"


class TestSyncDogApiMock:
    def test_full_flow(self, page):
        page.goto("https://beeceptor.com")
        page.locator("#channel").fill(MOCK_SERVER)
        page.locator("button[type='submit']").click()
        page.wait_for_load_state("networkidle")

        endpoint = page.locator("#endpointUrl").text_content().strip()
        assert endpoint.startswith("https://")

        page.locator("xpath=/html/body/main/div[2]/div[2]/div[1]/div[2]/a[1]").click()
        page.locator("button.dropdown-toggle-split").click()
        page.locator("xpath=/html/body/main/div[2]/div[5]/div[3]/div/div/div[3]/div/div/div/div[1]/div/ul/li[2]/a").click()

        page.locator("xpath=/html/body/main/div[2]/div[5]/div[3]/div/div/div[2]/div[6]/div[1]/div/div[2]/div[1]/div[1]/select").select_option("GET")
        page.locator("xpath=/html/body/main/div[2]/div[5]/div[3]/div/div/div[2]/div[6]/div[1]/div/div[2]/div[1]/div[2]/div/div[1]/select").select_option("path:equals")
        page.locator("input.v2-path-input").fill("/api/dog_image")

        page.locator("xpath=/html/body/main/div[2]/div[5]/div[3]/div/div/div[2]/div[6]/div[2]/div[2]/div[1]/div/div/div/div[2]/div/div[1]/div[1]/div/select").select_option("sync")
        page.locator("xpath=/html/body/main/div[2]/div[5]/div[3]/div/div/div[2]/div[6]/div[2]/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[1]/select").select_option("GET")
        page.locator("xpath=/html/body/main/div[2]/div[5]/div[3]/div/div/div[2]/div[6]/div[2]/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[2]/input").fill("https://dog.ceo/api/breeds/image/random")

        page.locator("xpath=/html/body/main/div[2]/div[5]/div[3]/div/div/div[2]/div[7]/div/button[2]").click()
        page.locator("xpath=/html/body/main/div[2]/div[5]/div[3]/div/div/div[1]/div/button").click()
        page.wait_for_load_state("networkidle")

        response = requests.get(f"{endpoint}/api/dog_image", timeout=10)
        assert response.status_code == 200

        data = response.json()
        assert "message" in data
        assert "status" in data
        assert data["message"].startswith("https://")
