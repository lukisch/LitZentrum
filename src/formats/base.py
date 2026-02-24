"""
LitZentrum - Basis-Klasse für alle Dateiformate
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Type, TypeVar
import json
import jsonschema

T = TypeVar('T', bound='LitFormat')


class LitFormatError(Exception):
    """Fehler beim Verarbeiten eines LitFormat"""
    pass


class LitValidationError(LitFormatError):
    """Validierungsfehler"""
    pass


class LitFormat(ABC):
    """Abstrakte Basisklasse für alle .li* Dateiformate"""
    
    SCHEMA_VERSION = "1.0.0"
    FILE_EXTENSION: str = ""
    SCHEMA_FILE: str = ""
    
    _schema_cache: Dict[str, dict] = {}
    
    @classmethod
    def get_schema(cls) -> dict:
        """Lädt und cached das JSON-Schema"""
        if cls.SCHEMA_FILE not in cls._schema_cache:
            schema_path = Path(__file__).parent.parent.parent / "schemas" / cls.SCHEMA_FILE
            if schema_path.exists():
                with open(schema_path, 'r', encoding='utf-8') as f:
                    cls._schema_cache[cls.SCHEMA_FILE] = json.load(f)
            else:
                cls._schema_cache[cls.SCHEMA_FILE] = {}
        return cls._schema_cache[cls.SCHEMA_FILE]
    
    @abstractmethod
    def to_dict(self) -> dict:
        """Konvertiert zu Dictionary für JSON-Speicherung"""
        pass
    
    @classmethod
    @abstractmethod
    def from_dict(cls: Type[T], data: dict) -> T:
        """Erstellt Instanz aus Dictionary"""
        pass
    
    def validate(self) -> bool:
        """Validiert gegen JSON-Schema"""
        schema = self.get_schema()
        if not schema:
            return True  # Kein Schema = keine Validierung
        
        try:
            jsonschema.validate(self.to_dict(), schema)
            return True
        except jsonschema.ValidationError as e:
            raise LitValidationError(f"Validierungsfehler: {e.message}")
    
    def save(self, path: Path) -> None:
        """Speichert in Datei"""
        self.validate()
        
        path = Path(path)
        if not path.suffix:
            path = path.with_suffix(self.FILE_EXTENSION)
        
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2, default=str)
    
    @classmethod
    def load(cls: Type[T], path: Path) -> T:
        """Lädt aus Datei"""
        path = Path(path)
        
        if not path.exists():
            raise LitFormatError(f"Datei nicht gefunden: {path}")
        
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return cls.from_dict(data)


def generate_id(prefix: str = "") -> str:
    """Generiert eine eindeutige ID"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    return f"{prefix}{timestamp}" if prefix else timestamp


def now_iso() -> str:
    """Gibt aktuelle Zeit als ISO-String zurück"""
    return datetime.now().isoformat()
