"""
Tests for the header-expansion logic in sync_to_sheets.py.

These tests run entirely in-process with lightweight mock objects so that no
real Google Sheets connection is required.  Run with:

    python src/test_sync_header_expand.py
"""
from __future__ import annotations

import io
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, call, patch

# ---------------------------------------------------------------------------
# Minimal gspread.utils stub so the module can import without gspread installed.
# ---------------------------------------------------------------------------
import types

_fake_gspread = types.ModuleType("gspread")
_fake_utils = types.ModuleType("gspread.utils")


def _rowcol_to_a1(row: int, col: int) -> str:  # noqa: ARG001
    letters = ""
    while col:
        col, rem = divmod(col - 1, 26)
        letters = chr(65 + rem) + letters
    return f"{letters}{row}"


_fake_utils.rowcol_to_a1 = _rowcol_to_a1
_fake_gspread.utils = _fake_utils
_fake_gspread.WorksheetNotFound = type("WorksheetNotFound", (Exception,), {})

sys.modules.setdefault("gspread", _fake_gspread)
sys.modules.setdefault("gspread.utils", _fake_utils)

# pandas must be available (it is listed in requirements.txt).
import pandas as pd  # noqa: E402

# Now import the module under test.
sys.path.insert(0, str(Path(__file__).parent))
import sync_to_sheets as sts  # noqa: E402

# ---------------------------------------------------------------------------
# Helper: build a mock worksheet whose get_all_values() returns `rows`.
# ---------------------------------------------------------------------------

def _make_ws(rows: list[list[str]]) -> MagicMock:
    ws = MagicMock()
    ws.get_all_values.return_value = rows
    return ws


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestExpandHeader(unittest.TestCase):
    """Unit tests for expand_header()."""

    def test_no_missing_columns_returns_sheet_header(self) -> None:
        ws = _make_ws([])  # get_all_values not called by expand_header directly
        sheet_header = ["signal_id", "asset", "side"]
        csv_columns = ["signal_id", "asset", "side"]

        result = sts.expand_header(ws, csv_columns, sheet_header, "EVALUATIONS")

        self.assertEqual(result, sheet_header)
        ws.update.assert_not_called()

    def test_new_columns_appended_to_header(self) -> None:
        ws = _make_ws([])
        sheet_header = ["signal_id", "asset", "side"]
        csv_columns = ["signal_id", "asset", "side", "mfe", "mae", "r_multiple"]

        result = sts.expand_header(ws, csv_columns, sheet_header, "EVALUATIONS")

        expected = ["signal_id", "asset", "side", "mfe", "mae", "r_multiple"]
        self.assertEqual(result, expected)
        ws.update.assert_called_once()
        call_args = ws.update.call_args
        # The first positional/keyword arg should be the range string
        range_arg = call_args[0][0] if call_args[0] else call_args[1].get("range_name", "")
        self.assertIn("A1", range_arg)
        # The values passed should be the full new header
        values_arg = call_args[0][1]
        self.assertEqual(values_arg, [expected])

    def test_log_message_on_new_columns(self) -> None:
        ws = _make_ws([])
        sheet_header = ["signal_id", "asset", "side"]
        csv_columns = ["signal_id", "asset", "side", "mfe", "mae"]

        buf = io.StringIO()
        with patch("sys.stdout", buf):
            sts.expand_header(ws, csv_columns, sheet_header, "EVALUATIONS")

        output = buf.getvalue()
        self.assertIn("added 2 new columns", output)
        self.assertIn("mfe", output)
        self.assertIn("mae", output)

    def test_log_message_already_up_to_date(self) -> None:
        ws = _make_ws([])
        sheet_header = ["signal_id", "asset"]
        csv_columns = ["signal_id", "asset"]

        buf = io.StringIO()
        with patch("sys.stdout", buf):
            sts.expand_header(ws, csv_columns, sheet_header, "EVALUATIONS")

        self.assertIn("already up to date", buf.getvalue())


class TestEnsureHeader(unittest.TestCase):
    """Unit tests for ensure_header() covering the three cases."""

    def test_case1_empty_sheet_creates_header(self) -> None:
        ws = _make_ws([])
        header = ["signal_id", "asset"]

        result = sts.ensure_header(ws, header, "EVALUATIONS")

        ws.append_row.assert_called_once_with(header, value_input_option="RAW")
        self.assertEqual(result, header)

    def test_case2_invalid_header_inserts_at_row1(self) -> None:
        # Sheet has rows but no signal_id in header -> invalid.
        ws = _make_ws([["foo", "bar"], ["1", "2"]])
        header = ["signal_id", "asset"]

        result = sts.ensure_header(ws, header, "EVALUATIONS")

        ws.insert_row.assert_called_once_with(header, index=1, value_input_option="RAW")
        self.assertEqual(result, header)

    def test_case3_valid_header_with_missing_columns_expands(self) -> None:
        old_header = ["signal_id", "asset", "side"]
        ws = _make_ws([old_header, ["S001", "USDJPY", "LONG"]])
        csv_columns = ["signal_id", "asset", "side", "mfe", "mae"]

        result = sts.ensure_header(ws, csv_columns, "EVALUATIONS")

        # expand_header should have been called -> update() was invoked.
        ws.update.assert_called_once()
        self.assertEqual(result, ["signal_id", "asset", "side", "mfe", "mae"])

    def test_case3_valid_header_already_complete_no_update(self) -> None:
        old_header = ["signal_id", "asset", "side", "mfe", "mae"]
        ws = _make_ws([old_header])
        csv_columns = ["signal_id", "asset", "side", "mfe", "mae"]

        result = sts.ensure_header(ws, csv_columns, "EVALUATIONS")

        ws.update.assert_not_called()
        self.assertEqual(result, old_header)


class TestAppendCsv(unittest.TestCase):
    """Integration-style tests for append_csv() using a CSV file on disk."""

    def setUp(self) -> None:
        import tempfile

        self._tmp = tempfile.TemporaryDirectory()
        self._tmp_dir = Path(self._tmp.name)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def _write_csv(self, filename: str, df: pd.DataFrame) -> Path:
        path = self._tmp_dir / filename
        df.to_csv(path, index=False)
        return path

    def _make_spreadsheet(self, ws: MagicMock) -> MagicMock:
        ss = MagicMock()
        ss.worksheet.return_value = ws
        return ss

    def test_new_columns_added_and_row_aligned(self) -> None:
        """
        Scenario:
        - Sheet has old header: signal_id, asset, side
        - CSV has new header:   signal_id, asset, side, mfe, mae, r_multiple
        - After sync: sheet header extended, row appended in sheet-header order.
        """
        old_header = ["signal_id", "asset", "side"]
        existing_data_row = ["S001", "USDJPY", "LONG"]
        ws = _make_ws([old_header, existing_data_row])

        # Simulate update() modifying get_all_values to return the new header.
        new_header = old_header + ["mfe", "mae", "r_multiple"]
        ws.update.side_effect = lambda *a, **kw: ws.get_all_values.return_value.__setitem__(
            0, new_header
        )

        ss = self._make_spreadsheet(ws)
        df = pd.DataFrame(
            [
                {
                    "signal_id": "S002",
                    "asset": "EURUSD",
                    "side": "SHORT",
                    "mfe": 1.5,
                    "mae": -0.3,
                    "r_multiple": 1.5,
                }
            ]
        )
        csv_path = self._write_csv("evaluations.csv", df)

        result = sts.append_csv(ss, csv_path, "EVALUATIONS")

        self.assertTrue(result)
        ws.append_rows.assert_called_once()
        appended = ws.append_rows.call_args[0][0]
        # Should have exactly one row.
        self.assertEqual(len(appended), 1)
        row = appended[0]
        # Row length should match the expanded header (6 columns).
        self.assertEqual(len(row), 6)
        # signal_id at position 0
        self.assertEqual(row[0], "S002")
        # mfe at position 3 (index of new header)
        self.assertEqual(row[3], "1.5")

    def test_duplicate_row_skipped_on_second_sync(self) -> None:
        """
        Scenario:
        - Sheet already has signal S001.
        - CSV contains S001 again.
        - append_rows should NOT be called (or called with empty list).
        """
        header = ["signal_id", "asset", "side", "mfe"]
        existing_row = ["S001", "USDJPY", "LONG", "1.2"]
        ws = _make_ws([header, existing_row])

        ss = self._make_spreadsheet(ws)
        df = pd.DataFrame(
            [{"signal_id": "S001", "asset": "USDJPY", "side": "LONG", "mfe": 1.2}]
        )
        csv_path = self._write_csv("evaluations.csv", df)

        sts.append_csv(ss, csv_path, "EVALUATIONS")

        # append_rows should not have been called because all rows are duplicates.
        ws.append_rows.assert_not_called()

    def test_new_column_log_output(self) -> None:
        old_header = ["signal_id", "asset"]
        ws = _make_ws([old_header])
        new_header = old_header + ["mfe"]
        ws.update.side_effect = lambda *a, **kw: ws.get_all_values.return_value.__setitem__(
            0, new_header
        )

        ss = self._make_spreadsheet(ws)
        df = pd.DataFrame([{"signal_id": "S001", "asset": "USDJPY", "mfe": 1.0}])
        csv_path = self._write_csv("evaluations.csv", df)

        buf = io.StringIO()
        with patch("sys.stdout", buf):
            sts.append_csv(ss, csv_path, "EVALUATIONS")

        output = buf.getvalue()
        self.assertIn("added 1 new columns", output)
        self.assertIn("mfe", output)


if __name__ == "__main__":
    unittest.main(verbosity=2)
