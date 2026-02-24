"""
LitZentrum - PDF Extractor
Extrahiert Text und Metadaten aus PDFs
"""
from pathlib import Path
from typing import Optional, Tuple
from dataclasses import dataclass
import logging

try:
    import fitz  # PyMuPDF
    HAS_PYMUPDF = True
except ImportError:
    HAS_PYMUPDF = False


@dataclass
class PDFInfo:
    """PDF-Metadaten"""
    title: Optional[str] = None
    author: Optional[str] = None
    subject: Optional[str] = None
    creator: Optional[str] = None
    page_count: int = 0
    
    
class PDFExtractor:
    """Extrahiert Inhalte aus PDFs"""
    
    def __init__(self, path: Path):
        if not HAS_PYMUPDF:
            raise ImportError("PyMuPDF nicht installiert. Bitte 'pip install PyMuPDF' ausführen.")
        
        self.path = Path(path)
        self.doc = None
    
    def open(self):
        """Öffnet das PDF"""
        self.doc = fitz.open(str(self.path))
    
    def close(self):
        """Schließt das PDF"""
        if self.doc:
            self.doc.close()
            self.doc = None
    
    def __enter__(self):
        self.open()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
    
    def get_info(self) -> PDFInfo:
        """Gibt PDF-Metadaten zurück"""
        if not self.doc:
            self.open()
        
        metadata = self.doc.metadata
        return PDFInfo(
            title=metadata.get("title"),
            author=metadata.get("author"),
            subject=metadata.get("subject"),
            creator=metadata.get("creator"),
            page_count=len(self.doc),
        )
    
    def get_page_count(self) -> int:
        """Gibt Seitenzahl zurück"""
        if not self.doc:
            self.open()
        return len(self.doc)
    
    def extract_text(self, page_num: int = None) -> str:
        """Extrahiert Text aus PDF"""
        if not self.doc:
            self.open()
        
        if page_num is not None:
            # Einzelne Seite (0-basiert)
            if 0 <= page_num < len(self.doc):
                return self.doc[page_num].get_text()
            return ""
        
        # Alle Seiten
        text_parts = []
        for page in self.doc:
            text_parts.append(page.get_text())
        return "\n\n".join(text_parts)
    
    def extract_text_range(self, start_page: int, end_page: int) -> str:
        """Extrahiert Text aus Seitenbereich"""
        if not self.doc:
            self.open()
        
        text_parts = []
        for i in range(start_page, min(end_page + 1, len(self.doc))):
            text_parts.append(self.doc[i].get_text())
        return "\n\n".join(text_parts)
    
    def get_page_image(self, page_num: int, zoom: float = 2.0) -> bytes:
        """Rendert Seite als Bild"""
        if not self.doc:
            self.open()
        
        if 0 <= page_num < len(self.doc):
            page = self.doc[page_num]
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)
            return pix.tobytes("png")
        return b""
    
    def search_text(self, query: str) -> list:
        """Sucht Text im PDF"""
        if not self.doc:
            self.open()
        
        results = []
        for page_num, page in enumerate(self.doc):
            text_instances = page.search_for(query)
            for rect in text_instances:
                results.append({
                    "page": page_num + 1,
                    "rect": (rect.x0, rect.y0, rect.x1, rect.y1),
                })
        return results


def extract_pdf_metadata(path: Path) -> Optional[PDFInfo]:
    """Schnelle Extraktion von PDF-Metadaten"""
    try:
        with PDFExtractor(path) as extractor:
            return extractor.get_info()
    except (OSError, PermissionError, ValueError, RuntimeError, ImportError) as e:
        logging.debug(f"Fehler beim Extrahieren der PDF-Metadaten aus '{path}': {e}")
        return None


def extract_pdf_text(path: Path, max_pages: int = 10) -> str:
    """Extrahiert Text aus den ersten Seiten"""
    try:
        with PDFExtractor(path) as extractor:
            page_count = min(extractor.get_page_count(), max_pages)
            return extractor.extract_text_range(0, page_count - 1)
    except (OSError, PermissionError, ValueError, RuntimeError, ImportError) as e:
        logging.debug(f"Fehler beim Extrahieren von PDF-Text aus '{path}': {e}")
        return ""
