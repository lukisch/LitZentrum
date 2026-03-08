# 📦 LitZentrum Suite – Final Documentation

## 1. Überblick

**Kurzbeschreibung:**  
LitZentrum ist eine ordnerbasierte Literaturverwaltung für wissenschaftliche Arbeiten mit PDF-Integration, Notizen, Zitaten, Aufgaben, Zusammenfassungen und optionaler KI-Unterstützung.

| Feld | Wert |
|------|------|
| **Version** | 1.0.0 |
| **Stand** | 2026-01-09 |
| **Status** | MVP Ready (100%) |
| **Sprache** | Python 3.10+ |
| **Framework** | PyQt6 |
| **Codebase** | ~5.700 Zeilen / 50 Dateien |

---

## 2. Herkunft & Fusion

### 2.1 Ursprungstools

| Tool | Version | Reifegrad | Kernfunktion |
|------|---------|-----------|--------------|
| ProFiler | V14 | 85% | Datei-Index, SQLite, Hash |
| PDFSchwärzer Pro | V2.5 | 85% | PDF-Verarbeitung, OCR |
| pdfmarker2000 | - | 80% | Seiten markieren/extrahieren |
| PDFtoPDFocr | - | 75% | OCR für PDFs |
| PDFunlock | - | 80% | PDF entsperren |
| ProSync | V3.1 | 85% | Backup, Git-Integration |

### 2.2 Fusionsziel

> **"Ordnerbasierte Literaturverwaltung mit lokalem Speicherformat"**

Die Suite vereint Quellenverwaltung, PDF-Werkstatt, Notizen, Zitate, Aufgaben und Bibliografie-Export in einer Anwendung - ohne Cloud-Abhängigkeit.

### 2.3 Synergien

| Synergie | Beschreibung |
|----------|--------------|
| 📁 **Folder-based** | Jede Quelle = eigener Ordner mit allen Daten |
| 📄 **PDF + Notes** | Markierungen direkt zu Zitaten konvertieren |
| 📚 **Bibliografie** | Automatischer BibTeX-Export, mehrere Stile |
| 🤖 **AI Optional** | Lokale KI (Ollama) für Zusammenfassungen |
| 🔄 **Git-Ready** | Versionierung der Projekte möglich |

---

## 3. Features

### 3.1 Hauptfunktionen

| Bereich | Icon | Features |
|---------|------|----------|
| **Projektverwaltung** | 📚 | Mehrere Projekte, Projektbaum |
| **Quellenverwaltung** | 📄 | Metadaten, Status, Tags |
| **PDF-Integration** | 📖 | Viewer, Textextraktion, OCR |
| **Notizen** | 📝 | Seitenreferenz, Tags, Markdown |
| **Zitate** | 💬 | Direkt/Indirekt, Seitenangabe |
| **Aufgaben** | ✅ | Pro Quelle + Projektebene |
| **Zusammenfassungen** | 📋 | Manuell oder KI-generiert |
| **Bibliografie** | 📚 | BibTeX, APA, MLA, Chicago, DIN |

### 3.2 Datei-Formate (JSON-basiert)

| Format | Extension | Beschreibung |
|--------|-----------|--------------|
| Projekt | `.liproj` | Projektkonfiguration |
| Metadaten | `.limeta` | Quellen-Metadaten |
| Notizen | `.linote` | Notizen mit Seitenreferenz |
| Zitate | `.liquote` | Direkte/indirekte Zitate |
| Aufgaben | `.litask` | To-Do-Listen |
| Zusammenfassungen | `.lisum` | Manuelle/KI-Summaries |

### 3.3 Zitationsstile

- **APA** (7th Edition)
- **MLA** (9th Edition)
- **Chicago**
- **DIN 1505-2**
- **Harvard**

### 3.4 PDF-Werkstatt

- PDF-Viewer mit Navigation
- Textextraktion
- OCR (Tesseract)
- Markierung → Zitat Workflow
- Seiten extrahieren

---

## 4. Architektur

### 4.1 Layer-Modell

```
┌─────────────────────────────────────────────────────────────────┐
│                         GUI Layer                                │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │ MainWindow  │  │   Panels    │  │        Tabs             │  │
│  │             │  │ ProjectTree │  │  PDF, Notes, Quotes     │  │
│  │             │  │ SourceList  │  │  Tasks, Summaries       │  │
│  │             │  │ DetailPanel │  │                         │  │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘  │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                       Dialogs                                ││
│  │  NewProject, Source, Quote, Bibliography, Settings, AIQueue ││
│  └─────────────────────────────────────────────────────────────┘│
├─────────────────────────────────────────────────────────────────┤
│                       Core Layer                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌───────────────┐   │
│  │ Project  │  │ Source   │  │ Format   │  │  EventBus     │   │
│  │ Manager  │  │ Manager  │  │ Handler  │  │               │   │
│  │          │  │          │  │          │  │  Signals      │   │
│  └──────────┘  └──────────┘  └──────────┘  └───────────────┘   │
├─────────────────────────────────────────────────────────────────┤
│                      Module Layer                                │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌───────────────┐   │
│  │Bibliogra-│  │ PDF      │  │   AI     │  │    Sync       │   │
│  │  phy     │  │ Workshop │  │ (Ollama) │  │  (Git/Backup) │   │
│  │          │  │          │  │          │  │               │   │
│  └──────────┘  └──────────┘  └──────────┘  └───────────────┘   │
├─────────────────────────────────────────────────────────────────┤
│                       Data Layer                                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Projekt_A/                                               │   │
│  │  ├── projekt_config.liproj                                │   │
│  │  ├── projekt_tasks.litask                                 │   │
│  │  └── Quellen/                                             │   │
│  │      └── Smith2023_AI/                                    │   │
│  │          ├── source.pdf   ├── meta.limeta                 │   │
│  │          ├── notes.linote ├── quotes.liquote              │   │
│  │          ├── tasks.litask └── summaries.lisum             │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### 4.2 Module

| Modul | Pfad | Beschreibung |
|-------|------|--------------|
| **ProjectManager** | `core/project_manager.py` | Projektverwaltung |
| **SourceManager** | `core/source_manager.py` | Quellenverwaltung |
| **EventBus** | `core/event_bus.py` | Event-System |
| **SettingsManager** | `core/settings_manager.py` | Einstellungen |
| **FormatHandler** | `formats/*.py` | JSON-Formate (6 Typen) |
| **BibTeX** | `modules/bibliography/bibtex.py` | BibTeX Export |
| **Styles** | `modules/bibliography/styles.py` | Zitationsstile |
| **PDFExtractor** | `modules/pdf_workshop/extractor.py` | Text-Extraktion |
| **OllamaQueue** | `modules/ai/ollama_queue.py` | KI Job-Queue |

### 4.3 Datenfluss

```
Projekt öffnen → Quellen laden → Quelle auswählen
       ↓
Detail-Panel zeigt Tabs (PDF, Notes, Quotes, Tasks, Summaries)
       ↓
Bearbeitung → JSON speichern → EventBus benachrichtigt UI
```

---

## 5. Projektstruktur

```
LitZentrum/
├── README.md
├── requirements.txt
├── setup.py
├── start.bat
│
├── schemas/                    # JSON-Schemas
│   ├── limeta.schema.json
│   ├── linote.schema.json
│   ├── liquote.schema.json
│   ├── litask.schema.json
│   ├── lisum.schema.json
│   └── liproj.schema.json
│
├── src/
│   ├── main.py                 # Einstiegspunkt
│   │
│   ├── core/                   # Kernlogik
│   │   ├── __init__.py
│   │   ├── project_manager.py
│   │   ├── source_manager.py
│   │   ├── event_bus.py
│   │   └── settings_manager.py
│   │
│   ├── formats/                # Datei-Formate
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── limeta.py
│   │   ├── linote.py
│   │   ├── liquote.py
│   │   ├── litask.py
│   │   ├── lisum.py
│   │   └── liproj.py
│   │
│   ├── models/                 # Datenmodelle
│   │   └── __init__.py
│   │
│   ├── gui/                    # Benutzeroberfläche
│   │   ├── __init__.py
│   │   ├── main_window.py
│   │   │
│   │   ├── panels/             # 3-Panel-Layout
│   │   │   ├── project_tree.py
│   │   │   ├── source_list.py
│   │   │   └── detail_panel.py
│   │   │
│   │   ├── tabs/               # Detail-Tabs
│   │   │   ├── pdf_tab.py
│   │   │   ├── notes_tab.py
│   │   │   ├── quotes_tab.py
│   │   │   ├── tasks_tab.py
│   │   │   └── summaries_tab.py
│   │   │
│   │   ├── dialogs/
│   │   │   ├── new_project_dialog.py
│   │   │   ├── source_dialog.py
│   │   │   └── settings_dialog.py
│   │   │
│   │   └── widgets/
│   │       └── pdf_viewer.py
│   │
│   └── modules/                # Erweiterungen
│       ├── bibliography/
│       │   ├── bibtex.py
│       │   └── styles.py
│       │
│       ├── pdf_workshop/
│       │   └── extractor.py
│       │
│       ├── ai/
│       │   └── ollama_queue.py
│       │
│       └── sync/
│           └── __init__.py
│
├── tests/
│   └── test_formats.py
│
└── resources/icons/
```

---

## 6. Datenformate & Datenbanken

### 6.1 Formate

| Format | Verwendung |
|--------|------------|
| **JSON** | Alle Datenformate (.li*) |
| **SQLite** | Optional für Index (ProFiler) |
| **BibTeX** | Export für LaTeX |

### 6.2 Projekt-Aufbau

```
MeinProjekt/
├── projekt_config.liproj       # Projekt-Einstellungen
├── projekt_tasks.litask        # Projektweite Aufgaben
├── projekt_notes.linote        # Projektweite Notizen
├── projekt_biblio.bib          # Generiertes Literaturverzeichnis
│
└── Quellen/
    ├── Smith2023_Understanding_AI/
    │   ├── source.pdf          # Original-PDF
    │   ├── meta.limeta         # Metadaten
    │   ├── notes.linote        # Notizen
    │   ├── quotes.liquote      # Zitate
    │   ├── tasks.litask        # Aufgaben
    │   └── summaries.lisum     # Zusammenfassungen
    │
    └── Doe2024_Machine_Learning/
        └── ...
```

### 6.3 Beispiel: meta.limeta

```json
{
  "schema_version": "1.0",
  "id": "src_001",
  "title": "Understanding Artificial Intelligence",
  "authors": [
    {"given": "John", "family": "Smith"}
  ],
  "year": 2023,
  "type": "article",
  "journal": "AI Research Journal",
  "volume": "15",
  "issue": "3",
  "pages": "123-145",
  "doi": "10.1234/example",
  "tags": ["AI", "Machine Learning"],
  "status": "read",
  "rating": 4
}
```

---

## 7. Workflows

### 7.1 Hauptworkflow

```
Projekt erstellen → Quellen hinzufügen → PDF lesen → Notizen/Zitate
       ↓
Aufgaben verwalten → Zusammenfassungen erstellen
       ↓
Bibliografie exportieren (BibTeX, APA, MLA...)
```

### 7.2 Markierung → Zitat Workflow

```
PDF öffnen → Text markieren → Rechtsklick: "Als Zitat übernehmen"
       ↓
QuoteDialog öffnet sich:
  - Text (automatisch gefüllt)
  - Seite (automatisch erkannt)
  - Typ wählen (direkt/indirekt)
  - Tags hinzufügen
  - Kommentar
       ↓
quotes.liquote wird aktualisiert
```

### 7.3 KI-Queue System (Optional)

```
Zusammenfassung anfordern → Job in Queue → Ollama verarbeitet
       ↓
Ergebnis in summaries.lisum gespeichert:
{
  "id": "s002",
  "source": "ai_ollama_mistral",
  "scope": "full_document",
  "text": "- Punkt 1...\n- Punkt 2...",
  "model": "mistral:latest"
}
```

---

## 8. Installation & Setup

### 8.1 Voraussetzungen

| Anforderung | Version |
|-------------|---------|
| Python | 3.10+ |
| OS | Windows/Linux/macOS |
| Ollama | Optional (für KI) |

### 8.2 Installation

```bash
# Ordner öffnen
cd "C:\Users\User\OneDrive\.SOFTWARE\SUITEN\LitZentrum"

# Abhängigkeiten installieren
pip install -r requirements.txt

# Starten
python src/main.py
# oder
start.bat
```

### 8.3 Abhängigkeiten

```
PyQt6>=6.4.0
PyMuPDF>=1.23.0
bibtexparser>=1.4.0
jsonschema>=4.17.0
requests>=2.28.0       # Für Ollama
```

### 8.4 Ollama Setup (Optional)

```bash
# Ollama installieren (https://ollama.ai)
ollama run mistral
```

---

## 9. Build & Deployment

### 9.1 PyInstaller

```bash
pyinstaller --onefile --windowed --icon=resources/icons/litzentrum.ico src/main.py
```

---

## 10. Tests

```bash
# Unit-Tests
python -m pytest tests/ -v

# Format-Tests
python tests/test_formats.py
```

---

## 11. Changelog

### 11.1 Zusammenfassung

| Datum | Version | Änderung |
|-------|---------|----------|
| 03.01.2026 | V1.0 | MVP implementiert |
| 09.01.2026 | V1.0 | Dokumentation finalisiert |

### 11.2 Statistiken

- **Dateien:** ~50
- **Zeilen:** ~5.700
- **Module:** 4 (Core, Formats, GUI, Modules)
- **Datei-Formate:** 6 (.li*)

---

## 12. Roadmap

### ✅ Erledigt

- [x] Projektverwaltung (erstellen, öffnen, Recent)
- [x] Quellenverwaltung (hinzufügen, Metadaten, Status)
- [x] JSON-Formate (6 Typen mit Schemas)
- [x] 3-Panel-Layout (Projektbaum, Liste, Details)
- [x] 5 Detail-Tabs (PDF, Notes, Quotes, Tasks, Summaries)
- [x] PDF-Viewer mit Navigation
- [x] Bibliografie-Export (BibTeX + 5 Stile)
- [x] Ollama KI-Integration (optional)

### 🔮 Zukunft

- [ ] PDF-Annotationen
- [ ] DOI/ISBN Lookup (CrossRef, OpenLibrary)
- [ ] Erweiterte Suche über alle Projekte
- [ ] Zotero/Mendeley Import

---

## 13. Lizenz

**MIT License**

---

## 14. Tastenkürzel

| Kürzel | Funktion |
|--------|----------|
| `Ctrl+N` | Neues Projekt |
| `Ctrl+O` | Projekt öffnen |
| `Ctrl+S` | Speichern |
| `Ctrl+Shift+N` | Neue Quelle |
| `Ctrl+F` | Suchen |
| `Ctrl+E` | Bibliografie exportieren |
| `F5` | Aktualisieren |

---

## 15. UI-Layout

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              LitZentrum                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│  [Datei] [Bearbeiten] [Ansicht] [Quellen] [Export] [KI] [Hilfe]            │
├─────────────────────────────────────────────────────────────────────────────┤
│  [📂 Neues Projekt] [➕ Quelle] [🔍 Suche] [📖 Bibliografie] [⚙️]          │
├───────────────┬─────────────────────────────┬───────────────────────────────┤
│               │                             │                               │
│  PROJEKTBAUM  │      QUELLEN-LISTE          │       DETAIL-PANEL            │
│               │                             │                               │
│  📚 Projekte  │  ┌─────────────────────┐    │  ┌─────────────────────────┐ │
│  ├─📁 Master- │  │Quelle     │Status  │    │  │      METADATEN          │ │
│  │  arbeit    │  ├───────────┼────────┤    │  │                         │ │
│  │  ├─📄Smith │  │Smith2023  │ ✅ Done│    │  │  Titel: Understanding.. │ │
│  │  ├─📄Müller│  │Müller2022 │ ⏳ Read│    │  │  Autor: Smith, John     │ │
│  │  └─📄Weber │  │Weber2021  │ 📝 Note│    │  │  Jahr:  2023            │ │
│  │            │  └───────────┴────────┘    │  │  DOI:   10.1234/...     │ │
│  ├─📁 Haus-   │                             │  │  Tags:  [AI] [Methodik] │ │
│  │  arbeit    │  Filter: [Alle ▼]          │  │                         │ │
│  │            │  Sortierung: [Name ▼]      │  │  [Bearbeiten] [Öffnen]  │ │
│  └─📁 Seminar │                             │  └─────────────────────────┘ │
│               │                             │                               │
│  ─────────────│                             │  ┌─────────────────────────┐ │
│  ⭐ Favoriten │                             │  │ [PDF][Notizen][Zitate]  │ │
│  🏷️ Tags      │                             │  │ [Aufgaben][Summaries]   │ │
│  📊 Statistik │                             │  ├─────────────────────────┤ │
│               │                             │  │                         │ │
│               │                             │  │  📝 Notizen (3)         │ │
│               │                             │  │  ├─ n001: Wichtige...   │ │
│               │                             │  │  ├─ n002: Vergleich...  │ │
│               │                             │  │  └─ n003: TODO: ...     │ │
│               │                             │  │                         │ │
│               │                             │  │  [+ Neue Notiz]         │ │
│               │                             │  └─────────────────────────┘ │
├───────────────┴─────────────────────────────┴───────────────────────────────┤
│  Status: 📚 3 Projekte │ 📄 12 Quellen │ 📝 45 Zitate │ KI: 🟢 Bereit       │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

*Generiert: 2026-01-09 | LitZentrum Suite | ~5.700 Zeilen / 50 Dateien*
