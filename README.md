# Campus Lost & Found Tracker

A beginner-friendly Python desktop app for reporting and tracking lost and found items on campus.

## Features

- Add a **Lost** or **Found** report.
- Store item name, category, location, date, description, and optional contact information.
- Save reports locally in an SQLite database.
- Search reports by item, category, location, description, type, or status.
- View full details by double-clicking a row.
- Mark reports as **Resolved** when an item is returned or otherwise handled.
- Delete reports after a confirmation prompt.
- Includes simple automated tests for database operations.

## Requirements

- Python 3.9 or newer recommended.
- Tkinter and SQLite are included with most standard Python installations.
- No third-party packages are required.

## Run on Windows

1. Download and extract `campus_lost_found_tracker.zip`.
2. Open the extracted folder.
3. Open PowerShell or Command Prompt in that folder.
4. Run:

   ```powershell
   python app.py
   ```

5. The app window will open. Add a report using the form at the top.

The first run automatically creates `lost_found.db` in the project folder. Keep that file if you want to preserve saved records. To start over, close the app and delete `lost_found.db` (this permanently deletes its saved reports).

## How to use

1. Select **Lost** if you misplaced something, or **Found** if you found an item.
2. Fill in the required fields marked with `*`.
3. Use the date format `YYYY-MM-DD`, for example `2026-10-14`.
4. Click **Add report**.
5. Search using the search box and click **Search** or press Enter.
6. Select a row and click **Mark resolved** after the issue is handled.
7. Double-click a row to see its full description and optional contact information.

## Run the database tests

From the project folder, run:

```powershell
python -m unittest -v
```

The tests use a temporary database and will not change the app's real `lost_found.db`.

## Project structure

```text
campus_lost_found_tracker/
├── app.py             # Tkinter interface and user actions
├── database.py        # SQLite database operations
├── test_database.py  # Small automated tests
├── README.md          # Setup and usage instructions
├── requirements.txt   # No external dependencies
└── .gitignore         # Ignores local database/cache files
```

## Important notes

- This is a local, beginner-level project, not a shared college-wide website. Reports are stored on the computer where the program runs.
- Contact information is optional. Avoid entering sensitive personal information. If this is used by a real college, get approval before collecting student data and add proper access controls.
- Add, test, and understand features yourself before listing them on a resume or describing them in an interview.

## Resume description (use after you have run and tested it)

**Campus Lost & Found Tracker | Python, Tkinter, SQLite**

- Built a desktop application to record and search lost and found items using item details, category, location, and date.
- Implemented persistent local storage with SQLite and report-status updates to track resolved items.
- Added form validation, keyword search, detail viewing, and confirmation before deleting records.
