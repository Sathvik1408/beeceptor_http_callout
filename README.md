# Beeceptor Mock API Tests

Playwright + pytest end-to-end test suite for automating [Beeceptor](https://beeceptor.com) mock API endpoint creation, rule configuration, and validation.

## Overview

Beeceptor is a mock API service. These tests automate the full lifecycle:

1. Launch Beeceptor and create a named endpoint
2. Configure request-matching rules (method + path)
3. Set up sync/async HTTP callout responses
4. Send test requests and validate responses

## Test Cases

| File | Description | Type |
|------|-------------|------|
| `test_sync_dog_api.py` | Proxies `GET /api/dog_image` → Dog CEO API (sync) | Synchronous |
| `test_async_payment_api.py` | Simulates async payment with callback on `POST /api/payment` | Asynchronous |

## Prerequisites

- Python 3.8+
- Playwright browsers (`playwright install chromium`)
- Internet access to `beeceptor.com`

## Setup

```bash
pip install -r requirements.txt
playwright install chromium
```

## Run All Tests

```bash
pytest -v
```

## Run Specific Test

```bash
pytest -v -k "dog"
pytest -v -k "payment"
```

## Run with HTML Report

```bash
pytest -v --html=report.html
```

## Project Structure

```
├── conftest.py                   # Shared fixtures (browser, context, page)
├── pytest.ini                    # Pytest configuration
├── requirements.txt
├── README.md
├── test_sync_dog_api.py          # Dog API sync mock tests
├── test_async_payment_api.py     # Payment API async mock tests
└── videos/                       # Test session recordings
```

## Fixtures (conftest.py)

- `playwright` — session-scoped Playwright instance
- `browser` — function-scoped Chromium browser
- `context` — function-scoped browser context with video recording
- `page` — function-scoped page
- `beeceptor_endpoint` — navigates to Beeceptor and returns the page
