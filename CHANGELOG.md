# Changelog / Aenderungsprotokoll

Alle wesentlichen Aenderungen an diesem Projekt werden hier dokumentiert.
Format basiert auf [Keep a Changelog](https://keepachangelog.com/de/1.1.0/).

## [Unreleased]

### Hinzugefuegt / Added
- Smoke-Tests fuer Core-Module (tests/test_smoke.py, 10 Tests: EventType, SearchResult, ExportOptions, ImportResult, PDFSelection, Statistics)
- Ollama-Modellauswahl: ComboBox wird automatisch mit verfuegbaren Modellen befuellt (_fetch_ollama_models, _populate_model_combo)
- "Modelle laden" Button neben "Verbindung testen" im Einstellungen-Dialog

### Geaendert / Changed
- Verbindungstest aktualisiert ComboBox automatisch bei Erfolg (Ollama)

### Behoben / Fixed
- Bare except in settings_manager.py, project_tree.py, ollama_queue.py, bibtex.py, extractor.py, sync/__init__.py durch spezifische Exceptions ersetzt
- TODO-Stellen in detail_panel.py und summaries_tab.py aufgeraeumt

## [1.0.0] - 2026-01-01

### Hinzugefuegt / Added
- Erstveroeffentlichung / Initial release
- Ordnerbasiertes Literaturverwaltungssystem
- Eigene Dateiformate: .liproj, .limeta, .linote, .liquote, .litask, .lisum
- PDF-Integration (PyMuPDF), BibTeX-Export, Ollama KI-Integration (optional)
