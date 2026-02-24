"""
LitZentrum - Projekt-Manager
Verwaltet Literaturprojekte (Ordner-basiert)
"""
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional
import shutil

from formats import LiProj, LiTask, LiNote


@dataclass
class LitProject:
    """Repräsentiert ein Literaturprojekt"""
    path: Path
    config: LiProj
    
    @property
    def name(self) -> str:
        return self.config.name
    
    @property
    def sources_path(self) -> Path:
        return self.path / self.config.sources_folder
    
    @property
    def project_tasks_path(self) -> Path:
        return self.path / "projekt_tasks.litask"
    
    @property
    def project_notes_path(self) -> Path:
        return self.path / "projekt_notes.linote"
    
    @property
    def bibliography_path(self) -> Path:
        return self.path / "projekt_biblio.bib"


class ProjectManager:
    """Verwaltet Literaturprojekte"""
    
    PROJECT_CONFIG_FILE = "projekt_config.liproj"
    
    def __init__(self):
        self.recent_projects: List[Path] = []
        self.current_project: Optional[LitProject] = None
    
    def create_project(self, path: Path, name: str, 
                       description: str = None,
                       citation_style: str = "apa") -> LitProject:
        """Erstellt ein neues Projekt"""
        path = Path(path)
        
        # Ordner erstellen
        path.mkdir(parents=True, exist_ok=True)
        
        # Projekt-Konfiguration
        config = LiProj(
            name=name,
            description=description,
            citation_style=citation_style,
        )
        config.save(path / self.PROJECT_CONFIG_FILE)
        
        # Quellen-Ordner
        sources_path = path / config.sources_folder
        sources_path.mkdir(exist_ok=True)
        
        # Leere Projekt-Dateien
        LiTask().save(path / "projekt_tasks.litask")
        LiNote().save(path / "projekt_notes.linote")
        
        project = LitProject(path=path, config=config)
        self.current_project = project
        self._add_to_recent(path)
        
        return project
    
    def open_project(self, path: Path) -> LitProject:
        """Öffnet ein bestehendes Projekt"""
        path = Path(path)
        config_path = path / self.PROJECT_CONFIG_FILE
        
        if not config_path.exists():
            raise FileNotFoundError(f"Kein LitZentrum-Projekt in: {path}")
        
        config = LiProj.load(config_path)
        project = LitProject(path=path, config=config)
        
        self.current_project = project
        self._add_to_recent(path)
        
        return project
    
    def is_project(self, path: Path) -> bool:
        """Prüft ob Pfad ein gültiges Projekt ist"""
        return (Path(path) / self.PROJECT_CONFIG_FILE).exists()
    
    def get_source_folders(self, project: LitProject = None) -> List[Path]:
        """Gibt alle Quellen-Ordner zurück"""
        project = project or self.current_project
        if not project:
            return []
        
        sources_path = project.sources_path
        if not sources_path.exists():
            return []
        
        return [p for p in sources_path.iterdir() if p.is_dir()]
    
    def get_project_tasks(self, project: LitProject = None) -> LiTask:
        """Lädt projektweite Aufgaben"""
        project = project or self.current_project
        if not project:
            return LiTask()
        
        task_path = project.project_tasks_path
        if task_path.exists():
            return LiTask.load(task_path)
        return LiTask()
    
    def save_project_tasks(self, tasks: LiTask, project: LitProject = None):
        """Speichert projektweite Aufgaben"""
        project = project or self.current_project
        if project:
            tasks.save(project.project_tasks_path)
    
    def get_project_notes(self, project: LitProject = None) -> LiNote:
        """Lädt projektweite Notizen"""
        project = project or self.current_project
        if not project:
            return LiNote()
        
        notes_path = project.project_notes_path
        if notes_path.exists():
            return LiNote.load(notes_path)
        return LiNote()
    
    def save_project_notes(self, notes: LiNote, project: LitProject = None):
        """Speichert projektweite Notizen"""
        project = project or self.current_project
        if project:
            notes.save(project.project_notes_path)
    
    def _add_to_recent(self, path: Path):
        """Fügt Projekt zu Recent-Liste hinzu"""
        path = Path(path).resolve()
        if path in self.recent_projects:
            self.recent_projects.remove(path)
        self.recent_projects.insert(0, path)
        self.recent_projects = self.recent_projects[:10]  # Max 10
    
    def close_project(self):
        """Schließt aktuelles Projekt"""
        self.current_project = None
