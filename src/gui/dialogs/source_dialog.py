"""
LitZentrum - Quellen Dialog
"""
from pathlib import Path
from typing import Optional

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QTabWidget,
    QLineEdit, QTextEdit, QComboBox, QPushButton, QSpinBox,
    QDialogButtonBox, QFileDialog, QLabel, QWidget
)

from formats import LiMeta


class SourceDialog(QDialog):
    """Dialog zum Erstellen/Bearbeiten einer Quelle"""
    
    def __init__(self, parent=None, meta: LiMeta = None):
        super().__init__(parent)
        self.meta = meta
        self.pdf_path: Optional[Path] = None
        
        self.setWindowTitle("Quelle bearbeiten" if meta else "Neue Quelle")
        self.setMinimumSize(600, 550)
        self._setup_ui()
        
        if meta:
            self._load_meta()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Tabs
        tabs = QTabWidget()
        
        # Tab 1: Basis-Metadaten
        basic_tab = QWidget()
        basic_layout = QFormLayout(basic_tab)
        
        # Titel
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Titel der Quelle")
        basic_layout.addRow("Titel*:", self.title_input)
        
        # Autoren
        self.authors_input = QLineEdit()
        self.authors_input.setPlaceholderText("Nachname1, Vorname1; Nachname2, Vorname2")
        basic_layout.addRow("Autoren:", self.authors_input)
        
        # Jahr
        self.year_spin = QSpinBox()
        self.year_spin.setRange(0, 2100)
        self.year_spin.setSpecialValueText("Unbekannt")
        self.year_spin.setValue(2024)
        basic_layout.addRow("Jahr:", self.year_spin)
        
        # Typ
        self.type_combo = QComboBox()
        self.type_combo.addItems([
            "Artikel", "Buch", "Buchkapitel", "Thesis", 
            "Konferenz", "Website", "Sonstiges"
        ])
        basic_layout.addRow("Typ:", self.type_combo)
        
        # PDF
        pdf_layout = QHBoxLayout()
        self.pdf_label = QLabel("Keine PDF ausgewählt")
        self.pdf_label.setStyleSheet("color: #666;")
        pdf_layout.addWidget(self.pdf_label)
        
        pdf_btn = QPushButton("📄 PDF auswählen...")
        pdf_btn.clicked.connect(self._select_pdf)
        pdf_layout.addWidget(pdf_btn)
        basic_layout.addRow("PDF:", pdf_layout)
        
        tabs.addTab(basic_tab, "Basis")
        
        # Tab 2: Erweitert
        extended_tab = QWidget()
        extended_layout = QFormLayout(extended_tab)
        
        # DOI
        self.doi_input = QLineEdit()
        self.doi_input.setPlaceholderText("10.1234/example.2024")
        extended_layout.addRow("DOI:", self.doi_input)
        
        # ISBN
        self.isbn_input = QLineEdit()
        self.isbn_input.setPlaceholderText("978-3-16-148410-0")
        extended_layout.addRow("ISBN:", self.isbn_input)
        
        # Verlag
        self.publisher_input = QLineEdit()
        extended_layout.addRow("Verlag:", self.publisher_input)
        
        # Journal
        self.journal_input = QLineEdit()
        extended_layout.addRow("Journal:", self.journal_input)
        
        # Volume/Issue/Pages
        vol_layout = QHBoxLayout()
        self.volume_input = QLineEdit()
        self.volume_input.setPlaceholderText("Vol")
        self.volume_input.setMaximumWidth(60)
        vol_layout.addWidget(self.volume_input)
        
        vol_layout.addWidget(QLabel("("))
        self.issue_input = QLineEdit()
        self.issue_input.setPlaceholderText("Issue")
        self.issue_input.setMaximumWidth(60)
        vol_layout.addWidget(self.issue_input)
        vol_layout.addWidget(QLabel(")"))
        
        self.pages_input = QLineEdit()
        self.pages_input.setPlaceholderText("S. 1-20")
        self.pages_input.setMaximumWidth(80)
        vol_layout.addWidget(self.pages_input)
        vol_layout.addStretch()
        
        extended_layout.addRow("Vol/Issue/Seiten:", vol_layout)
        
        # URL
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("https://...")
        extended_layout.addRow("URL:", self.url_input)
        
        tabs.addTab(extended_tab, "Erweitert")
        
        # Tab 3: Tags & Notizen
        notes_tab = QWidget()
        notes_layout = QFormLayout(notes_tab)
        
        # Tags
        self.tags_input = QLineEdit()
        self.tags_input.setPlaceholderText("tag1, tag2, tag3")
        notes_layout.addRow("Tags:", self.tags_input)
        
        # Abstract
        self.abstract_input = QTextEdit()
        self.abstract_input.setMaximumHeight(150)
        self.abstract_input.setPlaceholderText("Abstract/Zusammenfassung...")
        notes_layout.addRow("Abstract:", self.abstract_input)
        
        # Sprache
        self.language_combo = QComboBox()
        self.language_combo.addItems(["Deutsch", "Englisch", "Französisch", "Spanisch", "Andere"])
        notes_layout.addRow("Sprache:", self.language_combo)
        
        tabs.addTab(notes_tab, "Tags & Abstract")
        
        layout.addWidget(tabs)
        
        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save |
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self._validate_and_accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    
    def _select_pdf(self):
        """PDF auswählen"""
        path, _ = QFileDialog.getOpenFileName(
            self, "PDF auswählen", str(Path.home()),
            "PDF-Dateien (*.pdf)"
        )
        if path:
            self.pdf_path = Path(path)
            self.pdf_label.setText(f"📄 {self.pdf_path.name}")
            self.pdf_label.setStyleSheet("color: green;")
            
            # Titel aus Dateinamen, wenn leer
            if not self.title_input.text():
                self.title_input.setText(self.pdf_path.stem)
    
    def _load_meta(self):
        """Lädt bestehende Metadaten"""
        if not self.meta:
            return
        
        self.title_input.setText(self.meta.title)
        self.authors_input.setText("; ".join(self.meta.authors))
        self.year_spin.setValue(self.meta.year or 0)
        
        type_map = {"article": 0, "book": 1, "chapter": 2, "thesis": 3, 
                    "conference": 4, "website": 5, "other": 6}
        self.type_combo.setCurrentIndex(type_map.get(self.meta.source_type, 0))
        
        self.doi_input.setText(self.meta.doi or "")
        self.isbn_input.setText(self.meta.isbn or "")
        self.publisher_input.setText(self.meta.publisher or "")
        self.journal_input.setText(self.meta.journal or "")
        self.volume_input.setText(self.meta.volume or "")
        self.issue_input.setText(self.meta.issue or "")
        self.pages_input.setText(self.meta.pages or "")
        self.url_input.setText(self.meta.url or "")
        
        self.tags_input.setText(", ".join(self.meta.tags))
        self.abstract_input.setText(self.meta.abstract or "")
        
        lang_map = {"de": 0, "en": 1, "fr": 2, "es": 3}
        self.language_combo.setCurrentIndex(lang_map.get(self.meta.language, 4))
    
    def _validate_and_accept(self):
        """Validiert und akzeptiert"""
        from PyQt6.QtWidgets import QMessageBox
        
        if not self.title_input.text().strip():
            QMessageBox.warning(self, "Fehler", "Bitte einen Titel eingeben.")
            return
        
        self.accept()
    
    def get_meta(self) -> LiMeta:
        """Gibt LiMeta-Objekt zurück"""
        type_map = {0: "article", 1: "book", 2: "chapter", 3: "thesis",
                    4: "conference", 5: "website", 6: "other"}
        lang_map = {0: "de", 1: "en", 2: "fr", 3: "es", 4: "other"}
        
        # Autoren parsen
        authors_text = self.authors_input.text()
        authors = [a.strip() for a in authors_text.split(";") if a.strip()]
        
        # Tags parsen
        tags_text = self.tags_input.text()
        tags = [t.strip() for t in tags_text.split(",") if t.strip()]
        
        return LiMeta(
            title=self.title_input.text().strip(),
            authors=authors,
            year=self.year_spin.value() if self.year_spin.value() > 0 else None,
            source_type=type_map[self.type_combo.currentIndex()],
            doi=self.doi_input.text().strip() or None,
            isbn=self.isbn_input.text().strip() or None,
            publisher=self.publisher_input.text().strip() or None,
            journal=self.journal_input.text().strip() or None,
            volume=self.volume_input.text().strip() or None,
            issue=self.issue_input.text().strip() or None,
            pages=self.pages_input.text().strip() or None,
            url=self.url_input.text().strip() or None,
            tags=tags,
            abstract=self.abstract_input.toPlainText().strip() or None,
            language=lang_map[self.language_combo.currentIndex()],
            source_file=self.pdf_path.name if self.pdf_path else None,
        )
    
    def get_pdf_path(self) -> Optional[Path]:
        """Gibt PDF-Pfad zurück"""
        return self.pdf_path
