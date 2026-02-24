"""
LitZentrum - AI Module
Lokale KI-Integration mit Ollama
"""
from .ollama_queue import OllamaQueue, AIJob, JobStatus

__all__ = [
    "OllamaQueue",
    "AIJob",
    "JobStatus",
]
