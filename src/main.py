"""
LitZentrum - Literaturverwaltung
Haupteinstiegspunkt
"""
import sys
from pathlib import Path

# Füge src zum Pfad hinzu
src_path = Path(__file__).parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

from gui import MainWindow


def main():
    """Startet LitZentrum"""
    # High-DPI Unterstützung
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    app = QApplication(sys.argv)
    app.setApplicationName("LitZentrum")
    app.setOrganizationName("LitZentrum")
    app.setApplicationVersion("1.0.0")
    
    # Style
    app.setStyle("Fusion")
    
    # Icon (falls vorhanden)
    icon_path = Path(__file__).parent.parent / "resources" / "icons" / "litzentrum.ico"
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))
    
    # Hauptfenster
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
