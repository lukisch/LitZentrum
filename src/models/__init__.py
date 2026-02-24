"""
LitZentrum - Models
Datenmodelle für die Anwendung
"""
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from pathlib import Path
from datetime import datetime


@dataclass
class SearchResult:
    """Suchergebnis"""
    source_path: Path
    title: str
    authors: List[str]
    year: Optional[int]
    match_type: str  # title, author, tag, content
    match_text: str
    relevance: float = 1.0


@dataclass
class ExportOptions:
    """Export-Optionen"""
    format: str  # bibtex, word, markdown
    citation_style: str = "apa"
    include_abstracts: bool = False
    include_notes: bool = False
    include_quotes: bool = False
    output_path: Optional[Path] = None


@dataclass
class ImportResult:
    """Import-Ergebnis"""
    success: bool
    imported_count: int = 0
    failed_count: int = 0
    errors: List[str] = field(default_factory=list)
    imported_sources: List[Path] = field(default_factory=list)


@dataclass
class PDFSelection:
    """PDF-Textauswahl"""
    text: str
    page: int
    rect: tuple  # x0, y0, x1, y1
    
    def to_quote_data(self) -> Dict[str, Any]:
        """Konvertiert zu Zitat-Daten"""
        return {
            "text": self.text,
            "page": self.page,
        }


@dataclass  
class Statistics:
    """Projekt-Statistiken"""
    total_sources: int = 0
    sources_with_pdf: int = 0
    total_notes: int = 0
    total_quotes: int = 0
    total_tasks: int = 0
    open_tasks: int = 0
    overdue_tasks: int = 0
    total_summaries: int = 0
    
    def to_dict(self) -> Dict[str, int]:
        return {
            "Quellen": self.total_sources,
            "Mit PDF": self.sources_with_pdf,
            "Notizen": self.total_notes,
            "Zitate": self.total_quotes,
            "Aufgaben": self.total_tasks,
            "Offen": self.open_tasks,
            "Überfällig": self.overdue_tasks,
            "Zusammenfassungen": self.total_summaries,
        }


__all__ = [
    "SearchResult",
    "ExportOptions",
    "ImportResult",
    "PDFSelection",
    "Statistics",
]
