"""
logger.py – Configuración de logging para RAADBot.
"""

import logging
import sys
from rich.logging import RichHandler

def setup_logger(name: str = "raadbot"):
    """Configura un logger que usa Rich para una salida elegante."""
    logging.basicConfig(
        level="INFO",
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True, show_path=False)]
    )
    return logging.getLogger(name)

logger = setup_logger()
