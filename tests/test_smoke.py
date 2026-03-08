#!/usr/bin/env python3
"""Smoke-Tests fuer LitZentrum Core-Module."""

import sys
import os
from unittest.mock import MagicMock
from pathlib import Path

# PyQt6 mocken fuer headless Tests
for mod in ['PyQt6', 'PyQt6.QtWidgets', 'PyQt6.QtCore', 'PyQt6.QtGui',
            'PyQt6.QtWebEngineWidgets', 'PyQt6.QtPrintSupport']:
    if mod not in sys.modules:
        sys.modules[mod] = MagicMock()

# QObject-Mock mit funktionierendem __init_subclass__
mock_qobject = MagicMock()
mock_qobject.__init_subclass__ = classmethod(lambda cls, **kw: None)
sys.modules['PyQt6.QtCore'].QObject = mock_qobject
sys.modules['PyQt6.QtCore'].pyqtSignal = MagicMock(return_value=MagicMock())
sys.modules['PyQt6.QtCore'].QSettings = MagicMock

# Projekt-src zum Path
src_dir = str(Path(__file__).parent.parent / "src")
sys.path.insert(0, src_dir)

import unittest


class TestEventType(unittest.TestCase):
    """Tests fuer EventType Enum."""

    def test_import(self):
        from core.event_bus import EventType
        self.assertIsNotNone(EventType)

    def test_all_event_types_exist(self):
        from core.event_bus import EventType
        expected = [
            "PROJECT_OPENED", "PROJECT_CLOSED", "PROJECT_SAVED",
            "SOURCE_SELECTED", "SOURCE_CREATED", "SOURCE_UPDATED", "SOURCE_DELETED",
            "NOTE_ADDED", "NOTE_UPDATED", "NOTE_DELETED",
            "QUOTE_ADDED", "QUOTE_UPDATED", "QUOTE_DELETED",
            "STATUS_MESSAGE", "ERROR_MESSAGE", "REFRESH_VIEW",
        ]
        for name in expected:
            self.assertTrue(hasattr(EventType, name), f"EventType.{name} fehlt")

    def test_event_values_are_strings(self):
        from core.event_bus import EventType
        for evt in EventType:
            self.assertIsInstance(evt.value, str)


class TestModels(unittest.TestCase):
    """Tests fuer Datenmodelle."""

    def test_search_result(self):
        from models import SearchResult
        sr = SearchResult(
            source_path=Path("/test/file.pdf"),
            title="Test Paper",
            authors=["Author A", "Author B"],
            year=2025,
            match_type="title",
            match_text="Test"
        )
        self.assertEqual(sr.title, "Test Paper")
        self.assertEqual(sr.relevance, 1.0)

    def test_export_options_defaults(self):
        from models import ExportOptions
        eo = ExportOptions(format="bibtex")
        self.assertEqual(eo.citation_style, "apa")
        self.assertFalse(eo.include_abstracts)
        self.assertFalse(eo.include_notes)

    def test_import_result(self):
        from models import ImportResult
        ir = ImportResult(success=True, imported_count=5)
        self.assertTrue(ir.success)
        self.assertEqual(ir.imported_count, 5)
        self.assertEqual(ir.errors, [])

    def test_pdf_selection_to_quote(self):
        from models import PDFSelection
        sel = PDFSelection(text="Wichtiges Zitat", page=3, rect=(0, 0, 100, 50))
        quote = sel.to_quote_data()
        self.assertEqual(quote["text"], "Wichtiges Zitat")
        self.assertEqual(quote["page"], 3)

    def test_statistics_defaults(self):
        from models import Statistics
        stats = Statistics()
        self.assertEqual(stats.total_sources, 0)
        self.assertEqual(stats.total_notes, 0)

    def test_statistics_to_dict(self):
        from models import Statistics
        stats = Statistics(total_sources=10, total_notes=5, total_quotes=3)
        d = stats.to_dict()
        self.assertEqual(d["Quellen"], 10)
        self.assertEqual(d["Notizen"], 5)
        self.assertEqual(d["Zitate"], 3)

    def test_all_exports(self):
        from models import __all__
        expected = ["SearchResult", "ExportOptions", "ImportResult", "PDFSelection", "Statistics"]
        for name in expected:
            self.assertIn(name, __all__)


if __name__ == "__main__":
    unittest.main()
