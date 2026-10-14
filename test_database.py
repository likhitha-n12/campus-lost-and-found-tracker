"""Small automated tests for the database layer (uses temporary test data)."""

import tempfile
import unittest
from pathlib import Path

import database


class DatabaseTests(unittest.TestCase):
    def setUp(self):
        self.temp_folder = tempfile.TemporaryDirectory()
        self.db_file = Path(self.temp_folder.name) / "test_lost_found.db"
        database.initialize_database(self.db_file)

    def tearDown(self):
        self.temp_folder.cleanup()

    def sample_report(self):
        return {
            "report_type": "Lost",
            "item_name": "Blue notebook",
            "category": "Books / Notes",
            "location": "Library",
            "report_date": "2026-10-14",
            "description": "A blue notebook with a plain cover.",
            "contact_info": "",
        }

    def test_add_and_search_report(self):
        report_id = database.add_report(self.sample_report(), self.db_file)
        results = database.get_reports("notebook", self.db_file)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], report_id)
        self.assertEqual(results[0]["status"], "Open")

    def test_mark_resolved(self):
        report_id = database.add_report(self.sample_report(), self.db_file)
        self.assertTrue(database.mark_resolved(report_id, self.db_file))
        report = database.get_report(report_id, self.db_file)
        self.assertEqual(report["status"], "Resolved")

    def test_delete_report(self):
        report_id = database.add_report(self.sample_report(), self.db_file)
        self.assertTrue(database.delete_report(report_id, self.db_file))
        self.assertIsNone(database.get_report(report_id, self.db_file))


if __name__ == "__main__":
    unittest.main()
