# University Campus Administration

A lightweight Flask app for managing the predefined list of university campuses.

## Features
- Creates a SQLite-backed `university_campuses` table.
- Provides an admin view of all campuses.
- Supports adding new campuses and deleting existing ones.

## Run locally
1. Install dependencies:
   ```bash
   python -m pip install --break-system-packages -r requirements.txt
   ```
2. Start the app:
   ```bash
   python app.py
   ```
3. Open http://127.0.0.1:5000/admin/campuses
