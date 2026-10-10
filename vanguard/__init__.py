# **Group:** Vanguard  
# **Jaydon Hylton (2210144)**  **Chadwick Cox (1800729)**  **Semoy Smith (1505625)**
"""Load .env from the project root and build the Azure chat model."""
"""Vanguard advising lab — shared Azure chat configuration."""

from vanguard.azure_chat import (
    TEMPERATURE,
    TOKEN_BUDGET,
    build_chat_model,
    load_settings,
    project_root,
)

__all__ = [
    "TEMPERATURE",
    "TOKEN_BUDGET",
    "build_chat_model",
    "load_settings",
    "project_root",
]
