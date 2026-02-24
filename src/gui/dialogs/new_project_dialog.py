"""
LitZentrum - Neues Projekt Dialog
"""
from pathlib import Path

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QTextEdit, QComboBox, QPushButton,
    QDialogButtonBox, QFileDialog, QLabel
)


class NewProjectDialog(QDialog):
    """Dialog zum Erstellen eines neuen Projekts"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Neues Projekt erstellen")
        self.setMinimumSize(500, 350)
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Formular
        form = QFormLayout()
        
        # Name
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("z.B. Masterarbeit_2026")
        form.addRow("Projektname:", self.name_input)
        
        # Beschreibung
        self.desc_input = QTextEdit()
        self.desc_input.setMaximumHeight(80)
        self.desc_input.setPlaceholderText("Optionale Beschreibung...")
        form.addRow("Beschreibung:", self.desc_input)
        
        # Pfad
        path_layout = QHBoxLayout()
        self.path_input = QLineEdit()
        self.path_input.setReadOnly(True)
        path_layout.addWidget(self.path_input)
        
        browse_btn = QPushButton("📁 Auswählen...")
        browse_btn.clicked.connect(self._browse_path)
        path_layout.addWidget(browse_btn)
        
        form.addRow("Speicherort:", path_layout)
        
        # Zitationsstil
        self.style_combo = QComboBox()
        self.style_combo.addItems(["APA (7th Edition)", "MLA", "Chicago", "DIN 1505", "Harvard"])
        form.addRow("Zitationsstil:", self.style_combo)
        
        layout.addLayout(form)
        
        # Hinweis
        hint = QLabel(
            "💡 Der Projektordner wird am gewählten Ort erstellt.\n"
            "   Enthält: Quellen-Ordner, Projekt-Notizen, Aufgaben"
        )
        hint.setStyleSheet("color: #666; font-size: 11px;")
        layout.addWidget(hint)
        
        layout.addStretch()
        
        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self._validate_and_accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    
    def _browse_path(self):
        """Ordner auswählen"""
        path = QFileDialog.getExistingDirectory(
            self, "Projektordner auswählen", str(Path.home())
        )
        if path:
            # Kombiniere mit Projektname
            name = self.name_input.text() or "NeuesProjekt"
            full_path = Path(path) / name
            self.path_input.setText(str(full_path))
    
    def _validate_and_accept(self):
        """Validiert und akzeptiert"""
        from PyQt6.QtWidgets import QMessageBox
        
        if not self.name_input.text().strip():
            QMessageBox.warning(self, "Fehler", "Bitte einen Projektnamen eingeben.")
            return
        
        if not self.path_input.text():
            QMessageBox.warning(self, "Fehler", "Bitte einen Speicherort auswählen.")
            return
        
        path = Path(self.path_input.text())
        if path.exists() and list(path.iterdir()):
            QMessageBox.warning(self, "Fehler", "Der Ordner existiert bereits und ist nicht leer.")
            return
        
        self.accept()
    
    def get_data(self) -> dict:
        """Gibt die Eingabedaten zurück"""
        style_map = {
            0: "apa", 1: "mla", 2: "chicago", 3: "din", 4: "harvard"
        }
        
        return {
            "name": self.name_input.text().strip(),
            "description": self.desc_input.toPlainText().strip() or None,
            "path": Path(self.path_input.text()),
            "style": style_map[self.style_combo.currentIndex()]
        }
