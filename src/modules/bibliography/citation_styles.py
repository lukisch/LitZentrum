"""
LitZentrum - Zitationsstile
APA, MLA, Chicago, DIN, Harvard
"""
from abc import ABC, abstractmethod
from typing import Optional

from formats import LiMeta


class CitationFormatter(ABC):
    """Abstrakte Basisklasse für Zitationsformatierung"""
    
    @abstractmethod
    def format_full(self, meta: LiMeta) -> str:
        """Formatiert vollständige Literaturangabe"""
        pass
    
    @abstractmethod
    def format_inline(self, meta: LiMeta, page: Optional[int] = None) -> str:
        """Formatiert Inline-Zitat"""
        pass
    
    def _format_authors_list(self, authors: list, max_authors: int = 3) -> str:
        """Formatiert Autorenliste"""
        if not authors:
            return "Unbekannt"
        
        if len(authors) == 1:
            return authors[0]
        elif len(authors) <= max_authors:
            return ", ".join(authors[:-1]) + " & " + authors[-1]
        else:
            return authors[0] + " et al."


class APAFormatter(CitationFormatter):
    """APA Style (7th Edition)"""
    
    def format_full(self, meta: LiMeta) -> str:
        """APA Vollzitat"""
        parts = []
        
        # Autoren
        if meta.authors:
            authors = self._format_apa_authors(meta.authors)
            parts.append(authors)
        
        # Jahr
        year = f"({meta.year})" if meta.year else "(o.J.)"
        parts.append(year)
        
        # Titel
        if meta.title:
            title = meta.title
            if meta.source_type in ("article",):
                parts.append(f"{title}.")
            else:
                parts.append(f"*{title}*.")
        
        # Journal
        if meta.journal:
            journal_part = f"*{meta.journal}*"
            if meta.volume:
                journal_part += f", *{meta.volume}*"
            if meta.issue:
                journal_part += f"({meta.issue})"
            if meta.pages:
                journal_part += f", {meta.pages}"
            parts.append(journal_part + ".")
        
        # Publisher
        if meta.publisher and meta.source_type in ("book", "chapter"):
            parts.append(f"{meta.publisher}.")
        
        # DOI
        if meta.doi:
            parts.append(f"https://doi.org/{meta.doi}")
        
        return " ".join(parts)
    
    def format_inline(self, meta: LiMeta, page: Optional[int] = None) -> str:
        """APA Inline-Zitat: (Author, Jahr, S. X)"""
        author = meta.first_author
        year = meta.year or "o.J."
        
        if page:
            return f"({author}, {year}, S. {page})"
        return f"({author}, {year})"
    
    def _format_apa_authors(self, authors: list) -> str:
        """Formatiert Autoren nach APA"""
        if not authors:
            return ""
        
        if len(authors) == 1:
            return authors[0] + "."
        elif len(authors) == 2:
            return f"{authors[0]} & {authors[1]}."
        elif len(authors) <= 20:
            return ", ".join(authors[:-1]) + ", & " + authors[-1] + "."
        else:
            return ", ".join(authors[:19]) + ", ... " + authors[-1] + "."


class MLAFormatter(CitationFormatter):
    """MLA Style (9th Edition)"""
    
    def format_full(self, meta: LiMeta) -> str:
        """MLA Vollzitat"""
        parts = []
        
        # Autoren
        if meta.authors:
            if len(meta.authors) == 1:
                parts.append(meta.authors[0] + ".")
            elif len(meta.authors) == 2:
                parts.append(f"{meta.authors[0]}, and {meta.authors[1]}.")
            else:
                parts.append(f"{meta.authors[0]}, et al.")
        
        # Titel
        if meta.title:
            if meta.source_type == "article":
                parts.append(f'"{meta.title}."')
            else:
                parts.append(f"*{meta.title}*.")
        
        # Container/Journal
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
        elif meta.year:
            parts.append(f"{meta.year}.")
        
        # Publisher
        if meta.publisher:
            parts.append(f"{meta.publisher}.")
        
        return " ".join(parts)
    
    def format_inline(self, meta: LiMeta, page: Optional[int] = None) -> str:
        """MLA Inline-Zitat: (Author Page)"""
        author = meta.first_author
        
        if page:
            return f"({author} {page})"
        return f"({author})"


class ChicagoFormatter(CitationFormatter):
    """Chicago Style (Notes-Bibliography)"""
    
    def format_full(self, meta: LiMeta) -> str:
        """Chicago Vollzitat"""
        parts = []
        
        # Autoren
        if meta.authors:
            parts.append(", ".join(meta.authors) + ".")
        
        # Titel
        if meta.title:
            if meta.source_type == "article":
                parts.append(f'"{meta.title}."')
            else:
                parts.append(f"*{meta.title}*.")
        
        # Journal
        if meta.journal:
            journal = f"*{meta.journal}*"
            if meta.volume:
                journal += f" {meta.volume}"
            if meta.issue:
                journal += f", no. {meta.issue}"
            if meta.year:
                journal += f" ({meta.year})"
            if meta.pages:
                journal += f": {meta.pages}"
            parts.append(journal + ".")
        
        # Publisher
        if meta.publisher and meta.source_type in ("book", "chapter"):
            pub = meta.publisher
            if meta.year:
                pub += f", {meta.year}"
            parts.append(pub + ".")
        
        return " ".join(parts)
    
    def format_inline(self, meta: LiMeta, page: Optional[int] = None) -> str:
        """Chicago Inline: (Author Jahr, Seite)"""
        author = meta.first_author
        year = meta.year or "o.J."
        
        if page:
            return f"({author} {year}, {page})"
        return f"({author} {year})"


class DINFormatter(CitationFormatter):
    """DIN 1505-2 (Deutsche Norm)"""
    
    def format_full(self, meta: LiMeta) -> str:
        """DIN Vollzitat"""
        parts = []
        
        # Autoren
        if meta.authors:
            parts.append("; ".join(meta.authors) + ":")
        
        # Titel
        if meta.title:
            parts.append(meta.title + ".")
        
        # In: Journal
        if meta.journal:
            journal = f"In: {meta.journal}"
            if meta.volume:
                journal += f" {meta.volume}"
            if meta.year:
                journal += f" ({meta.year})"
            if meta.issue:
                journal += f", H. {meta.issue}"
            if meta.pages:
                journal += f", S. {meta.pages}"
            parts.append(journal + ".")
        
        # Verlag
        if meta.publisher:
            pub = meta.publisher
            if meta.year and not meta.journal:
                pub += f", {meta.year}"
            parts.append(pub + ".")
        
        # ISBN
        if meta.isbn:
            parts.append(f"ISBN {meta.isbn}.")
        
        return " ".join(parts)
    
    def format_inline(self, meta: LiMeta, page: Optional[int] = None) -> str:
        """DIN Inline: [Autor Jahr, S. X]"""
        author = meta.first_author
        year = meta.year or "o.J."
        
        if page:
            return f"[{author} {year}, S. {page}]"
        return f"[{author} {year}]"


class HarvardFormatter(CitationFormatter):
    """Harvard Style"""
    
    def format_full(self, meta: LiMeta) -> str:
        """Harvard Vollzitat"""
        parts = []
        
        # Autoren
        if meta.authors:
            authors = self._format_authors_list(meta.authors)
            parts.append(authors)
        
        # Jahr
        if meta.year:
            parts.append(f"({meta.year})")
        
        # Titel
        if meta.title:
            if meta.source_type == "article":
                parts.append(f"'{meta.title}',")
            else:
                parts.append(f"*{meta.title}*,")
        
        # Journal
        if meta.journal:
            journal = f"*{meta.journal}*"
            if meta.volume:
                journal += f", {meta.volume}"
            if meta.issue:
                journal += f"({meta.issue})"
            if meta.pages:
                journal += f", pp. {meta.pages}"
            parts.append(journal + ".")
        
        # Publisher
        if meta.publisher and not meta.journal:
            parts.append(f"{meta.publisher}.")
        
        return " ".join(parts)
    
    def format_inline(self, meta: LiMeta, page: Optional[int] = None) -> str:
        """Harvard Inline: (Author, Jahr, p. X)"""
        author = meta.first_author
        year = meta.year or "n.d."
        
        if page:
            return f"({author}, {year}, p. {page})"
        return f"({author}, {year})"


# Factory für einfachen Zugriff
FORMATTERS = {
    "apa": APAFormatter,
    "mla": MLAFormatter,
    "chicago": ChicagoFormatter,
    "din": DINFormatter,
    "harvard": HarvardFormatter,
}


def get_formatter(style: str) -> CitationFormatter:
    """Gibt Formatter für gegebenen Stil zurück"""
    formatter_class = FORMATTERS.get(style.lower(), APAFormatter)
    return formatter_class()
