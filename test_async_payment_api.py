import requests
import pytest

MOCK_SERVER = "payment-api-demo"


class TestAsyncPaymentApiMock:
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

        page.locator("xpath=/html/body/main/div[2]/div[5]/div[3]/div/div/div[2]/div[6]/div[1]/div/div[2]/div[1]/div[1]/select").select_option("POST")
        page.locator("xpath=/html/body/main/div[2]/div[5]/div[3]/div/div/div[2]/div[6]/div[1]/div/div[2]/div[1]/div[2]/div/div[1]/select").select_option("path:equals")
        page.locator("input.v2-path-input").fill("/api/payment")

        page.locator("xpath=/html/body/main/div[2]/div[5]/div[3]/div/div/div[2]/div[6]/div[2]/div[2]/div[1]/div/div/div/div[2]/div/div[1]/div[1]/div/select").select_option("async")
        page.locator("xpath=/html/body/main/div[2]/div[5]/div[3]/div/div/div[2]/div[6]/div[2]/div[2]/div[1]/div/div/div/div[2]/div/div[2]/div[2]/input").fill("202")
        page.locator("xpath=/html/body/main/div[2]/div[5]/div[3]/div/div/div[2]/div[6]/div[2]/div[2]/div[1]/div/div/div/div[2]/div/div[3]/div[2]/div/div[2]/textarea").fill(
            '{\n  "status": "success",\n  "message": "Payment processed successfully"\n}'
        )
        page.locator("xpath=/html/body/main/div[2]/div[5]/div[3]/div/div/div[2]/div[6]/div[2]/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[2]/input").fill(endpoint + '/callback')
        page.locator("xpath=/html/body/main/div[2]/div[5]/div[3]/div/div/div[2]/div[6]/div[2]/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[1]/select").select_option("POST")

        page.locator("xpath=/html/body/main/div[2]/div[5]/div[3]/div/div/div[2]/div[7]/div/button[2]").click()
        page.locator("xpath=/html/body/main/div[2]/div[5]/div[3]/div/div/div[3]/div/div/div/div[1]/div/button[1]").click()

        page.locator("xpath=/html/body/main/div[2]/div[5]/div[3]/div/div/div[2]/div[6]/div[1]/div/div[2]/div[1]/div[1]/select").select_option("POST")
        page.locator("xpath=/html/body/main/div[2]/div[5]/div[3]/div/div/div[2]/div[6]/div[1]/div/div[2]/div[1]/div[2]/div/div[2]/input").fill("/callback")

        page.locator("xpath=/html/body/main/div[2]/div[5]/div[3]/div/div/div[2]/div[7]/div/button[2]").click()
        page.locator("xpath=/html/body/main/div[2]/div[5]/div[3]/div/div/div[1]/div/button").click()
        page.wait_for_timeout(1000)

        url = "https://payment-api-demo.free.beeceptor.com/api/payment"
        response = requests.post(url, json={"amount": 1000, "customerId": "C123"}, timeout=10)
        assert response.status_code == 202
        data = response.json()
        assert data["status"] == "success"
