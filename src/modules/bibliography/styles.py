"""
LitZentrum - Zitationsstile
Formatiert Zitate nach verschiedenen Stilen (APA, MLA, Chicago, DIN, Harvard)
"""
from abc import ABC, abstractmethod
from typing import Optional

from formats import LiMeta


class CitationFormatter(ABC):
    """Abstrakte Basisklasse für Zitationsformatierer"""
    
    @abstractmethod
    def format_reference(self, meta: LiMeta) -> str:
        """Formatiert Literaturverzeichnis-Eintrag"""
        pass
    
    @abstractmethod
    def format_inline(self, meta: LiMeta, page: Optional[int] = None) -> str:
        """Formatiert Inline-Zitat"""
        pass
    
    def _format_authors(self, authors: list, max_authors: int = 3) -> str:
        """Formatiert Autorenliste"""
        if not authors:
            return "Unbekannt"
        
        if len(authors) <= max_authors:
            if len(authors) == 1:
                return authors[0]
            else:
                return ", ".join(authors[:-1]) + " & " + authors[-1]
        else:
            return authors[0] + " et al."


class APAFormatter(CitationFormatter):
    """APA 7th Edition Style"""
    
    def format_reference(self, meta: LiMeta) -> str:
        parts = []
        
        # Autoren
        authors = self._format_authors(meta.authors)
        parts.append(authors)
        
        # Jahr
        year = f"({meta.year})" if meta.year else "(o.J.)"
        parts.append(year + ".")
        
        # Titel
        if meta.title:
            title = meta.title
            if meta.source_type == "article":
                parts.append(f"{title}.")
            else:
                parts.append(f"*{title}*.")
        
        # Journal (für Artikel)
        if meta.journal:
            journal_part = f"*{meta.journal}*"
            if meta.volume:
                journal_part += f", *{meta.volume}*"
            if meta.issue:
                journal_part += f"({meta.issue})"
            if meta.pages:
                journal_part += f", {meta.pages}"
            parts.append(journal_part + ".")
        
        # Verlag (für Bücher)
        elif meta.publisher:
            parts.append(f"{meta.publisher}.")
        
        # DOI
        if meta.doi:
            parts.append(f"https://doi.org/{meta.doi}")
        
        return " ".join(parts)
    
    def format_inline(self, meta: LiMeta, page: Optional[int] = None) -> str:
        author = meta.first_author
        year = meta.year or "o.J."
        
        if page:
            return f"({author}, {year}, S. {page})"
        return f"({author}, {year})"


class MLAFormatter(CitationFormatter):
    """MLA 9th Edition Style"""
    
    def format_reference(self, meta: LiMeta) -> str:
        parts = []
        
        # Autoren (Nachname, Vorname)
        if meta.authors:
            parts.append(meta.authors[0] + ".")
        
        # Titel
        if meta.title:
            if meta.source_type == "article":
                parts.append(f'"{meta.title}."')
            else:
                parts.append(f"*{meta.title}*.")
        
        # Container (Journal)
        if meta.journal:
            container = f"*{meta.journal}*"
            if meta.volume:
                container += f", vol. {meta.volume}"
            if meta.issue:
                container += f", no. {meta.issue}"
            if meta.year:
                container += f", {meta.year}"
            if meta.pages:
                container += f", pp. {meta.pages}"
            parts.append(container + ".")
        
        # Verlag
        elif meta.publisher:
            parts.append(f"{meta.publisher}, {meta.year or 'n.d.'}.")
        
        return " ".join(parts)
    
    def format_inline(self, meta: LiMeta, page: Optional[int] = None) -> str:
        author = meta.first_author
        if page:
            return f"({author} {page})"
        return f"({author})"


class ChicagoFormatter(CitationFormatter):
    """Chicago Manual of Style (Notes-Bibliography)"""
    
    def format_reference(self, meta: LiMeta) -> str:
        parts = []
        
        # Autoren
        authors = self._format_authors(meta.authors)
        parts.append(authors + ".")
        
        # Titel
        if meta.title:
            if meta.source_type == "article":
                parts.append(f'"{meta.title}."')
            else:
                parts.append(f"*{meta.title}*.")
        
        # Journal
        if meta.journal:
            journal_part = f"*{meta.journal}*"
            if meta.volume:
                journal_part += f" {meta.volume}"
            if meta.issue:
                journal_part += f", no. {meta.issue}"
            if meta.year:
                journal_part += f" ({meta.year})"
            if meta.pages:
                journal_part += f": {meta.pages}"
            parts.append(journal_part + ".")
        
        # Verlag
        elif meta.publisher:
            location = ""  # Chicago braucht eigentlich Ort
            parts.append(f"{location}{meta.publisher}, {meta.year or 'n.d.'}.")
        
        return " ".join(parts)
    
    def format_inline(self, meta: LiMeta, page: Optional[int] = None) -> str:
        author = meta.first_author
        year = meta.year or "n.d."
        if page:
            return f"({author} {year}, {page})"
        return f"({author} {year})"


class DINFormatter(CitationFormatter):
    """DIN 1505-2 Style (German Standard)"""
    
    def format_reference(self, meta: LiMeta) -> str:
        parts = []
        
        # Autoren
        if meta.authors:
            authors = "; ".join(meta.authors)
            parts.append(authors + ":")
        
        # Titel
        if meta.title:
            parts.append(meta.title + ".")
        
        # Bei Artikeln
        if meta.journal:
            parts.append(f"In: {meta.journal}")
            if meta.volume:
                parts.append(f"Bd. {meta.volume}")
            if meta.year:
                parts.append(f"({meta.year})")
            if meta.pages:
                parts.append(f"S. {meta.pages}")
        
        # Bei Büchern
        elif meta.publisher:
            if meta.publisher:
                parts.append(meta.publisher)
            if meta.year:
                parts.append(str(meta.year))
        
        # ISBN
        if meta.isbn:
            parts.append(f"– ISBN {meta.isbn}")
        
        return " ".join(parts)
    
    def format_inline(self, meta: LiMeta, page: Optional[int] = None) -> str:
        author = meta.first_author
        year = meta.year or "o.J."
        if page:
            return f"[{author} {year}, S. {page}]"
        return f"[{author} {year}]"


class HarvardFormatter(CitationFormatter):
    """Harvard Style"""
    
    def format_reference(self, meta: LiMeta) -> str:
        parts = []
        
        # Autoren
        authors = self._format_authors(meta.authors)
        parts.append(authors)
        
        # Jahr
        year = f"({meta.year})" if meta.year else "(n.d.)"
        parts.append(year)
        
        # Titel
        if meta.title:
            if meta.source_type == "article":
                parts.append(f"'{meta.title}',")
            else:
                parts.append(f"*{meta.title}*,")
        
        # Journal
        if meta.journal:
            journal_part = f"*{meta.journal}*"
            if meta.volume:
                journal_part += f", {meta.volume}"
            if meta.issue:
                journal_part += f"({meta.issue})"
            if meta.pages:
                journal_part += f", pp. {meta.pages}"
            parts.append(journal_part + ".")
        
        # Verlag
        elif meta.publisher:
            parts.append(f"{meta.publisher}.")
        
        return " ".join(parts)
    
    def format_inline(self, meta: LiMeta, page: Optional[int] = None) -> str:
        author = meta.first_author
        year = meta.year or "n.d."
        if page:
            return f"({author}, {year}, p. {page})"
        return f"({author}, {year})"


class CitationStyleManager:
    """Verwaltet Zitationsstile"""
    
    STYLES = {
        "apa": APAFormatter,
        "mla": MLAFormatter,
        "chicago": ChicagoFormatter,
        "din": DINFormatter,
        "harvard": HarvardFormatter,
    }
    
    STYLE_NAMES = {
        "apa": "APA (7th Edition)",
        "mla": "MLA (9th Edition)",
        "chicago": "Chicago",
        "din": "DIN 1505-2",
        "harvard": "Harvard",
    }
    
    def __init__(self, default_style: str = "apa"):
        self.default_style = default_style
    
    def get_formatter(self, style: str = None) -> CitationFormatter:
        """Gibt Formatierer für Stil zurück"""
        style = style or self.default_style
        formatter_class = self.STYLES.get(style, APAFormatter)
        return formatter_class()
    
    def format_reference(self, meta: LiMeta, style: str = None) -> str:
        """Formatiert Literaturverzeichnis-Eintrag"""
        return self.get_formatter(style).format_reference(meta)
    
    def format_inline(self, meta: LiMeta, page: int = None, style: str = None) -> str:
        """Formatiert Inline-Zitat"""
        return self.get_formatter(style).format_inline(meta, page)
    
    @classmethod
    def available_styles(cls) -> list:
        """Gibt verfügbare Stile zurück"""
        return list(cls.STYLES.keys())
