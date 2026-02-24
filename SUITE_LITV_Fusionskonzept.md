# 📚 SUITE LITV - Fusionskonzept

## Übersicht

**Ziel:** Eine ordnerbasierte Literaturverwaltungssoftware basierend auf ProFiler, mit PDF-Werkstatt und optionaler KI-Integration.

---

## 📦 Enthaltene Tools

### Kern-Tools

| Tool | Funktion | Reifegrad | Zeilen |
|------|----------|-----------|--------|
| **ProFiler V14** | Datei-Index, Metadaten, Versionierung | 85% | 7575 |
| **MediaBrain** | Multi-Provider Medienverwaltung | 75% | ~1500 |
| **ProSync V3.1** | Sichere Datenbank-Synchronisation | 85% | 1764 |
| **ProfiPrompt** | Prompt/Notizen-Verwaltung | 80% | ~500 |

### TEXT-Module (PDF-Werkstatt)

| Modul | Funktion | Reifegrad |
|-------|----------|-----------|
| **PDFSchwärzer Pro V2.5** | PDF-Redaction mit Fuzzy-Match | 90% |
| **pdfmarker2000** | PDF-Markierung, Auszüge erstellen | 85% |
| **PDFtoPDFocr** | OCR für PDFs | 80% |
| **PDFunlock** | PDF-Entsperrung | 85% |
| **FormConstructor V1.5** | Formular-Builder | 80% |
| **DokuReader** | Basis-Dokumentleser | 75% |
| **TxtSpawner** | Text aus Zwischenablage | 80% |
| **TextPool** | Text-Pooling | 75% |
| **StapelKönig** | Stapelverarbeitung | 70% |
| **logtotxt** | Log-Konvertierung | 100% |
| **pyCuttertxt** | Code-Extraktor | 75% |

---

## 🎯 Fusionskonzept: "LitZentrum"

### Vision (basierend auf LIT-Konzept.html)

**Ordner = Projekt, Pro Quelle ein Ordner** - Ein durchschaubares, lokales Literaturverwaltungssystem:

- Keine versteckten Datenbanken
- Textbasierte Dateiformate (JSON)
- Kompatibel mit DokuZentrum/ProFiler
- Optionale Ollama/KI-Integration

### Dateistruktur pro Projekt

```
Projekt_Masterarbeit/
├── Quellen/
│   ├── Smith2023_AI_Study/
│   │   ├── source.pdf              # Originalquelle
│   │   ├── meta.limeta             # Metadaten (JSON)
│   │   ├── notes.linote            # Notizen (JSON)
│   │   ├── tasks.litask            # Aufgaben (JSON)
│   │   ├── summaries.lisum         # Zusammenfassungen
│   │   └── quotes.liquote          # Zitate
│   │
│   └── Mueller2022_Methodik/
│       └── ...
│
├── projekt_tasks.litask            # Projektweite Aufgaben
├── projekt_notes.linote            # Projektweite Notizen
├── projekt_biblio.bib              # Generiertes Literaturverzeichnis
└── projekt_config.liproj           # Projekteinstellungen
```

### Kernmodule

```
┌──────────────────────────────────────────────────────────────────────┐
│                          LitZentrum                                  │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │                      HAUPTFENSTER                              │ │
│  │  ┌────────────┬───────────────────┬─────────────────────────┐ │ │
│  │  │ PROJEKTBAUM│   QUELLEN-LISTE   │    DETAIL-PANEL         │ │ │
│  │  │            │                   │                         │ │ │
│  │  │ 📚 Projekte│ [Quelle] [Status] │ 📋 Metadaten           │ │ │
│  │  │ ├─Masterarb│ Smith2023   ✅    │ ├─ Titel, Autor, Jahr  │ │ │
│  │  │ │ └─Quellen│ Mueller2022 ⏳    │ ├─ DOI, ISBN           │ │ │
│  │  │ └─Hausarb. │ Weber2021   📝    │ └─ Tags                │ │ │
│  │  │            │                   │                         │ │ │
│  │  │ ⭐ Favoriten│                   │ 📝 Tabs:               │ │ │
│  │  │ 🏷️ Tags    │                   │ [Notizen][Zitate]      │ │ │
│  │  │            │                   │ [Aufgaben][Summaries]  │ │ │
│  │  └────────────┴───────────────────┴─────────────────────────┘ │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                                                                      │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────┐  │
│  │  PDF-WERKSTATT  │  │   INDEXER       │  │    KI-ASSISTANT     │  │
│  │  (TEXT-Module)  │  │  (ProFiler)     │  │    (Ollama/Queue)   │  │
│  │                 │  │                 │  │                     │  │
│  │ • Markieren     │  │ • Volltext      │  │ • Zusammenfassen    │  │
│  │ • Schwärzen     │  │ • Metadaten     │  │ • Exzerpieren       │  │
│  │ • Auszüge       │  │ • Hash/Versions │  │ • Zitate vorschlagen│  │
│  │ • OCR           │  │ • Duplikate     │  │ • ISBN-Lookup       │  │
│  │ • Entsperren    │  │ • Kategorien    │  │                     │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────────┘  │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                    EXPORT & BIBLIOGRAFIE                     │   │
│  │                                                              │   │
│  │  📖 BibTeX  │  📄 APA/MLA/DIN  │  📝 Word  │  📊 PDF        │   │
│  └──────────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 🏗️ Architektur

### Layer-Struktur

```
LitZentrum/
├── core/
│   ├── project_manager.py      # Projekt-Verwaltung
│   ├── source_manager.py       # Quellen-Verwaltung
│   ├── metadata_handler.py     # .limeta Parsing
│   ├── notes_handler.py        # .linote/.litask/.lisum/.liquote
│   └── profiler_bridge.py      # ProFiler-Integration
│
├── modules/
│   ├── pdf_workshop/           # TEXT-Module
│   │   ├── marker.py           # pdfmarker2000
│   │   ├── redactor.py         # PDFSchwärzer Pro
│   │   ├── ocr.py              # PDFtoPDFocr
│   │   ├── unlocker.py         # PDFunlock
│   │   └── extractor.py        # Auszüge erstellen
│   │
│   ├── bibliography/
│   │   ├── bibtex_gen.py       # BibTeX Generator
│   │   ├── citation_styles.py  # APA, MLA, DIN, etc.
│   │   └── word_export.py      # DOCX Export
│   │
│   ├── ai/                     # Optional
│   │   ├── ollama_queue.py     # KI-Warteschlange
│   │   ├── summarizer.py       # Zusammenfassungen
│   │   └── isbn_lookup.py      # ISBN/DOI Abfrage
│   │
│   └── sync/                   # ProSync
│       └── project_sync.py
│
├── gui/
│   ├── main_window.py
│   ├── project_tree.py
│   ├── source_list.py
│   ├── detail_panel.py
│   └── pdf_viewer.py
│
└── formats/                    # Dateiformat-Definitionen
    ├── limeta_schema.json
    ├── linote_schema.json
    ├── litask_schema.json
    ├── lisum_schema.json
    └── liquote_schema.json
```

---

## 📄 Dateiformate (aus LIT-Konzept)

### meta.limeta (Metadaten)
```json
{
  "title": "Understanding AI",
  "authors": ["Smith, John", "Doe, Anna"],
  "year": 2023,
  "doi": "10.1234/ai.2023.001",
  "isbn": "978-3-16-148410-0",
  "publisher": "Springer",
  "tags": ["AI", "Methodik"],
  "source_file": "source.pdf",
  "metadata_source": "manual|isbn_lookup|ai",
  "verified": false
}
```

### quotes.liquote (Zitate)
```json
[
  {
    "id": "q001",
    "type": "direct",
    "page": 12,
    "text": "Original quotation text.",
    "comment": "Gut für Einleitung.",
    "tags": ["intro", "definition"]
  }
]
```

---

## 🔄 Vergleich: Citavi vs. LitZentrum

| Aspekt | Citavi | LitZentrum |
|--------|--------|------------|
| Datenmodell | Proprietäre DB | Ordner + JSON |
| Komplexität | Sehr hoch | Minimal |
| PDF-Workflows | Begrenzt | Sehr stark (PDFSchwärzer etc.) |
| Wissenselemente | Zitate, Gedanken | Zitate, Notizen, Tasks, Summaries |
| Offline-First | Ja | Ja + transparente Struktur |
| Teamarbeit | Server/Cloud | Git, Cloud-Sync, Ordner-Sharing |
| KI-Integration | Keine | Ollama-Queue (optional) |
| Open Source | Nein | Ja |
| Kosten | ~300€ | Kostenlos |

---

## ⚡ Synergien

1. **ProFiler + Quellen:** Automatische Indizierung aller PDFs
2. **PDFSchwärzer + Zitate:** Markierte Stellen → Zitate
3. **OCR + Volltext:** Gescannte PDFs durchsuchbar
4. **ProSync + Projekte:** Sichere Backup-Synchronisation
5. **Ollama + Summaries:** KI-gestützte Zusammenfassungen
6. **ProfiPrompt + Notizen:** Recherche-Prompts speichern

---

## 🚀 Implementierungs-Roadmap

### Phase 1: Core (4 Wochen)
- [ ] Projektstruktur-Management
- [ ] Dateiformat-Handler (.limeta, .linote, etc.)
- [ ] ProFiler-Bridge für Index

### Phase 2: GUI (3 Wochen)
- [ ] Hauptfenster mit 3-Panel-Layout
- [ ] Projektbaum
- [ ] Quellen-Liste
- [ ] Detail-Panel mit Tabs

### Phase 3: PDF-Werkstatt (4 Wochen)
- [ ] PDFSchwärzer-Integration
- [ ] Marker-Integration
- [ ] OCR-Integration
- [ ] "Markierung → Zitat" Workflow

### Phase 4: Bibliografie (2 Wochen)
- [ ] BibTeX-Generator
- [ ] Zitationsstile (APA, MLA, DIN)
- [ ] Word-Export

### Phase 5: KI (optional, 3 Wochen)
- [ ] Ollama-Queue
- [ ] Automatische Summaries
- [ ] ISBN/DOI-Lookup via API

---

## ✅ Fazit

**Empfehlung: FUSION STARK EMPFOHLEN** ⭐⭐⭐⭐⭐

LitZentrum füllt eine echte Marktlücke:
- **Transparenter als Citavi:** Ordner + Dateien statt Black-Box
- **Stärkere PDF-Tools:** PDFSchwärzer Pro übertrifft Citavi
- **Kostenlos & Open Source:** Keine Lizenzkosten
- **KI-Ready:** Ollama-Integration vorbereitet

**Unique Selling Points:**
1. Ordnerbasiert = Git-kompatibel = Team-tauglich
2. Beste PDF-Redaction im Literatur-Bereich
3. Optionale lokale KI (Datenschutz!)
4. Durchschaubare JSON-Formate

**Geschätzter Aufwand:** 16 Wochen für MVP (ohne KI: 13 Wochen)
**Empfohlenes Framework:** PyQt6

**Wichtig:** Das LIT-Konzept.html enthält bereits eine durchdachte Spezifikation - diese sollte als Basis dienen!

---
*Analyse erstellt: 03.01.2026*


---

# 📋 DETAILLIERTER UMSETZUNGSPLAN

## 🎯 Projektziele & Scope

### MVP-Definition (Minimum Viable Product)
Das MVP umfasst:
- ✅ Projektstruktur (Ordner = Projekt, Unterordner = Quelle)
- ✅ Dateiformat-Handler (.limeta, .linote, .litask, .liquote, .lisum)
- ✅ GUI: Projektbaum + Quellen-Liste + Detail-Panel
- ✅ PDF-Vorschau mit Markierungs-Export
- ✅ Bibliografie-Export (BibTeX)
- ❌ KI-Integration (Phase 2)
- ❌ OCR für gescannte PDFs (Phase 2)

### Nicht-Ziele für MVP
- Keine Citavi-Import-Funktion
- Keine automatische Metadaten-Erkennung
- Keine Team-Synchronisation

### Design-Prinzipien (aus LIT-Konzept.html)
1. **Ordner = Projekt** - Keine versteckten Datenbanken
2. **Pro Quelle ein Ordner** - Alles zusammen
3. **JSON-basierte Formate** - Transparent und Git-kompatibel
4. **ProFiler als Engine** - Bewährte Index-Technologie
5. **Optionale KI** - Ollama für lokale Verarbeitung

---

## 📅 PHASE 1: Core & Dateiformate (Wochen 1-4)

### Woche 1: Projekt-Setup & Dateiformat-Definitionen

#### Tag 1-2: Repository & Struktur
```
LitZentrum/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── app.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── project_manager.py     # Projekt-CRUD
│   │   ├── source_manager.py      # Quellen-CRUD
│   │   ├── settings_manager.py
│   │   └── profiler_bridge.py     # ProFiler-Integration
│   │
│   ├── formats/
│   │   ├── __init__.py
│   │   ├── base_format.py         # Basis-Klasse
│   │   ├── limeta.py              # Metadaten
│   │   ├── linote.py              # Notizen
│   │   ├── litask.py              # Aufgaben
│   │   ├── liquote.py             # Zitate
│   │   └── lisum.py               # Zusammenfassungen
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── project.py
│   │   ├── source.py
│   │   ├── note.py
│   │   ├── task.py
│   │   ├── quote.py
│   │   └── summary.py
│   │
│   ├── gui/
│   │   ├── __init__.py
│   │   ├── main_window.py
│   │   ├── panels/
│   │   │   ├── project_tree.py
│   │   │   ├── source_list.py
│   │   │   └── detail_panel.py
│   │   ├── tabs/
│   │   │   ├── notes_tab.py
│   │   │   ├── quotes_tab.py
│   │   │   ├── tasks_tab.py
│   │   │   └── summaries_tab.py
│   │   └── dialogs/
│   │
│   └── modules/
│       ├── pdf_workshop/          # TEXT-Module
│       │   ├── marker.py
│       │   ├── redactor.py
│       │   ├── ocr.py
│       │   └── extractor.py
│       ├── bibliography/
│       │   ├── bibtex.py
│       │   ├── styles.py
│       │   └── exporter.py
│       ├── ai/                    # Phase 2
│       │   ├── ollama_queue.py
│       │   └── summarizer.py
│       └── sync/
│           └── project_sync.py
│
├── schemas/                       # JSON Schemas
│   ├── limeta.schema.json
│   ├── linote.schema.json
│   ├── litask.schema.json
│   ├── liquote.schema.json
│   └── lisum.schema.json
│
├── resources/
│   ├── icons/
│   ├── themes/
│   └── citation_styles/
│
├── tests/
└── requirements.txt
```

**Tasks:**
- [ ] Git Repository initialisieren
- [ ] Ordnerstruktur anlegen
- [ ] requirements.txt erstellen
- [ ] JSON Schemas definieren

**Deliverable:** Strukturiertes Projekt mit Schema-Definitionen

#### Tag 3-5: Dateiformate implementieren
```python
# src/formats/base_format.py
from abc import ABC, abstractmethod
from pathlib import Path
import json
from datetime import datetime

class LitFormat(ABC):
    """Basis-Klasse für alle LitZentrum Dateiformate"""
    
    EXTENSION: str = ""
    SCHEMA_VERSION: str = "1.0"
    
    def __init__(self, file_path: Path = None):
        self.file_path = file_path
        self.data = self._default_data()
        self._modified = False
    
    @abstractmethod
    def _default_data(self) -> dict:
        """Standard-Datenstruktur"""
        pass
    
    def load(self, file_path: Path = None):
        """Lädt Daten aus Datei"""
        path = file_path or self.file_path
        if path and path.exists():
            with open(path, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            self.file_path = path
        self._modified = False
    
    def save(self, file_path: Path = None):
        """Speichert Daten in Datei"""
        path = file_path or self.file_path
        if not path:
            raise ValueError("Kein Dateipfad angegeben")
        
        self.data['_schema_version'] = self.SCHEMA_VERSION
        self.data['_modified_at'] = datetime.now().isoformat()
        
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
        
        self.file_path = path
        self._modified = False
    
    @property
    def is_modified(self) -> bool:
        return self._modified


# src/formats/limeta.py
class LiMeta(LitFormat):
    """Metadaten einer Quelle (.limeta)"""
    
    EXTENSION = ".limeta"
    
    def _default_data(self) -> dict:
        return {
            "title": "",
            "authors": [],
            "year": None,
            "doi": "",
            "isbn": "",
            "publisher": "",
            "journal": "",
            "volume": "",
            "issue": "",
            "pages": "",
            "abstract": "",
            "url": "",
            "tags": [],
            "source_file": "",
            "source_type": "article",  # article, book, chapter, website, etc.
            "metadata_source": "manual",  # manual, isbn_lookup, doi_lookup, ai
            "verified": False,
            "notes": ""
        }
    
    @property
    def title(self) -> str:
        return self.data.get("title", "")
    
    @title.setter
    def title(self, value: str):
        self.data["title"] = value
        self._modified = True
    
    @property
    def authors(self) -> list:
        return self.data.get("authors", [])
    
    def add_author(self, name: str, position: int = None):
        if position is None:
            self.data["authors"].append(name)
        else:
            self.data["authors"].insert(position, name)
        self._modified = True
    
    def to_bibtex(self) -> str:
        """Generiert BibTeX-Eintrag"""
        bib_type = self._get_bibtex_type()
        key = self._generate_key()
        
        fields = []
        if self.data.get("title"):
            fields.append(f'  title = {{{self.data["title"]}}}')
        if self.data.get("authors"):
            fields.append(f'  author = {{{" and ".join(self.data["authors"])}}}')
        if self.data.get("year"):
            fields.append(f'  year = {{{self.data["year"]}}}')
        # ... weitere Felder
        
        return f"@{bib_type}{{{key},\n" + ",\n".join(fields) + "\n}"


# src/formats/linote.py
class LiNote(LitFormat):
    """Notizen zu einer Quelle (.linote)"""
    
    EXTENSION = ".linote"
    
    def _default_data(self) -> dict:
        return {
            "notes": []
        }
    
    def add_note(self, text: str, tags: list = None, page: int = None) -> str:
        """Fügt neue Notiz hinzu, gibt ID zurück"""
        note_id = f"n{len(self.data['notes']) + 1:03d}"
        
        note = {
            "id": note_id,
            "text": text,
            "tags": tags or [],
            "page": page,
            "created_at": datetime.now().isoformat(),
            "modified_at": datetime.now().isoformat()
        }
        
        self.data["notes"].append(note)
        self._modified = True
        return note_id
    
    def get_note(self, note_id: str) -> dict:
        for note in self.data["notes"]:
            if note["id"] == note_id:
                return note
        return None
    
    def update_note(self, note_id: str, text: str = None, tags: list = None):
        for note in self.data["notes"]:
            if note["id"] == note_id:
                if text is not None:
                    note["text"] = text
                if tags is not None:
                    note["tags"] = tags
                note["modified_at"] = datetime.now().isoformat()
                self._modified = True
                return
    
    def delete_note(self, note_id: str):
        self.data["notes"] = [n for n in self.data["notes"] if n["id"] != note_id]
        self._modified = True


# src/formats/liquote.py
class LiQuote(LitFormat):
    """Zitate aus einer Quelle (.liquote)"""
    
    EXTENSION = ".liquote"
    
    def _default_data(self) -> dict:
        return {
            "quotes": []
        }
    
    def add_quote(self, text: str, page: int, 
                  quote_type: str = "direct",
                  comment: str = "", 
                  tags: list = None) -> str:
        """
        Fügt Zitat hinzu.
        quote_type: "direct" (wörtlich) oder "indirect" (paraphrasiert)
        """
        quote_id = f"q{len(self.data['quotes']) + 1:03d}"
        
        quote = {
            "id": quote_id,
            "type": quote_type,
            "text": text,
            "page": page,
            "comment": comment,
            "tags": tags or [],
            "created_at": datetime.now().isoformat()
        }
        
        self.data["quotes"].append(quote)
        self._modified = True
        return quote_id
    
    def format_citation(self, quote_id: str, style: str = "apa") -> str:
        """Formatiert Zitat für Verwendung"""
        quote = self.get_quote(quote_id)
        if not quote:
            return ""
        
        # Placeholder - wird von Bibliography-Modul verwendet
        if quote["type"] == "direct":
            return f'"{quote["text"]}" (S. {quote["page"]})'
        else:
            return f'{quote["text"]} (vgl. S. {quote["page"]})'


# src/formats/litask.py
class LiTask(LitFormat):
    """Aufgaben zu einer Quelle oder Projekt (.litask)"""
    
    EXTENSION = ".litask"
    
    def _default_data(self) -> dict:
        return {
            "tasks": []
        }
    
    def add_task(self, title: str, 
                 description: str = "",
                 priority: str = "normal",  # low, normal, high
                 due_date: str = None) -> str:
        """Fügt Aufgabe hinzu"""
        task_id = f"t{len(self.data['tasks']) + 1:03d}"
        
        task = {
            "id": task_id,
            "title": title,
            "description": description,
            "priority": priority,
            "status": "open",  # open, in_progress, done
            "due_date": due_date,
            "created_at": datetime.now().isoformat(),
            "completed_at": None
        }
        
        self.data["tasks"].append(task)
        self._modified = True
        return task_id
    
    def complete_task(self, task_id: str):
        for task in self.data["tasks"]:
            if task["id"] == task_id:
                task["status"] = "done"
                task["completed_at"] = datetime.now().isoformat()
                self._modified = True
                return


# src/formats/lisum.py
class LiSum(LitFormat):
    """Zusammenfassungen einer Quelle (.lisum)"""
    
    EXTENSION = ".lisum"
    
    def _default_data(self) -> dict:
        return {
            "summaries": []
        }
    
    def add_summary(self, text: str,
                    scope: str = "full",  # full, chapter, section, page_range
                    scope_detail: str = "",
                    source: str = "manual") -> str:  # manual, ai_ollama, ai_claude
        """Fügt Zusammenfassung hinzu"""
        sum_id = f"s{len(self.data['summaries']) + 1:03d}"
        
        summary = {
            "id": sum_id,
            "text": text,
            "scope": scope,
            "scope_detail": scope_detail,
            "source": source,
            "model": None,  # Falls AI: Modellname
            "created_at": datetime.now().isoformat()
        }
        
        self.data["summaries"].append(summary)
        self._modified = True
        return sum_id
```

**Tasks:**
- [ ] LitFormat Basis-Klasse
- [ ] LiMeta implementieren
- [ ] LiNote implementieren
- [ ] LiQuote implementieren
- [ ] LiTask implementieren
- [ ] LiSum implementieren
- [ ] JSON Schema Validierung

**Deliverable:** Alle Dateiformate funktionieren

### Woche 2: Projekt- und Quellen-Management

#### Tag 1-2: Project Model & Manager
```python
# src/models/project.py
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional
import json

@dataclass
class LitProject:
    """Repräsentiert ein Literaturprojekt"""
    
    name: str
    path: Path
    description: str = ""
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    default_citation_style: str = "apa"
    
    def __post_init__(self):
        self.path = Path(self.path)
    
    @property
    def sources_dir(self) -> Path:
        return self.path / "Quellen"
    
    @property
    def config_file(self) -> Path:
        return self.path / "projekt_config.liproj"
    
    @property
    def project_tasks_file(self) -> Path:
        return self.path / "projekt_tasks.litask"
    
    @property
    def project_notes_file(self) -> Path:
        return self.path / "projekt_notes.linote"
    
    @property
    def bibliography_file(self) -> Path:
        return self.path / "projekt_biblio.bib"
    
    def create_structure(self):
        """Erstellt Projektordner-Struktur"""
        self.path.mkdir(parents=True, exist_ok=True)
        self.sources_dir.mkdir(exist_ok=True)
        
        # Config speichern
        config = {
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at,
            "default_citation_style": self.default_citation_style
        }
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
        
        # Leere Projekt-Dateien erstellen
        LiTask().save(self.project_tasks_file)
        LiNote().save(self.project_notes_file)
    
    @classmethod
    def load(cls, path: Path) -> 'LitProject':
        """Lädt Projekt aus Ordner"""
        config_file = path / "projekt_config.liproj"
        if not config_file.exists():
            raise ValueError(f"Kein gültiges Projekt: {path}")
        
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        return cls(
            name=config["name"],
            path=path,
            description=config.get("description", ""),
            created_at=config.get("created_at"),
            default_citation_style=config.get("default_citation_style", "apa")
        )
    
    def get_sources(self) -> List['LitSource']:
        """Gibt alle Quellen im Projekt zurück"""
        sources = []
        if self.sources_dir.exists():
            for source_dir in self.sources_dir.iterdir():
                if source_dir.is_dir():
                    try:
                        source = LitSource.load(source_dir)
                        sources.append(source)
                    except:
                        pass
        return sources


# src/models/source.py
@dataclass
class LitSource:
    """Repräsentiert eine einzelne Quelle (Ordner)"""
    
    path: Path
    folder_name: str = ""
    
    def __post_init__(self):
        self.path = Path(self.path)
        if not self.folder_name:
            self.folder_name = self.path.name
    
    @property
    def meta_file(self) -> Path:
        return self.path / "meta.limeta"
    
    @property
    def notes_file(self) -> Path:
        return self.path / "notes.linote"
    
    @property
    def quotes_file(self) -> Path:
        return self.path / "quotes.liquote"
    
    @property
    def tasks_file(self) -> Path:
        return self.path / "tasks.litask"
    
    @property
    def summaries_file(self) -> Path:
        return self.path / "summaries.lisum"
    
    @property
    def source_file(self) -> Optional[Path]:
        """Findet die Originaldatei (PDF, etc.)"""
        for ext in ['.pdf', '.epub', '.docx', '.html']:
            for f in self.path.glob(f"*{ext}"):
                if not f.name.startswith('_'):
                    return f
        return None
    
    def create_structure(self, source_file: Path = None):
        """Erstellt Quellen-Ordner mit Dateien"""
        self.path.mkdir(parents=True, exist_ok=True)
        
        # Standard-Dateien erstellen
        LiMeta().save(self.meta_file)
        LiNote().save(self.notes_file)
        LiQuote().save(self.quotes_file)
        LiTask().save(self.tasks_file)
        LiSum().save(self.summaries_file)
        
        # Quelldatei kopieren falls angegeben
        if source_file and source_file.exists():
            import shutil
            dest = self.path / f"source{source_file.suffix}"
            shutil.copy2(source_file, dest)
            
            # Metadaten aktualisieren
            meta = LiMeta()
            meta.load(self.meta_file)
            meta.data["source_file"] = dest.name
            meta.save()
    
    @classmethod
    def load(cls, path: Path) -> 'LitSource':
        """Lädt Quelle aus Ordner"""
        if not (path / "meta.limeta").exists():
            raise ValueError(f"Keine gültige Quelle: {path}")
        return cls(path=path)
    
    def get_metadata(self) -> LiMeta:
        meta = LiMeta()
        meta.load(self.meta_file)
        return meta
    
    def get_status(self) -> str:
        """Gibt Status der Bearbeitung zurück"""
        tasks = LiTask()
        tasks.load(self.tasks_file)
        
        open_tasks = sum(1 for t in tasks.data["tasks"] if t["status"] != "done")
        
        quotes = LiQuote()
        quotes.load(self.quotes_file)
        
        notes = LiNote()
        notes.load(self.notes_file)
        
        if open_tasks == 0 and len(quotes.data["quotes"]) > 0:
            return "done"  # ✅
        elif len(notes.data["notes"]) > 0 or len(quotes.data["quotes"]) > 0:
            return "in_progress"  # ⏳
        else:
            return "new"  # 📄
```

**Tasks:**
- [ ] LitProject Model
- [ ] LitSource Model
- [ ] ProjectManager Klasse
- [ ] Projekt erstellen/öffnen/löschen
- [ ] Quelle erstellen/importieren

**Deliverable:** Projekt- und Quellen-Verwaltung funktioniert

#### Tag 3-4: Source Manager
```python
# src/core/source_manager.py
class SourceManager:
    """Verwaltet Quellen innerhalb eines Projekts"""
    
    def __init__(self, project: LitProject):
        self.project = project
    
    def create_source(self, name: str, source_file: Path = None) -> LitSource:
        """Erstellt neue Quelle"""
        # Name normalisieren (z.B. "Smith2023_AI_Study")
        folder_name = self._normalize_name(name)
        source_path = self.project.sources_dir / folder_name
        
        if source_path.exists():
            raise ValueError(f"Quelle existiert bereits: {folder_name}")
        
        source = LitSource(path=source_path, folder_name=folder_name)
        source.create_structure(source_file)
        
        return source
    
    def import_pdf(self, pdf_path: Path, auto_extract: bool = True) -> LitSource:
        """Importiert PDF als neue Quelle"""
        # Ordnername aus Dateiname generieren
        name = pdf_path.stem
        source = self.create_source(name, pdf_path)
        
        if auto_extract:
            # Versuche Metadaten aus PDF zu extrahieren
            self._extract_pdf_metadata(source, pdf_path)
        
        return source
    
    def _extract_pdf_metadata(self, source: LitSource, pdf_path: Path):
        """Extrahiert Metadaten aus PDF"""
        import fitz
        
        doc = fitz.open(pdf_path)
        pdf_meta = doc.metadata
        
        meta = source.get_metadata()
        
        if pdf_meta.get("title"):
            meta.data["title"] = pdf_meta["title"]
        if pdf_meta.get("author"):
            meta.data["authors"] = [pdf_meta["author"]]
        
        meta.save()
    
    def delete_source(self, source: LitSource, backup: bool = True):
        """Löscht Quelle (mit optionalem Backup)"""
        if backup:
            import shutil
            backup_path = self.project.path / "_deleted" / source.folder_name
            backup_path.parent.mkdir(exist_ok=True)
            shutil.move(source.path, backup_path)
        else:
            import shutil
            shutil.rmtree(source.path)
    
    def search_sources(self, query: str) -> List[LitSource]:
        """Durchsucht Quellen nach Begriff"""
        results = []
        query_lower = query.lower()
        
        for source in self.project.get_sources():
            meta = source.get_metadata()
            
            # Suche in Titel, Autoren, Tags
            if (query_lower in meta.data.get("title", "").lower() or
                any(query_lower in a.lower() for a in meta.data.get("authors", [])) or
                any(query_lower in t.lower() for t in meta.data.get("tags", []))):
                results.append(source)
        
        return results
```

**Tasks:**
- [ ] SourceManager Klasse
- [ ] PDF-Import mit Metadaten-Extraktion
- [ ] Quelle umbenennen
- [ ] Quelle verschieben
- [ ] Suche in Quellen

**Deliverable:** Quellen-Management vollständig

#### Tag 5: ProFiler Bridge
```python
# src/core/profiler_bridge.py
class ProfilerBridge:
    """Integration mit ProFiler für Index-Funktionen"""
    
    def __init__(self, project: LitProject):
        self.project = project
        self.db_path = project.path / ".litindex" / "index.db"
        self.db_path.parent.mkdir(exist_ok=True)
        self.conn = sqlite3.connect(str(self.db_path))
        self._create_tables()
    
    def _create_tables(self):
        self.conn.executescript('''
            CREATE TABLE IF NOT EXISTS source_index (
                id INTEGER PRIMARY KEY,
                source_path TEXT UNIQUE,
                title TEXT,
                authors TEXT,
                year INTEGER,
                content_text TEXT,
                indexed_at TEXT
            );
            
            CREATE VIRTUAL TABLE IF NOT EXISTS source_fts USING fts5(
                title, authors, content_text
            );
        ''')
    
    def index_source(self, source: LitSource):
        """Indiziert eine Quelle für Volltextsuche"""
        meta = source.get_metadata()
        
        # PDF-Text extrahieren
        content = ""
        if source.source_file and source.source_file.suffix == '.pdf':
            content = self._extract_pdf_text(source.source_file)
        
        self.conn.execute('''
            INSERT OR REPLACE INTO source_index 
            (source_path, title, authors, year, content_text, indexed_at)
            VALUES (?, ?, ?, ?, ?, datetime('now'))
        ''', (
            str(source.path),
            meta.data.get("title", ""),
            ", ".join(meta.data.get("authors", [])),
            meta.data.get("year"),
            content
        ))
        
        self.conn.commit()
    
    def search(self, query: str) -> List[dict]:
        """Volltextsuche in allen Quellen"""
        cursor = self.conn.execute('''
            SELECT source_path, title, authors, snippet(source_fts, 2, '<b>', '</b>', '...', 32)
            FROM source_fts
            WHERE source_fts MATCH ?
            ORDER BY rank
        ''', (query,))
        
        return [
            {'path': row[0], 'title': row[1], 'authors': row[2], 'snippet': row[3]}
            for row in cursor
        ]
```

**Tasks:**
- [ ] ProfilerBridge Klasse
- [ ] Quellen-Indizierung
- [ ] Volltextsuche
- [ ] PDF-Text-Extraktion

**Deliverable:** Index-Funktionen verfügbar

### Woche 3-4: GUI Grundgerüst

#### Tag 1-3: Hauptfenster mit 3-Panel Layout
```python
# src/gui/main_window.py
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LitZentrum")
        self.setMinimumSize(1400, 900)
        
        self.current_project: Optional[LitProject] = None
        self.current_source: Optional[LitSource] = None
        
        self._setup_ui()
        self._setup_menu()
        self._setup_toolbar()
        self._connect_signals()
        self._restore_state()
    
    def _setup_ui(self):
        # Haupt-Splitter
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Links: Projektbaum
        self.project_tree = ProjectTreePanel()
        main_splitter.addWidget(self.project_tree)
        
        # Mitte: Quellen-Liste
        self.source_list = SourceListPanel()
        main_splitter.addWidget(self.source_list)
        
        # Rechts: Detail-Panel
        self.detail_panel = DetailPanel()
        main_splitter.addWidget(self.detail_panel)
        
        main_splitter.setSizes([250, 400, 550])
        self.setCentralWidget(main_splitter)
    
    def _setup_menu(self):
        menubar = self.menuBar()
        
        # Datei-Menü
        file_menu = menubar.addMenu("&Datei")
        file_menu.addAction("Neues Projekt...", self._new_project, "Ctrl+N")
        file_menu.addAction("Projekt öffnen...", self._open_project, "Ctrl+O")
        file_menu.addAction("Projekt schließen", self._close_project)
        file_menu.addSeparator()
        file_menu.addAction("Quelle hinzufügen...", self._add_source, "Ctrl+Shift+N")
        file_menu.addAction("PDF importieren...", self._import_pdf)
        file_menu.addSeparator()
        file_menu.addAction("Beenden", self.close, "Ctrl+Q")
        
        # Bearbeiten-Menü
        edit_menu = menubar.addMenu("&Bearbeiten")
        edit_menu.addAction("Metadaten bearbeiten...", self._edit_metadata, "Ctrl+M")
        edit_menu.addAction("Notiz hinzufügen...", self._add_note, "Ctrl+Shift+N")
        edit_menu.addAction("Zitat hinzufügen...", self._add_quote, "Ctrl+Shift+Q")
        
        # Ansicht-Menü
        view_menu = menubar.addMenu("&Ansicht")
        view_menu.addAction("PDF-Werkstatt", self._show_pdf_workshop)
        view_menu.addAction("Volltext-Suche...", self._show_search, "Ctrl+F")
        
        # Export-Menü
        export_menu = menubar.addMenu("&Export")
        export_menu.addAction("Bibliografie erstellen...", self._export_bibliography)
        export_menu.addAction("Nach Word exportieren...", self._export_word)
        
        # KI-Menü (Phase 2)
        ai_menu = menubar.addMenu("&KI")
        ai_menu.addAction("Zusammenfassung erstellen...", self._ai_summarize)
        ai_menu.addAction("Metadaten nachschlagen...", self._ai_lookup)
        ai_menu.addAction("KI-Warteschlange...", self._show_ai_queue)
```

**Tasks:**
- [ ] MainWindow mit Splitter-Layout
- [ ] Menüleiste komplett
- [ ] Toolbar (Neu, Öffnen, Suche, Export)
- [ ] StatusBar

**Deliverable:** Hauptfenster-Grundgerüst

#### Tag 4-5: Projekt-Baum Panel
```python
# src/gui/panels/project_tree.py
class ProjectTreePanel(QWidget):
    project_selected = pyqtSignal(object)  # LitProject
    folder_selected = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Header
        header = QHBoxLayout()
        header.addWidget(QLabel("📚 Projekte"))
        self.refresh_btn = QPushButton("🔄")
        self.refresh_btn.setFixedSize(24, 24)
        header.addStretch()
        header.addWidget(self.refresh_btn)
        layout.addLayout(header)
        
        # Tree Widget
        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.itemClicked.connect(self._on_item_clicked)
        layout.addWidget(self.tree)
        
        # Buttons
        btn_layout = QHBoxLayout()
        self.new_btn = QPushButton("+ Projekt")
        self.open_btn = QPushButton("📂 Öffnen")
        btn_layout.addWidget(self.new_btn)
        btn_layout.addWidget(self.open_btn)
        layout.addLayout(btn_layout)
        
        self.projects: List[LitProject] = []
        self._load_recent_projects()
    
    def add_project(self, project: LitProject):
        """Fügt Projekt zum Baum hinzu"""
        item = QTreeWidgetItem([f"📚 {project.name}"])
        item.setData(0, Qt.ItemDataRole.UserRole, project)
        
        # Unterordner
        sources_item = QTreeWidgetItem(["📁 Quellen"])
        sources_item.setData(0, Qt.ItemDataRole.UserRole, "sources")
        item.addChild(sources_item)
        
        # Quellen als Kinder
        for source in project.get_sources():
            meta = source.get_metadata()
            status = source.get_status()
            status_icon = {"done": "✅", "in_progress": "⏳", "new": "📄"}.get(status, "📄")
            
            source_item = QTreeWidgetItem([f"{status_icon} {meta.title or source.folder_name}"])
            source_item.setData(0, Qt.ItemDataRole.UserRole, source)
            sources_item.addChild(source_item)
        
        self.tree.addTopLevelItem(item)
        item.setExpanded(True)
        sources_item.setExpanded(True)
```

**Tasks:**
- [ ] ProjectTreePanel Widget
- [ ] Projekte anzeigen
- [ ] Quellen als Kinder
- [ ] Status-Icons (✅ ⏳ 📄)
- [ ] Drag & Drop (optional)

**Deliverable:** Projektbaum funktioniert

#### Weitere Tage (Woche 4): Source List & Detail Panel

```python
# src/gui/panels/source_list.py
class SourceListPanel(QWidget):
    source_selected = pyqtSignal(object)  # LitSource
    
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        
        # Filter & Suche
        filter_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Quellen filtern...")
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["Alle", "Unbearbeitet", "In Bearbeitung", "Fertig"])
        filter_layout.addWidget(self.search_input)
        filter_layout.addWidget(self.filter_combo)
        layout.addLayout(filter_layout)
        
        # Tabelle
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Status", "Titel", "Autoren", "Jahr"])
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.itemSelectionChanged.connect(self._on_selection_changed)
        layout.addWidget(self.table)


# src/gui/panels/detail_panel.py
class DetailPanel(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        
        # Header mit Titel
        self.title_label = QLabel("Keine Quelle ausgewählt")
        self.title_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(self.title_label)
        
        # Metadaten-Übersicht
        self.meta_group = QGroupBox("Metadaten")
        meta_layout = QFormLayout()
        self.author_label = QLabel()
        self.year_label = QLabel()
        self.doi_label = QLabel()
        self.tags_label = QLabel()
        meta_layout.addRow("Autoren:", self.author_label)
        meta_layout.addRow("Jahr:", self.year_label)
        meta_layout.addRow("DOI:", self.doi_label)
        meta_layout.addRow("Tags:", self.tags_label)
        self.meta_group.setLayout(meta_layout)
        layout.addWidget(self.meta_group)
        
        # Tabs: Notizen | Zitate | Aufgaben | Zusammenfassungen
        self.tabs = QTabWidget()
        
        self.notes_tab = NotesTab()
        self.quotes_tab = QuotesTab()
        self.tasks_tab = TasksTab()
        self.summaries_tab = SummariesTab()
        
        self.tabs.addTab(self.notes_tab, "📝 Notizen")
        self.tabs.addTab(self.quotes_tab, "💬 Zitate")
        self.tabs.addTab(self.tasks_tab, "☑️ Aufgaben")
        self.tabs.addTab(self.summaries_tab, "📋 Zusammenfassungen")
        
        layout.addWidget(self.tabs)
        
        # PDF-Button
        self.open_pdf_btn = QPushButton("📄 PDF öffnen")
        layout.addWidget(self.open_pdf_btn)
```

**Tasks:**
- [ ] SourceListPanel mit Tabelle
- [ ] Filter und Suche
- [ ] Sortierung
- [ ] DetailPanel mit Tabs
- [ ] NotesTab, QuotesTab, TasksTab, SummariesTab

**Deliverable:** GUI-Grundgerüst komplett

---

## 📅 PHASE 2: PDF-Werkstatt (Wochen 5-8)

### Woche 5-6: PDF-Viewer & Markierungen

#### Tasks:
- [ ] PDF-Viewer mit PyMuPDF
- [ ] Text-Markierung
- [ ] "Als Zitat übernehmen" Funktion
- [ ] Markierungen speichern
- [ ] Annotationen anzeigen

### Woche 7-8: PDF-Tools Integration

#### Tasks:
- [ ] PDFSchwärzer Pro Integration
- [ ] pdfmarker2000 Integration
- [ ] Auszüge erstellen
- [ ] OCR-Integration (optional)

---

## 📅 PHASE 3: Bibliografie (Wochen 9-10)

### Woche 9: BibTeX Generator

```python
# src/modules/bibliography/bibtex.py
class BibTeXGenerator:
    """Generiert BibTeX aus Projekt-Quellen"""
    
    def generate(self, project: LitProject, 
                 sources: List[LitSource] = None) -> str:
        """Generiert BibTeX für alle oder ausgewählte Quellen"""
        if sources is None:
            sources = project.get_sources()
        
        entries = []
        for source in sources:
            meta = source.get_metadata()
            entry = meta.to_bibtex()
            entries.append(entry)
        
        return "\n\n".join(entries)
    
    def export(self, project: LitProject, output_path: Path = None):
        """Exportiert BibTeX in Datei"""
        if output_path is None:
            output_path = project.bibliography_file
        
        content = self.generate(project)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
```

**Tasks:**
- [ ] BibTeX Generator
- [ ] Export-Dialog
- [ ] Quellen-Auswahl für Export

### Woche 10: Zitationsstile

```python
# src/modules/bibliography/styles.py
class CitationStyleFormatter:
    """Formatiert Zitate nach verschiedenen Stilen"""
    
    STYLES = {
        'apa': APAFormatter,
        'mla': MLAFormatter,
        'chicago': ChicagoFormatter,
        'din': DINFormatter,
        'harvard': HarvardFormatter,
    }
    
    def format(self, meta: LiMeta, style: str = 'apa') -> str:
        formatter = self.STYLES.get(style, APAFormatter)()
        return formatter.format(meta)
    
    def format_inline(self, meta: LiMeta, page: int, style: str = 'apa') -> str:
        """Formatiert Inline-Zitat (z.B. "(Smith, 2023, S. 42)")"""
        formatter = self.STYLES.get(style, APAFormatter)()
        return formatter.format_inline(meta, page)


class APAFormatter:
    def format(self, meta: LiMeta) -> str:
        authors = self._format_authors(meta.authors)
        year = f"({meta.data.get('year', 'o.J.')})"
        title = f"*{meta.title}*" if meta.title else ""
        
        return f"{authors} {year}. {title}."
    
    def format_inline(self, meta: LiMeta, page: int) -> str:
        author = meta.authors[0].split(',')[0] if meta.authors else "Unbekannt"
        year = meta.data.get('year', 'o.J.')
        return f"({author}, {year}, S. {page})"
```

**Tasks:**
- [ ] APA Formatter
- [ ] MLA Formatter
- [ ] DIN Formatter
- [ ] Stil-Auswahl Dialog
- [ ] Word-Export mit Formatierung

---

## 📅 PHASE 4: KI-Integration (Wochen 11-13) - Optional

### Woche 11-12: Ollama Queue

```python
# src/modules/ai/ollama_queue.py
class OllamaQueue(QObject):
    """Warteschlange für lokale KI-Verarbeitung"""
    
    job_started = pyqtSignal(str)
    job_progress = pyqtSignal(str, int)
    job_completed = pyqtSignal(str, str)  # job_id, result
    job_failed = pyqtSignal(str, str)     # job_id, error
    
    def __init__(self):
        super().__init__()
        self.queue = []
        self.current_job = None
        self.thread = None
        
        self.base_url = "http://localhost:11434"
        self.default_model = "mistral:latest"
    
    def add_job(self, job_type: str, source: LitSource, 
                params: dict = None) -> str:
        """Fügt Job zur Queue hinzu"""
        job_id = f"job_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{len(self.queue)}"
        
        job = {
            "id": job_id,
            "type": job_type,  # summarize, extract_quotes, metadata_lookup
            "source": source,
            "params": params or {},
            "status": "pending",
            "created_at": datetime.now().isoformat()
        }
        
        self.queue.append(job)
        self._process_next()
        
        return job_id
    
    def _process_next(self):
        if self.current_job or not self.queue:
            return
        
        self.current_job = self.queue.pop(0)
        self.job_started.emit(self.current_job["id"])
        
        # In Thread ausführen
        self.thread = QThread()
        self.worker = OllamaWorker(self.current_job, self.base_url, self.default_model)
        self.worker.moveToThread(self.thread)
        
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self._on_job_finished)
        self.worker.error.connect(self._on_job_error)
        
        self.thread.start()


# src/modules/ai/summarizer.py
class Summarizer:
    """Erstellt Zusammenfassungen mit Ollama"""
    
    PROMPT_TEMPLATE = """Erstelle eine strukturierte Zusammenfassung des folgenden akademischen Textes.
    
Gliedere die Zusammenfassung in:
1. Hauptthese/Kernaussage
2. Methodik (falls relevant)
3. Wichtigste Ergebnisse/Argumente
4. Schlussfolgerungen

Text:
{text}

Zusammenfassung:"""
    
    def summarize(self, text: str, model: str = "mistral:latest") -> str:
        prompt = self.PROMPT_TEMPLATE.format(text=text[:10000])  # Max 10k Zeichen
        
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            }
        )
        
        return response.json()["response"]
```

**Tasks:**
- [ ] OllamaQueue Klasse
- [ ] Job-Verwaltung
- [ ] Summarizer
- [ ] Metadata-Lookup (ISBN/DOI)
- [ ] Queue-Dialog

### Woche 13: KI-UI Integration

**Tasks:**
- [ ] "Zusammenfassen" Button
- [ ] KI-Status-Anzeige
- [ ] Ergebnisse in .lisum speichern
- [ ] Model-Auswahl

---

## 📅 PHASE 5: Polish & Release (Wochen 14-16)

### Tasks:
- [ ] ProSync Integration für Backups
- [ ] Themes (Light/Dark)
- [ ] Settings Dialog
- [ ] Keyboard Shortcuts
- [ ] Performance-Optimierung
- [ ] Testing
- [ ] Documentation
- [ ] Release Build

---

## 📋 Meilensteine

| Woche | Meilenstein | Deliverable |
|-------|-------------|-------------|
| 1 | Dateiformate | Alle .li* Formate funktionieren |
| 2 | Projekt-Management | Projekte & Quellen verwalten |
| 3-4 | GUI Grundgerüst | 3-Panel Interface |
| 5-6 | PDF-Viewer | Markierungen → Zitate |
| 7-8 | PDF-Tools | Schwärzen, Auszüge |
| 9-10 | Bibliografie | BibTeX + Zitationsstile |
| 11-13 | KI (Optional) | Ollama-Integration |
| 14-16 | MVP Release | Version 1.0 |

---

## ⚠️ Risiken & Mitigationen

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|--------|------------|
| PDF-Extraktion komplex | Hoch | Mittel | PyMuPDF als robuste Basis |
| Ollama nicht installiert | Mittel | Niedrig | Feature optional, klare Anleitung |
| Große Bibliotheken | Mittel | Mittel | Lazy Loading, Pagination |
| Dateiformat-Änderungen | Niedrig | Hoch | Schema-Versionierung von Anfang an |

---

## 🔧 Technische Abhängigkeiten

```
requirements.txt:
PyQt6>=6.4.0
PyMuPDF>=1.21.0
bibtexparser>=1.4.0
python-docx>=0.8.11
requests>=2.28.0
jsonschema>=4.17.0
```

---

*Detaillierter Umsetzungsplan erstellt: 03.01.2026*


---

## ✅ IMPLEMENTIERUNGSFORTSCHRITT (Stand: 03.01.2026)

### Abgeschlossene Module

#### Phase 1: Dateiformate & Kern-Architektur ✅ KOMPLETT
- [x] JSON-Schemas für alle 6 Formate (.limeta, .linote, .liquote, .litask, .lisum, .liproj)
- [x] Python Format-Klassen mit Validierung
- [x] ProjectManager für Projektverwaltung
- [x] SourceManager für Quellenverwaltung
- [x] EventBus für Modul-Kommunikation
- [x] SettingsManager für Einstellungen

#### Phase 2: GUI Grundgerüst ✅ KOMPLETT
- [x] MainWindow mit 3-Panel-Layout
- [x] ProjectTreePanel (Projektbaum)
- [x] SourceListPanel (Quellenliste mit Filter)
- [x] DetailPanel (Metadaten + Tabs)
- [x] Alle Tabs: Notes, Quotes, Tasks, Summaries, PDF
- [x] Dialoge: NewProject, Source, Settings

#### Phase 3: PDF-Integration ✅ KOMPLETT
- [x] PDFViewer Widget mit Zoom, Navigation
- [x] PDFExtractor für Textextraktion
- [x] PDFTab mit Suche und Schnellaktionen
- [x] Integration in DetailPanel

#### Phase 4: Bibliografie ✅ KOMPLETT
- [x] BibTeXGenerator und BibTeXParser
- [x] 5 Zitationsstile (APA, MLA, Chicago, DIN, Harvard)
- [x] CitationStyleManager

#### Phase 5: KI-Integration ✅ GRUNDSTRUKTUR
- [x] OllamaQueue mit Job-Verwaltung
- [x] Summarizer-Prompts
- [x] Basis-UI-Integration

#### Phase 6: Sync & Backup ✅ KOMPLETT
- [x] GitSync für Versionierung
- [x] BackupManager für lokale Backups

### Dateistatistik

| Kategorie | Dateien | ~Zeilen |
|-----------|---------|---------|
| Core | 5 | ~700 |
| Formats | 8 | ~750 |
| GUI Panels | 4 | ~750 |
| GUI Tabs | 6 | ~1200 |
| GUI Dialogs | 4 | ~650 |
| GUI Widgets | 2 | ~300 |
| Modules | 6 | ~900 |
| Tests | 1 | ~200 |
| Config/Setup | 4 | ~250 |
| **GESAMT** | **~50** | **~5700** |

### Projektstruktur

```
LitZentrum/
├── src/
│   ├── main.py                     # Einstiegspunkt
│   ├── core/                       # Kernlogik (5 Dateien)
│   ├── formats/                    # Datei-Formate (8 Dateien)
│   ├── gui/                        # Benutzeroberfläche
│   │   ├── main_window.py
│   │   ├── panels/                 # 3 Panels + __init__
│   │   ├── tabs/                   # 5 Tabs + __init__
│   │   ├── dialogs/                # 3 Dialoge + __init__
│   │   └── widgets/                # PDFViewer + __init__
│   ├── models/                     # Datenmodelle
│   └── modules/                    # Erweiterungen
│       ├── bibliography/           # BibTeX + Stile
│       ├── pdf_workshop/           # PDF-Extraktion
│       ├── ai/                     # Ollama-Queue
│       └── sync/                   # Git + Backup
├── schemas/                        # 6 JSON-Schemas
├── tests/                          # Unit-Tests
├── resources/icons/                # Icons (leer)
├── requirements.txt
├── setup.py
├── start.bat
└── README.md
```

### Nächste Schritte

1. **Icons erstellen** - App-Icon und Toolbar-Icons
2. **Integration testen** - Anwendung starten und debuggen
3. **Word-Export** - python-docx Integration für Literaturverzeichnisse
4. **Dark Theme** - Alternatives Farbschema
5. **Keyboard Shortcuts** - Produktivitäts-Features

---

*Implementierung gestartet: 03.01.2026*
*Letztes Update: 03.01.2026*
