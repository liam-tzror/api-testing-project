# API Testing Project

## About
Automated testing project built with Python and pytest, covering a custom REST API (Node.js, Express, SQLite) at both the API and UI levels.
Includes integration tests, security tests, content validation, and bug detection - API testing with `requests`, and end-to-end UI testing with Playwright against a minimal HTML frontend that talks to the same API.

## Tech Stack
**Testing:** Python, pytest, requests, Playwright
**API Server:** Node.js, Express, better-sqlite3
**Frontend:** Minimal HTML/JavaScript (login + task list, calls the API via fetch)

## Tests Overview

### API tests (`test_advanced.py`)
- CRUD operations (Create, Read, Update, Delete)
- Authentication & authorization tests
- Security tests (XSS)
- Input validation (invalid types, empty fields, long titles) using parametrize
- Response content validation (not just status codes)
- Error message verification
- Automatic test data cleanup using pytest fixtures (yield)
- Shared authenticated session (`requests.Session`) instead of repeating headers per request
- Configurable API URL via `BASE_URL` environment variable

### UI tests (`test_ui.py`)
- Login flow (success, wrong password, empty fields)
- Task creation and deletion through the UI
- Content-based locators (`has_text`) instead of fixed positions, so tests don't break as data changes
- Input validation matching the API behavior (empty title, whitespace-only title)
- Security test (XSS) - documents that malicious input is currently accepted rather than blocked, matching the same gap found at the API level

## How to Run

1. Install Node.js dependencies:
```
npm install
```

2. Start the API server:
```
node server.js
```

3. In a separate terminal, serve the frontend:
```
python -m http.server 8080
```

4. In another terminal, install Python dependencies:
```
pip install requests pytest pytest-playwright
playwright install
```

5. Run the API tests:
```
pytest test_advanced.py -v
```

6. Run the UI tests:
```
pytest test_ui.py -v
```

## Author
Liam Tzror - QA Automation Engineer