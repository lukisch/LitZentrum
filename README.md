# LitZentrum

**Folder-Based Literature Management**

A desktop application for managing academic literature with a local storage format, PDF integration, and optional AI support.

## Features

- 📚 **Folder-Based System**: Each source in its own folder
- 📄 **PDF Integration**: Full-text search, text extraction
- 📝 **Notes & Quotes**: Page references, tags, categories
- ✅ **Task Management**: Per-source and project-wide tasks
- 📋 **Summaries**: Manual or AI-generated
- 📚 **Bibliography**: BibTeX export, multiple citation styles
- 🤖 **AI Integration**: Local processing with Ollama (optional)
- 🔄 **Git Integration**: Project versioning

## Screenshots

![Main Window](screenshots/main.png)

## Installation

```bash
# Clone the repository
cd LitZentrum

# Install dependencies
pip install -r requirements.txt

# Start
python src/main.py
```

## Dependencies

- Python 3.10+
- PyQt6
- PyMuPDF (fitz)
- bibtexparser
- jsonschema
- requests (for Ollama)

## Project Structure

```
LitZentrum/
├── src/
│   ├── main.py                 # Entry point
│   ├── core/                   # Core logic
│   │   ├── project_manager.py  # Project management
│   │   ├── source_manager.py   # Source management
│   │   ├── event_bus.py        # Event system
│   │   └── settings_manager.py # Settings
│   ├── formats/                # File formats
│   │   ├── limeta.py          # Metadata
│   │   ├── linote.py          # Notes
│   │   ├── liquote.py         # Quotes
│   │   ├── litask.py          # Tasks
│   │   └── lisum.py           # Summaries
│   ├── gui/                    # User interface
│   │   ├── main_window.py
│   │   ├── panels/
│   │   ├── tabs/
│   │   └── dialogs/
│   └── modules/                # Extensions
│       ├── bibliography/       # BibTeX & styles
│       ├── pdf_workshop/       # PDF processing
│       ├── ai/                 # Ollama integration
│       └── sync/               # Git & backup
├── schemas/                    # JSON schemas
├── tests/                      # Unit tests
└── resources/                  # Icons etc.
```

## File Formats

All data is stored as JSON:

| Format | Description |
|--------|-------------|
| `.liproj` | Project configuration |
| `.limeta` | Source metadata |
| `.linote` | Notes |
| `.liquote` | Quotes |
| `.litask` | Tasks |
| `.lisum` | Summaries |

## Project Layout

```
MyProject/
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

## Citation Styles

- APA (7th Edition)
- MLA (9th Edition)
- Chicago
- DIN 1505-2
- Harvard

## AI Integration (Optional)

For local AI features, Ollama is used:

```bash
# Install Ollama (https://ollama.ai)
ollama run mistral
```

Features:
- Automatic summaries
- Quote extraction
- Metadata detection

## License

AGPL v3 - See [LICENSE](LICENSE)

This project uses PyQt6 (GPL) and PyMuPDF (AGPL).

## Version

1.0.0 (January 2026)

---

Deutsche Version: [README.de.md](README.de.md)
