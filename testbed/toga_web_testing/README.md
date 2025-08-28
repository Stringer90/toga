This repository is dedicated to development, testing, and proof-of-concept work related to issue [3545](https://github.com/beeware/toga/issues/3545), which focuses on implementing testing for the web platform.

## How We Run this Test Suite
1. Open this repository in VSCode.
2. Ensure you have the following installed in your environment/venv (these are the versions I use):
   - `playwright==1.51.0`
   - `pytest==8.3.5`
   - `pytest-asyncio==0.26.0`
   - `pytest-playwright==0.7.0`
3. Open a Toga app in another VSCode window.
4. Copy the contents of this repository’s example `app.py` into your Toga project.
5. Update and build your Toga app for web.
6. Run your Toga app as a web app.
7. In this repository’s VSCode window:
   - `cd` into the repository’s directory.
   - Run: `pytest testbed/tests`
