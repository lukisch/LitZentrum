"""
LitZentrum - Tests für Format-Klassen
"""
import sys
from pathlib import Path

# Pfad hinzufügen
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import unittest
import tempfile
import json


class TestLiMetaFormat(unittest.TestCase):
    """Tests für LiMeta"""
    
    def test_create_minimal(self):
        from formats import LiMeta
        
        meta = LiMeta(title="Test Article")
        self.assertEqual(meta.title, "Test Article")
        self.assertEqual(meta.authors, [])
        self.assertEqual(meta.schema_version, "1.0.0")
    
    def test_create_full(self):
        from formats import LiMeta
        
        meta = LiMeta(
            title="Understanding AI",
            authors=["Smith, John", "Doe, Jane"],
            year=2024,
            doi="10.1234/example",
            source_type="article",
        )
        
        self.assertEqual(meta.title, "Understanding AI")
        self.assertEqual(len(meta.authors), 2)
        self.assertEqual(meta.year, 2024)
        self.assertEqual(meta.first_author, "Smith")
    
    def test_citation_key(self):
        from formats import LiMeta
        
        meta = LiMeta(
            title="Test",
            authors=["Mueller, Hans"],
            year=2023,
        )
        
        self.assertEqual(meta.citation_key, "Mueller2023")
    
    def test_save_load(self):
        from formats import LiMeta
        
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "meta.limeta"
            
            original = LiMeta(
                title="Test Article",
                authors=["Author One"],
                year=2024,
                tags=["test", "example"],
            )
            original.save(path)
            
            # Datei existiert
            self.assertTrue(path.exists())
            
            # Laden
            loaded = LiMeta.load(path)
            self.assertEqual(loaded.title, original.title)
            self.assertEqual(loaded.authors, original.authors)
            self.assertEqual(loaded.year, original.year)
            self.assertEqual(loaded.tags, original.tags)


class TestLiNoteFormat(unittest.TestCase):
    """Tests für LiNote"""
    
    def test_create_empty(self):
        from formats import LiNote
        
        notes = LiNote()
        self.assertEqual(len(notes), 0)
    
    def test_add_notes(self):
        from formats import LiNote
        
        notes = LiNote()
        notes.add("Erste Notiz", page=1, tags=["wichtig"])
        notes.add("Zweite Notiz", page=5)
        
        self.assertEqual(len(notes), 2)
        self.assertEqual(notes.notes[0].content, "Erste Notiz")
        self.assertEqual(notes.notes[0].page, 1)
    
    def test_get_by_page(self):
        from formats import LiNote
        
        notes = LiNote()
        notes.add("Seite 1", page=1)
        notes.add("Seite 5", page=5)
        notes.add("Auch Seite 1", page=1)
        
        page1_notes = notes.get_by_page(1)
        self.assertEqual(len(page1_notes), 2)


class TestLiQuoteFormat(unittest.TestCase):
    """Tests für LiQuote"""
    
    def test_add_quotes(self):
        from formats import LiQuote
        
        quotes = LiQuote()
        quotes.add("Direktes Zitat", page=10, quote_type="direct")
        quotes.add("Indirektes Zitat", page=15, quote_type="indirect")
        
        self.assertEqual(len(quotes), 2)
        
        direct = quotes.get_direct()
        self.assertEqual(len(direct), 1)


class TestLiTaskFormat(unittest.TestCase):
    """Tests für LiTask"""
    
    def test_add_tasks(self):
        from formats import LiTask
        
        tasks = LiTask()
        tasks.add("Kapitel 1 lesen", priority="high")
        tasks.add("Zusammenfassung schreiben", due_date="2024-12-31")
        
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks.open_count, 2)
    
    def test_complete_task(self):
        from formats import LiTask
        
        tasks = LiTask()
        tasks.add("Test Task")
        
        tasks.complete(tasks.tasks[0].id)
        
        self.assertEqual(tasks.tasks[0].status, "done")
        self.assertIsNotNone(tasks.tasks[0].completed_at)


class TestProjectManager(unittest.TestCase):
    """Tests für ProjectManager"""
    
    def test_create_project(self):
        from core import ProjectManager
        
        with tempfile.TemporaryDirectory() as tmpdir:
            pm = ProjectManager()
            
            project = pm.create_project(
                path=Path(tmpdir) / "TestProjekt",
                name="Test Projekt",
                description="Ein Testprojekt",
            )
            
            self.assertTrue(project.path.exists())
            self.assertTrue(project.sources_path.exists())
            self.assertTrue((project.path / "projekt_config.liproj").exists())
    
    def test_open_project(self):
        from core import ProjectManager
        
        with tempfile.TemporaryDirectory() as tmpdir:
            pm = ProjectManager()
            
            # Erstellen
            project = pm.create_project(
                path=Path(tmpdir) / "TestProjekt",
                name="Test Projekt",
            )
            
            pm.close_project()
            
            # Neu öffnen
            reopened = pm.open_project(project.path)
            self.assertEqual(reopened.name, "Test Projekt")


if __name__ == "__main__":
    unittest.main()
