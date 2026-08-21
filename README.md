# API Testing Project

## About
Automated API testing project built with Python and pytest, testing a custom REST API built with Node.js, Express, and SQLite.
Includes integration tests, security tests, content validation, and bug detection.

## Tech Stack
**Testing:** Python, pytest, requests
**API Server:** Node.js, Express, better-sqlite3

## Tests Overview
- CRUD operations (Create, Read, Update, Delete)
- Authentication & authorization tests
- Security tests (XSS)
- Input validation (invalid types, empty fields, long titles) using parametrize
- Response content validation (not just status codes)
- Error message verification
- Automatic test data cleanup using pytest fixtures (yield)

## How to Run
1. Install Node.js dependencies:
npm install

2. Start the API server:
node server.js

3. In a separate terminal, install Python dependencies:
pip install requests pytest

4. Run all tests:
pytest test_advanced.py -v

## Author
Liam Tzror - QA Automation Engineer