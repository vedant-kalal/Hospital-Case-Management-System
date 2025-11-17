# Hospital Case Management System

Hospital case management system

Works on CLI, made with fully connected backend and MySql DataBase using SQLAlchemy.

## Overview
This project is a CLI-based hospital case management system implemented in Python using SQLAlchemy as the ORM and MySQL as the database backend. It contains models, services, and utilities to manage patient cases, clinicians, health centers, and case notes.

## Quickstart
1. Create and activate a Python virtual environment.

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install dependencies (you may need to adjust package names based on the project):

   ```powershell
   pip install -r requirements.txt
   ```

3. Configure your MySQL connection string in `src/config.py` (or via environment variables) and run the CLI/entrypoint (e.g., `demo.py`).

4. Typical workflow:
   - Start the database server (MySQL)
   - Update config
   - Run scripts or the CLI to interact with the system

## Notes
- This repository expects a MySQL database. Use appropriate credentials and create the database before running migrations or the app.
- If you want me to add a `requirements.txt` or GitHub Actions CI, tell me and I can add them.

## License
Add a license if you want the repository to be open source.
