# API Testing Project

## About
Automated API testing project built with Python and pytest.
Includes integration tests, security tests, content validation, and bug detection - built from scratch with a custom Node.js + SQLite API server.

## Tech Stack
- Python
- pytest
- requests

## Tests Overview
- CRUD operations (Create, Read, Update, Delete)
- Authentication & authorization tests
- Security tests (SQL Injection, XSS, Fake Token)
- Input validation (invalid types, empty fields, long titles) using parametrize
- Response content validation (not just status codes)
- Error message verification

## How to Run
1. Install dependencies:
pip install requests pytest

2. Run all tests:
pytest test_advanced.py -v

## Author
Liam Tzror - QA Automation Engineer