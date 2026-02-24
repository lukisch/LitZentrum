"""
LitZentrum - LiProj Format (.liproj)
Projekt-Konfiguration
"""
from dataclasses import dataclass, field
from typing import Optional

from .base import LitFormat, now_iso


@dataclass
class LiProj(LitFormat):
    """Projekt-Konfiguration"""
    
    FILE_EXTENSION = ".liproj"
    SCHEMA_FILE = "liproj.schema.json"
    
    name: str
    description: Optional[str] = None
    citation_style: str = "apa"
    language: str = "de"
    sources_folder: str = "Quellen"
    schema_version: str = "1.0.0"
    created_at: str = field(default_factory=now_iso)
    updated_at: str = field(default_factory=now_iso)
    
    def to_dict(self) -> dict:
        return {
            "schema_version": self.schema_version,
            "name": self.name,
            "description": self.description,
            "citation_style": self.citation_style,
            "language": self.language,
            "sources_folder": self.sources_folder,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "LiProj":
        return cls(
            name=data.get("name", "Neues Projekt"),
            description=data.get("description"),
            citation_style=data.get("citation_style", "apa"),
            language=data.get("language", "de"),
            sources_folder=data.get("sources_folder", "Quellen"),
            schema_version=data.get("schema_version", "1.0.0"),
            created_at=data.get("created_at", now_iso()),
            updated_at=data.get("updated_at", now_iso()),
        )
    
    def update(self):
        """Aktualisiert updated_at Zeitstempel"""
        self.updated_at = now_iso()
