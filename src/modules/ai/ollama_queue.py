"""
LitZentrum - Ollama Queue
Warteschlange für lokale KI-Verarbeitung
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Callable
from enum import Enum
import threading
import queue
import logging

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

from PyQt6.QtCore import QObject, pyqtSignal


class JobStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class AIJob:
    """Ein KI-Verarbeitungsauftrag"""
    id: str
    job_type: str  # summarize, extract_quotes, metadata_lookup
    input_text: str
    params: dict = field(default_factory=dict)
    status: JobStatus = JobStatus.PENDING
    result: Optional[str] = None
    error: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    started_at: Optional[str] = None
    completed_at: Optional[str] = None


class OllamaQueue(QObject):
    """Warteschlange für Ollama-Anfragen"""
    
    job_started = pyqtSignal(str)  # job_id
    job_progress = pyqtSignal(str, int)  # job_id, progress
    job_completed = pyqtSignal(str, str)  # job_id, result
    job_failed = pyqtSignal(str, str)  # job_id, error
    
    def __init__(self, base_url: str = "http://localhost:11434", 
                 default_model: str = "mistral:latest"):
        super().__init__()
        
        if not HAS_REQUESTS:
            raise ImportError("requests nicht installiert")
        
        self.base_url = base_url
        self.default_model = default_model
        
        self._queue: queue.Queue = queue.Queue()
        self._jobs: dict[str, AIJob] = {}
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._job_counter = 0
    
    def is_available(self) -> bool:
        """Prüft ob Ollama erreichbar ist"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=2)
            return response.status_code == 200
        except (requests.RequestException, requests.Timeout, OSError) as e:
            logging.debug(f"Ollama nicht erreichbar: {e}")
            return False
    
    def get_models(self) -> List[str]:
        """Gibt verfügbare Modelle zurück"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get("models", [])
                return [m["name"] for m in models]
        except (requests.RequestException, requests.Timeout, ValueError, KeyError, OSError) as e:
            logging.debug(f"Fehler beim Abrufen der Ollama-Modelle: {e}")
        return []
    
    def add_job(self, job_type: str, input_text: str, 
                params: dict = None) -> str:
        """Fügt Job zur Queue hinzu"""
        self._job_counter += 1
        job_id = f"job_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{self._job_counter}"
        
        job = AIJob(
            id=job_id,
            job_type=job_type,
            input_text=input_text,
            params=params or {},
        )
        
        self._jobs[job_id] = job
        self._queue.put(job_id)
        
        # Worker starten falls nicht läuft
        self._ensure_worker()
        
        return job_id
    
    def get_job(self, job_id: str) -> Optional[AIJob]:
        """Gibt Job-Status zurück"""
        return self._jobs.get(job_id)
    
    def cancel_job(self, job_id: str) -> bool:
        """Bricht Job ab (falls noch pending)"""
        job = self._jobs.get(job_id)
        if job and job.status == JobStatus.PENDING:
            job.status = JobStatus.CANCELLED
            return True
        return False
    
    def _ensure_worker(self):
        """Stellt sicher dass Worker-Thread läuft"""
        if not self._running:
            self._running = True
            self._thread = threading.Thread(target=self._worker, daemon=True)
            self._thread.start()
    
    def _worker(self):
        """Worker-Thread für Queue-Verarbeitung"""
        while self._running:
            try:
                job_id = self._queue.get(timeout=1)
                job = self._jobs.get(job_id)
                
                if not job or job.status != JobStatus.PENDING:
                    continue
                
                self._process_job(job)
                
            except queue.Empty:
                # Queue leer, weiter warten
                pass
            except Exception as e:
                print(f"[OllamaQueue] Worker-Fehler: {e}")
    
    def _process_job(self, job: AIJob):
        """Verarbeitet einen Job"""
        job.status = JobStatus.RUNNING
        job.started_at = datetime.now().isoformat()
        self.job_started.emit(job.id)
        
        try:
            # Prompt basierend auf Job-Typ
            prompt = self._build_prompt(job)
            
            # Ollama-Anfrage
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": job.params.get("model", self.default_model),
                    "prompt": prompt,
                    "stream": False,
                },
                timeout=120,
            )
            
            if response.status_code == 200:
                result = response.json().get("response", "")
                job.result = result
                job.status = JobStatus.COMPLETED
                job.completed_at = datetime.now().isoformat()
                self.job_completed.emit(job.id, result)
            else:
                raise Exception(f"HTTP {response.status_code}")
            
        except Exception as e:
            job.error = str(e)
            job.status = JobStatus.FAILED
            job.completed_at = datetime.now().isoformat()
            self.job_failed.emit(job.id, str(e))
    
    def _build_prompt(self, job: AIJob) -> str:
        """Baut Prompt basierend auf Job-Typ"""
        text = job.input_text[:10000]  # Max 10k Zeichen
        
        if job.job_type == "summarize":
            return f"""Erstelle eine strukturierte Zusammenfassung des folgenden akademischen Textes.

Gliedere die Zusammenfassung in:
1. Hauptthese/Kernaussage
2. Methodik (falls relevant)
3. Wichtigste Ergebnisse/Argumente
4. Schlussfolgerungen

Text:
{text}

Zusammenfassung:"""

        elif job.job_type == "extract_quotes":
            return f"""Extrahiere die wichtigsten zitierfähigen Aussagen aus dem folgenden Text.

Formatiere jedes Zitat wie folgt:
- "Zitat" (Kontext/Bedeutung)

Text:
{text}

Wichtige Zitate:"""

        elif job.job_type == "metadata_lookup":
            return f"""Extrahiere bibliografische Metadaten aus dem folgenden Text.

Suche nach: Titel, Autor(en), Jahr, DOI, ISBN, Verlag, Journal

Text:
{text}

Gefundene Metadaten (JSON):"""

        else:
            return text
    
    def stop(self):
        """Stoppt den Worker"""
        self._running = False
        if self._thread:
            self._thread.join(timeout=2)
