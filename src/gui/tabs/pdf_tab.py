"""
LitZentrum - PDF Tab
Tab mit integriertem PDF-Viewer
"""
from typing import Optional
from pathlib import Path

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QPushButton, QLabel, QTextEdit, QLineEdit,
    QListWidget, QListWidgetItem, QGroupBox
)

from core import LitSource, SourceManager
from ..widgets.pdf_viewer import PDFViewer


class PDFTab(QWidget):
    """Tab mit PDF-Viewer und Werkzeugen"""
    
    quote_requested = pyqtSignal(str, int)  # Text, Seite
    note_requested = pyqtSignal(str, int)   # Text, Seite
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.source: Optional[LitSource] = None
        self.source_manager: Optional[SourceManager] = None
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Splitter: PDF links, Tools rechts
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # PDF-Viewer
        self.pdf_viewer = PDFViewer()
        self.pdf_viewer.page_changed.connect(self._on_page_changed)
        self.splitter.addWidget(self.pdf_viewer)
        
        # Rechte Seite: Tools
        tools_widget = QWidget()
        tools_layout = QVBoxLayout(tools_widget)
        tools_layout.setContentsMargins(5, 5, 5, 5)
        
        # Suche
        search_group = QGroupBox("🔍 Suche im PDF")
        search_layout = QVBoxLayout(search_group)
        
        search_row = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Suchbegriff...")
        self.search_input.returnPressed.connect(self._search_pdf)
        search_row.addWidget(self.search_input)
        
        self.search_btn = QPushButton("Suchen")
        self.search_btn.clicked.connect(self._search_pdf)
        search_row.addWidget(self.search_btn)
        search_layout.addLayout(search_row)
        
        self.search_results = QListWidget()
        self.search_results.setMaximumHeight(150)
        self.search_results.itemDoubleClicked.connect(self._on_search_result_clicked)
        search_layout.addWidget(self.search_results)
        
        tools_layout.addWidget(search_group)
        
        # Schnell-Aktionen
        actions_group = QGroupBox("⚡ Schnell-Aktionen")
        actions_layout = QVBoxLayout(actions_group)
        
        self.extract_text_btn = QPushButton("📄 Text dieser Seite extrahieren")
        self.extract_text_btn.clicked.connect(self._extract_page_text)
        actions_layout.addWidget(self.extract_text_btn)
        
        self.add_quote_btn = QPushButton("💬 Zitat von dieser Seite")
        self.add_quote_btn.clicked.connect(self._add_quote_from_page)
        actions_layout.addWidget(self.add_quote_btn)
        
        self.add_note_btn = QPushButton("📝 Notiz zu dieser Seite")
        self.add_note_btn.clicked.connect(self._add_note_for_page)
        actions_layout.addWidget(self.add_note_btn)
        
        tools_layout.addWidget(actions_group)
        
        # Seiteninfo
        info_group = QGroupBox("ℹ️ Seiten-Info")
        info_layout = QVBoxLayout(info_group)
        
        self.page_info_label = QLabel("Keine Seite geladen")
        self.page_info_label.setWordWrap(True)
        info_layout.addWidget(self.page_info_label)
        
        tools_layout.addWidget(info_group)
        
        # Text-Vorschau
        preview_group = QGroupBox("📋 Text-Vorschau")
        preview_layout = QVBoxLayout(preview_group)
        
        self.text_preview = QTextEdit()
        self.text_preview.setReadOnly(True)
        self.text_preview.setMaximumHeight(200)
        self.text_preview.setPlaceholderText("Text der aktuellen Seite...")
        preview_layout.addWidget(self.text_preview)
        
        tools_layout.addWidget(preview_group)
        
        tools_layout.addStretch()
        
        self.splitter.addWidget(tools_widget)
        
        # Splitter-Größen
        self.splitter.setSizes([700, 300])
        
        layout.addWidget(self.splitter)
    
    def set_data(self, source: LitSource, manager: SourceManager):
        """Setzt Quelle und lädt PDF"""
        self.source = source
        self.source_manager = manager
        
        if source.has_pdf:
            self.pdf_viewer.open_pdf(source.pdf_path)
            self._update_page_info()
        else:
            self.pdf_viewer.close_pdf()
            self.page_info_label.setText("Keine PDF verfügbar")
            self.text_preview.clear()
    
    def _on_page_changed(self, page: int):
        """Seite gewechselt"""
        self._update_page_info()
    
    def _update_page_info(self):
        """Aktualisiert Seiten-Info"""
        if not self.pdf_viewer.doc:
            return
        
        page = self.pdf_viewer.current_page
        total = self.pdf_viewer.page_count
        
        self.page_info_label.setText(f"Seite {page + 1} von {total}")
        
        # Text-Vorschau aktualisieren
        text = self.pdf_viewer.get_text(page)
        preview = text[:1000]
        if len(text) > 1000:
            preview += "..."
        self.text_preview.setText(preview)
    
    def _search_pdf(self):
        """Sucht im PDF"""
        query = self.search_input.text().strip()
        if not query:
            return
        
        self.search_results.clear()
        results = self.pdf_viewer.search(query)
        
        for result in results:
            item = QListWidgetItem(f"Seite {result['page']}")
            item.setData(Qt.ItemDataRole.UserRole, result['page'])
            self.search_results.addItem(item)
        
        if not results:
            self.search_results.addItem("Keine Treffer")
    
    def _on_search_result_clicked(self, item: QListWidgetItem):
        """Springt zu Suchergebnis"""
        page = item.data(Qt.ItemDataRole.UserRole)
        if page:
            self.pdf_viewer.go_to_page(page)
    
    def _extract_page_text(self):
        """Extrahiert Text der aktuellen Seite"""
        text = self.pdf_viewer.get_text()
        if text:
            self.text_preview.setText(text)
    
    def _add_quote_from_page(self):
        """Fügt Zitat von aktueller Seite hinzu"""
        page = self.pdf_viewer.current_page + 1
        # Ausgewählten Text oder Aufforderung
        self.quote_requested.emit("", page)
    
    def _add_note_for_page(self):
        """Fügt Notiz für aktuelle Seite hinzu"""
        page = self.pdf_viewer.current_page + 1
        self.note_requested.emit("", page)
    
    def clear(self):
        """Leert die Anzeige"""
        self.source = None
        self.source_manager = None
        self.pdf_viewer.close_pdf()
        self.search_results.clear()
        self.text_preview.clear()
        self.page_info_label.setText("Keine Seite geladen")
