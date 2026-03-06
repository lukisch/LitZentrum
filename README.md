# LitZentrum

**Ordnerbasierte Literaturverwaltung**

Eine Desktop-Anwendung zur Verwaltung wissenschaftlicher Literatur mit lokalem Speicherformat, PDF-Integration und optionaler KI-Unterstützung.

## Features

- 📚 **Ordnerbasiertes System**: Jede Quelle in eigenem Ordner
- 📄 **PDF-Integration**: Volltextsuche, Textextraktion
- 📝 **Notizen & Zitate**: Seitenreferenzen, Tags, Kategorien
- ✅ **Aufgabenverwaltung**: Pro Quelle und projektweite Tasks
- 📋 **Zusammenfassungen**: Manuell oder KI-generiert
- 📚 **Bibliografie**: BibTeX-Export, mehrere Zitationsstile
- 🤖 **KI-Integration**: Lokale Verarbeitung mit Ollama (optional)
- 🔄 **Git-Integration**: Versionierung der Projekte

## Screenshots

![Hauptfenster](screenshots/main.png)

## Installation

```bash
# Repository klonen
cd LitZentrum

# Abhängigkeiten installieren
pip install -r requirements.txt

# Starten
python src/main.py
```

## Abhängigkeiten

- Python 3.10+
- PyQt6
- PyMuPDF (fitz)
- bibtexparser
- jsonschema
- requests (für Ollama)

## Projektstruktur

```
LitZentrum/
├── src/
│   ├── main.py                 # Einstiegspunkt
│   ├── core/                   # Kernlogik
│   │   ├── project_manager.py  # Projektverwaltung
│   │   ├── source_manager.py   # Quellenverwaltung
│   │   ├── event_bus.py        # Event-System
│   │   └── settings_manager.py # Einstellungen
│   ├── formats/                # Datei-Formate
│   │   ├── limeta.py          # Metadaten
│   │   ├── linote.py          # Notizen
│   │   ├── liquote.py         # Zitate
│   │   ├── litask.py          # Aufgaben
│   │   └── lisum.py           # Zusammenfassungen
│   ├── gui/                    # Benutzeroberfläche
│   │   ├── main_window.py
│   │   ├── panels/
│   │   ├── tabs/
│   │   └── dialogs/
│   └── modules/                # Erweiterungen
│       ├── bibliography/       # BibTeX & Stile
│       ├── pdf_workshop/       # PDF-Verarbeitung
│       ├── ai/                 # Ollama-Integration
│       └── sync/               # Git & Backup
├── schemas/                    # JSON-Schemas
├── tests/                      # Unit-Tests
└── resources/                  # Icons etc.
```

## Datei-Formate

Alle Daten werden als JSON gespeichert:

| Format | Beschreibung |
|--------|-------------|
| `.liproj` | Projektkonfiguration |
| `.limeta` | Quellen-Metadaten |
| `.linote` | Notizen |
| `.liquote` | Zitate |
| `.litask` | Aufgaben |
| `.lisum` | Zusammenfassungen |

## Projekt-Aufbau

```
MeinProjekt/
├── projekt_config.liproj
├── projekt_tasks.litask
├── projekt_notes.linote
├── Quellen/
│   ├── Smith2023_Understanding_AI/
│   │   ├── meta.limeta
│   │   ├── notes.linote
│   │   ├── quotes.liquote
│   │   ├── tasks.litask
│   │   ├── summaries.lisum
│   │   └── source.pdf
│   └── Doe2024_Machine_Learning/
│       └── ...
```

## Zitationsstile

- APA (7th Edition)
- MLA (9th Edition)
- Chicago
- DIN 1505-2
- Harvard

## KI-Integration (Optional)

Für lokale KI-Funktionen wird Ollama verwendet:

```bash
# Ollama installieren (https://ollama.ai)
ollama run mistral
```

Funktionen:
- Automatische Zusammenfassungen
- Zitat-Extraktion
- Metadaten-Erkennung

## Lizenz

AGPL v3 - Siehe [LICENSE](LICENSE)

Dieses Projekt verwendet PyQt6 (GPL) und PyMuPDF (AGPL).

## Version

1.0.0 (Januar 2026)

---

## English

A folder-based literature management system with PDF integration, notes, and optional AI support.

### Features

- Folder-based organization
- PDF viewer integration
- Note-taking
- Optional AI support
- Citation management

### Installation

```bash
git clone https://github.com/lukisch/REL-PUB_LitZentrum_SUITE.git
cd REL-PUB_LitZentrum_SUITE
pip install -r requirements.txt
python "src/main.py"
```

### License

See [LICENSE](LICENSE) for details.
