"""
LitZentrum - Projektbaum Panel
Zeigt die Projektstruktur als Baum
"""
from pathlib import Path
from typing import Optional
import logging

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTreeWidget, QTreeWidgetItem,
    QLabel, QHeaderView
)

from core import LitProject, LitSource


class ProjectTreePanel(QWidget):
    """Panel mit Projektbaum"""
    
    source_selected = pyqtSignal(object)  # LitSource
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.project: Optional[LitProject] = None
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Header
        header = QLabel("📚 Projekt")
        header.setStyleSheet("font-weight: bold; padding: 5px;")
        layout.addWidget(header)
        
        # Baum
        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.setIndentation(15)
        self.tree.itemClicked.connect(self._on_item_clicked)
        self.tree.itemDoubleClicked.connect(self._on_item_double_clicked)
        layout.addWidget(self.tree)
    
    def set_project(self, project: LitProject):
        """Setzt das aktuelle Projekt"""
        self.project = project
        self._build_tree()
    
    def _build_tree(self):
        """Baut den Projektbaum auf"""
        self.tree.clear()
        
        if not self.project:
            return
        
        # Projekt-Root
        root = QTreeWidgetItem([f"📚 {self.project.name}"])
        root.setData(0, Qt.ItemDataRole.UserRole, ("project", self.project))
        root.setExpanded(True)
        self.tree.addTopLevelItem(root)
        
        # Quellen-Ordner
        sources_item = QTreeWidgetItem(["📁 Quellen"])
        sources_item.setData(0, Qt.ItemDataRole.UserRole, ("folder", "sources"))
        root.addChild(sources_item)
        
        # Quellen laden
        sources_path = self.project.sources_path
        if sources_path.exists():
            for folder in sorted(sources_path.iterdir()):
                if folder.is_dir():
                    meta_file = folder / "meta.limeta"
                    if meta_file.exists():
                        from formats import LiMeta
                        try:
                            meta = LiMeta.load(meta_file)
                            from core import LitSource
                            source = LitSource(path=folder, meta=meta)

                            icon = "📄" if source.has_pdf else "📝"
                            item = QTreeWidgetItem([f"{icon} {meta.first_author} ({meta.year or '?'})"])
                            item.setToolTip(0, meta.title)
                            item.setData(0, Qt.ItemDataRole.UserRole, ("source", source))
                            sources_item.addChild(item)
                        except (OSError, PermissionError, ValueError, KeyError, AttributeError) as e:
                            logging.debug(f"Fehler beim Laden von Quelle '{folder.name}': {e}")
        
        sources_item.setExpanded(True)
        
        # Projekt-Notizen
        notes_item = QTreeWidgetItem(["📝 Projekt-Notizen"])
        notes_item.setData(0, Qt.ItemDataRole.UserRole, ("file", "notes"))
        root.addChild(notes_item)
        
        # Projekt-Aufgaben
        tasks_item = QTreeWidgetItem(["✅ Projekt-Aufgaben"])
        tasks_item.setData(0, Qt.ItemDataRole.UserRole, ("file", "tasks"))
        root.addChild(tasks_item)
    
    def _on_item_clicked(self, item: QTreeWidgetItem, column: int):
        """Item wurde angeklickt"""
        data = item.data(0, Qt.ItemDataRole.UserRole)
        if data and data[0] == "source":
            self.source_selected.emit(data[1])
    
    def _on_item_double_clicked(self, item: QTreeWidgetItem, column: int):
        """Item wurde doppelt angeklickt"""
        data = item.data(0, Qt.ItemDataRole.UserRole)
        if data and data[0] == "source":
            source = data[1]
            if source.has_pdf:
                # PDF öffnen (später implementieren)
                pass
    
    def clear(self):
        """Leert den Baum"""
        self.tree.clear()
        self.project = None
    
    def refresh(self):
        """Aktualisiert den Baum"""
        if self.project:
            self._build_tree()
