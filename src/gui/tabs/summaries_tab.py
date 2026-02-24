"""
LitZentrum - Zusammenfassungen Tab
"""
from typing import Optional

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem,
    QPushButton, QTextEdit, QLabel, QDialog, QDialogButtonBox,
    QLineEdit, QComboBox
)

from core import LitSource, SourceManager
from formats import LiSum, Summary


class SummariesTab(QWidget):
    """Tab für Zusammenfassungen"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.summaries: Optional[LiSum] = None
        self.source: Optional[LitSource] = None
        self.source_manager: Optional[SourceManager] = None
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Toolbar
        toolbar = QHBoxLayout()
        
        add_btn = QPushButton("➕ Neue Zusammenfassung")
        add_btn.clicked.connect(self._add_summary)
        toolbar.addWidget(add_btn)
        
        ai_btn = QPushButton("🤖 KI-Zusammenfassung")
        ai_btn.clicked.connect(self._ai_summarize)
        ai_btn.setToolTip("Zusammenfassung mit Ollama generieren")
        toolbar.addWidget(ai_btn)
        
        toolbar.addStretch()
        
        self.count_label = QLabel("0 Zusammenfassungen")
        toolbar.addWidget(self.count_label)
        
        layout.addLayout(toolbar)
        
        # Liste
        self.list_widget = QListWidget()
        self.list_widget.setAlternatingRowColors(True)
        self.list_widget.itemClicked.connect(self._on_item_clicked)
        self.list_widget.itemDoubleClicked.connect(self._edit_summary)
        layout.addWidget(self.list_widget)
        
        # Vorschau
        self.preview_label = QLabel("Vorschau:")
        layout.addWidget(self.preview_label)
        
        self.preview_text = QTextEdit()
        self.preview_text.setReadOnly(True)
        self.preview_text.setMaximumHeight(150)
        layout.addWidget(self.preview_text)
    
    def set_data(self, summaries: LiSum, source: LitSource, manager: SourceManager):
        """Setzt die Daten"""
        self.summaries = summaries
        self.source = source
        self.source_manager = manager
        self._refresh()
    
    def _refresh(self):
        """Aktualisiert die Anzeige"""
        self.list_widget.clear()
        self.preview_text.clear()
        
        if not self.summaries:
            self.count_label.setText("0 Zusammenfassungen")
            return
        
        for summary in self.summaries.summaries:
            # Icon nach Quelle
            icons = {"manual": "📝", "ai_generated": "🤖", "imported": "📥"}
            icon = icons.get(summary.source, "📋")
            
            type_str = {"full": "Gesamt", "chapter": "Kapitel", "section": "Abschnitt", "abstract": "Abstract"}
            type_label = type_str.get(summary.type, summary.type)
            
            text = f"{icon} {summary.title} ({type_label})"
            
            item = QListWidgetItem(text)
            item.setData(Qt.ItemDataRole.UserRole, summary)
            self.list_widget.addItem(item)
        
        self.count_label.setText(f"{len(self.summaries)} Zusammenfassungen")
    
    def _on_item_clicked(self, item: QListWidgetItem):
        """Zeigt Vorschau"""
        summary = item.data(Qt.ItemDataRole.UserRole)
        if summary:
            self.preview_text.setText(summary.content)
    
    def _add_summary(self):
        """Neue Zusammenfassung hinzufügen"""
        if not self.summaries or not self.source_manager:
            return
        
        dialog = SummaryDialog(self)
        if dialog.exec():
            data = dialog.get_data()
            self.summaries.add(
                title=data["title"],
                content=data["content"],
                summary_type=data["type"],
                source="manual",
                pages=data["pages"],
                tags=data["tags"]
            )
            self.source_manager.save_summaries(self.source, self.summaries)
            self._refresh()
    
    def _edit_summary(self, item: QListWidgetItem):
        """Zusammenfassung bearbeiten"""
        summary = item.data(Qt.ItemDataRole.UserRole)
        if not summary:
            return
        
        dialog = SummaryDialog(self, summary)
        if dialog.exec():
            data = dialog.get_data()
            summary.title = data["title"]
            summary.content = data["content"]
            summary.type = data["type"]
            summary.pages = data["pages"]
            summary.tags = data["tags"]
            summary.update_content(data["content"])
            
            self.source_manager.save_summaries(self.source, self.summaries)
            self._refresh()
    
    def _ai_summarize(self):
        """KI-Zusammenfassung erstellen"""
        from PyQt6.QtWidgets import QMessageBox

        if not self.source or not self.source.has_pdf:
            QMessageBox.warning(self, "Hinweis", "Keine PDF vorhanden.")
            return

        # Feature geplant: Vollständige Ollama-Integration
        # Implementierung benötigt:
        # 1. PDF-Text extrahieren (modules.pdf_workshop.extractor)
        # 2. Job an OllamaQueue senden (modules.ai.ollama_queue)
        # 3. Progress-Dialog während Verarbeitung
        # 4. Ergebnis als neue Zusammenfassung speichern
        QMessageBox.information(
            self, "KI-Zusammenfassung",
            "Die KI-Integration mit Ollama ist für zukünftige Version geplant.\n\n"
            "Vorbereitung: Stellen Sie sicher, dass Ollama läuft:\n"
            "ollama run mistral"
        )
    
    def clear(self):
        """Leert die Anzeige"""
        self.summaries = None
        self.source = None
        self.list_widget.clear()
        self.preview_text.clear()
        self.count_label.setText("0 Zusammenfassungen")


class SummaryDialog(QDialog):
    """Dialog zum Erstellen/Bearbeiten einer Zusammenfassung"""
    
    def __init__(self, parent=None, summary: Summary = None):
        super().__init__(parent)
        self.summary = summary
        self.setWindowTitle("Zusammenfassung bearbeiten" if summary else "Neue Zusammenfassung")
        self.setMinimumSize(700, 600)
        self._setup_ui()
        
        if summary:
            self._load_summary()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Titel
        title_layout = QHBoxLayout()
        title_layout.addWidget(QLabel("Titel:"))
        self.title_input = QLineEdit()
        title_layout.addWidget(self.title_input)
        layout.addLayout(title_layout)
        
        # Typ & Seiten
        row_layout = QHBoxLayout()
        
        row_layout.addWidget(QLabel("Typ:"))
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Gesamtzusammenfassung", "Kapitel", "Abschnitt", "Abstract"])
        row_layout.addWidget(self.type_combo)
        
        row_layout.addWidget(QLabel("Seiten:"))
        self.pages_input = QLineEdit()
        self.pages_input.setPlaceholderText("z.B. 1-50")
        self.pages_input.setMaximumWidth(100)
        row_layout.addWidget(self.pages_input)
        
        row_layout.addStretch()
        layout.addLayout(row_layout)
        
        # Inhalt
        layout.addWidget(QLabel("Zusammenfassung:"))
        self.content_edit = QTextEdit()
        self.content_edit.setPlaceholderText("Zusammenfassung eingeben (Markdown unterstützt)...")
        layout.addWidget(self.content_edit)
        
        # Tags
        tags_layout = QHBoxLayout()
        tags_layout.addWidget(QLabel("Tags:"))
        self.tags_input = QLineEdit()
        self.tags_input.setPlaceholderText("tag1, tag2, tag3")
        tags_layout.addWidget(self.tags_input)
        layout.addLayout(tags_layout)
        
        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save |
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    
    def _load_summary(self):
        """Lädt bestehende Zusammenfassung"""
        if self.summary:
            self.title_input.setText(self.summary.title)
            self.content_edit.setText(self.summary.content)
            
            type_map = {"full": 0, "chapter": 1, "section": 2, "abstract": 3}
            self.type_combo.setCurrentIndex(type_map.get(self.summary.type, 0))
            
            self.pages_input.setText(self.summary.pages or "")
            self.tags_input.setText(", ".join(self.summary.tags))
    
    def get_data(self) -> dict:
        """Gibt die Eingabedaten zurück"""
        type_map = {0: "full", 1: "chapter", 2: "section", 3: "abstract"}
        tags_text = self.tags_input.text()
        
        return {
            "title": self.title_input.text(),
            "content": self.content_edit.toPlainText(),
            "type": type_map[self.type_combo.currentIndex()],
            "pages": self.pages_input.text() or None,
            "tags": [t.strip() for t in tags_text.split(",") if t.strip()]
        }
