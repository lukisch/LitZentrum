"""
LitZentrum - Settings Manager
Verwaltung der Benutzereinstellungen
"""
from pathlib import Path
from typing import Any, Dict, List, Optional
import json
import logging

from PyQt6.QtCore import QSettings


class SettingsManager:
    """Verwaltet Benutzereinstellungen"""
    
    DEFAULTS = {
        # Allgemein
        "language": "de",
        "theme": "light",
        
        # Zitation
        "default_citation_style": "apa",
        "auto_generate_citation_key": True,
        
        # PDF
        "pdf_zoom_default": 100,
        "pdf_highlight_color": "#FFFF00",
        
        # KI
        "ai_enabled": False,
        "ai_model": "mistral:latest",
        "ai_base_url": "http://localhost:11434",
        
        # Fenster
        "window_geometry": None,
        "window_state": None,
        "splitter_sizes": [200, 300, 400],
        
        # Letzte Projekte
        "recent_projects": [],
        "last_project": None,
        
        # Editor
        "editor_font_family": "Consolas",
        "editor_font_size": 11,
        
        # Backup
        "auto_backup": True,
        "backup_interval_minutes": 30,
        "backup_path": None,
    }
    
    def __init__(self, app_name: str = "LitZentrum"):
        self.settings = QSettings("LitZentrum", app_name)
        self._cache: Dict[str, Any] = {}
    
    def get(self, key: str, default: Any = None) -> Any:
        """Holt Einstellung"""
        if key in self._cache:
            return self._cache[key]
        
        # Default aus DEFAULTS oder Parameter
        if default is None:
            default = self.DEFAULTS.get(key)
        
        value = self.settings.value(key, default)
        
        # Typ-Konvertierung für bestimmte Keys
        if key in ("splitter_sizes", "recent_projects"):
            if isinstance(value, str):
                try:
                    value = json.loads(value)
                except (json.JSONDecodeError, ValueError, TypeError) as e:
                    logging.debug(f"Fehler beim JSON-Parsing für '{key}': {e}")
                    value = default
        elif key in ("ai_enabled", "auto_backup", "auto_generate_citation_key"):
            if isinstance(value, str):
                value = value.lower() == "true"
        elif key in ("pdf_zoom_default", "editor_font_size", "backup_interval_minutes"):
            try:
                value = int(value)
            except (ValueError, TypeError) as e:
                logging.debug(f"Fehler beim int-Parsing für '{key}': {e}")
                value = default
        
        self._cache[key] = value
        return value
    
    def set(self, key: str, value: Any):
        """Setzt Einstellung"""
        self._cache[key] = value
        
        # Listen als JSON speichern
        if isinstance(value, (list, dict)):
            value = json.dumps(value)
        
        self.settings.setValue(key, value)
    
    def remove(self, key: str):
        """Entfernt Einstellung"""
        if key in self._cache:
            del self._cache[key]
        self.settings.remove(key)
    
    def get_recent_projects(self) -> List[Path]:
        """Gibt letzte Projekte zurück"""
        paths = self.get("recent_projects", [])
        return [Path(p) for p in paths if Path(p).exists()]
    
    def add_recent_project(self, path: Path):
        """Fügt Projekt zur Recent-Liste hinzu"""
        path = str(Path(path).resolve())
        recent = self.get("recent_projects", [])
        
        if path in recent:
            recent.remove(path)
        recent.insert(0, path)
        recent = recent[:10]  # Max 10
        
        self.set("recent_projects", recent)
        self.set("last_project", path)
    
    def sync(self):
        """Synchronisiert Einstellungen"""
        self.settings.sync()
        self._cache.clear()
    
    def reset_to_defaults(self):
        """Setzt alle Einstellungen zurück"""
        self.settings.clear()
        self._cache.clear()


# Globale Instanz
_settings_instance: Optional[SettingsManager] = None

def get_settings() -> SettingsManager:
    """Gibt globale Settings-Instanz zurück"""
    global _settings_instance
    if _settings_instance is None:
        _settings_instance = SettingsManager()
    return _settings_instance
