"""
LitZentrum - Event Bus
Zentrale Event-Verteilung zwischen Modulen
"""
from PyQt6.QtCore import QObject, pyqtSignal
from enum import Enum
from typing import Any, Callable, Dict, List


class EventType(Enum):
    """Alle Event-Typen in LitZentrum"""
    
    # Projekt-Events
    PROJECT_OPENED = "project_opened"
    PROJECT_CLOSED = "project_closed"
    PROJECT_SAVED = "project_saved"
    
    # Quellen-Events
    SOURCE_SELECTED = "source_selected"
    SOURCE_CREATED = "source_created"
    SOURCE_UPDATED = "source_updated"
    SOURCE_DELETED = "source_deleted"
    
    # Notizen-Events
    NOTE_ADDED = "note_added"
    NOTE_UPDATED = "note_updated"
    NOTE_DELETED = "note_deleted"
    
    # Zitate-Events
    QUOTE_ADDED = "quote_added"
    QUOTE_UPDATED = "quote_updated"
    QUOTE_DELETED = "quote_deleted"
    
    # Aufgaben-Events
    TASK_ADDED = "task_added"
    TASK_COMPLETED = "task_completed"
    TASK_DELETED = "task_deleted"
    
    # Zusammenfassungs-Events
    SUMMARY_ADDED = "summary_added"
    SUMMARY_UPDATED = "summary_updated"
    
    # PDF-Events
    PDF_OPENED = "pdf_opened"
    PDF_PAGE_CHANGED = "pdf_page_changed"
    PDF_TEXT_SELECTED = "pdf_text_selected"
    
    # KI-Events
    AI_JOB_STARTED = "ai_job_started"
    AI_JOB_COMPLETED = "ai_job_completed"
    AI_JOB_FAILED = "ai_job_failed"
    
    # UI-Events
    STATUS_MESSAGE = "status_message"
    ERROR_MESSAGE = "error_message"
    REFRESH_VIEW = "refresh_view"


class EventBus(QObject):
    """Zentrale Event-Verteilung"""
    
    # Qt Signal für alle Events
    event_fired = pyqtSignal(str, object)  # event_type, data
    
    _instance = None
    
    def __init__(self):
        super().__init__()
        self._handlers: Dict[EventType, List[Callable]] = {}
    
    @classmethod
    def instance(cls) -> "EventBus":
        """Gibt die Singleton-Instanz des EventBus zurück.

        Returns:
            EventBus: Die globale EventBus-Instanz
        """
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def subscribe(self, event_type: EventType, handler: Callable[[Any], None]):
        """Registriert einen Handler für einen bestimmten Event-Typ.

        Args:
            event_type: Der Event-Typ für den der Handler registriert werden soll
            handler: Callback-Funktion die aufgerufen wird wenn das Event auftritt
        """
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        if handler not in self._handlers[event_type]:
            self._handlers[event_type].append(handler)
    
    def unsubscribe(self, event_type: EventType, handler: Callable):
        """Entfernt einen registrierten Handler für einen Event-Typ.

        Args:
            event_type: Der Event-Typ von dem der Handler entfernt werden soll
            handler: Die zu entfernende Callback-Funktion
        """
        if event_type in self._handlers:
            if handler in self._handlers[event_type]:
                self._handlers[event_type].remove(handler)
    
    def emit(self, event_type: EventType, data: Any = None):
        """Sendet ein Event an alle registrierten Handler.

        Das Event wird sowohl als Qt Signal als auch direkt an alle
        registrierten Handler gesendet. Handler-Fehler werden abgefangen
        und geloggt ohne den Event-Fluss zu unterbrechen.

        Args:
            event_type: Der Typ des zu sendenden Events
            data: Optionale Daten die an die Handler übergeben werden
        """
        # Qt Signal
        self.event_fired.emit(event_type.value, data)

        # Direkte Handler
        if event_type in self._handlers:
            for handler in self._handlers[event_type]:
                try:
                    handler(data)
                except Exception as e:
                    print(f"[EventBus] Handler-Fehler bei {event_type.value}: {e}")
    
    def clear(self):
        """Entfernt alle Handler"""
        self._handlers.clear()


# Globale Instanz
def get_event_bus() -> EventBus:
    """Gibt die globale EventBus-Instanz zurück"""
    return EventBus.instance()
