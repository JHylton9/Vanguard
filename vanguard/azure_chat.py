# **Group:** Vanguard  
# **Jaydon Hylton (2210144)**  **Chadwick Cox (1800729)**  **Semoy Smith (1505625)**
"""Load .env from the project root and build the Azure chat model."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI

# Repeatable, short replies: no sampling, and a 256-token ceiling on every call.
TEMPERATURE = 0.0
TOKEN_BUDGET = 256
AuthMode = Literal["local", "identity"]


def project_root() -> Path:
    # The notebook kernel's cwd is often not the repo root, so walk upward for pyproject.toml / .env.
    starts: list[Path] = [Path.cwd()]
    try:
        from IPython import get_ipython

        ipython = get_ipython()
    except ImportError:
        ipython = None
    if ipython is not None:
        for key in ("__vsc_ipynb_file__", "__session__"):
            value = ipython.user_ns.get(key)
            if value:
                starts.append(Path(str(value)).expanduser())
    this_file = Path(__file__).resolve().parent.parent
    starts.append(this_file)

    for start in starts:
        current = start if start.is_dir() else start.parent
        for candidate in [current, *current.parents]:
            if (candidate / "pyproject.toml").is_file() or (candidate / ".env").is_file():
                return candidate
    return Path.cwd()


def load_azure_environment() -> Path:
    # Read endpoint and key from .env so they never sit in a notebook cell.
    root = project_root()
    env_path = root / ".env"
    if not env_path.is_file():
        example = root / ".env.example"
        raise FileNotFoundError(
            f"No .env at {env_path}. Copy {example} to .env, set "
            "AZURE_AI_FOUNDRY_ENDPOINT and AZURE_AI_FOUNDRY_KEY, then select kernel "
            f"{root / '.venv' / 'Scripts' / 'python.exe'}."
        )
    load_dotenv(env_path, override=True)
    return env_path


@dataclass(frozen=True)
class AzureSettings:
    endpoint: str
    model_name: str
    api_version: str
    auth_mode: AuthMode
    api_key: str | None
    env_path: str


def load_settings(auth_mode: AuthMode | None = None) -> AzureSettings:
    env_path = load_azure_environment()
    endpoint = os.getenv("AZURE_AI_FOUNDRY_ENDPOINT", "").strip().rstrip("/")
    if not endpoint:
        raise ValueError(
            f"AZURE_AI_FOUNDRY_ENDPOINT is empty in {env_path}. "
            "Set it to https://ws-vanguard-lab1.openai.azure.com/"
        )
    # "local" keeps the Foundry key; "identity" drops it and uses Azure AD instead.
    mode = (auth_mode or os.getenv("AZURE_AUTH_MODE", "local")).strip().lower()
    if mode not in ("local", "identity"):
        raise ValueError("AZURE_AUTH_MODE must be local or identity")
    api_key = os.getenv("AZURE_AI_FOUNDRY_KEY", "").strip() or None
    if mode == "identity":
        api_key = None
    elif not api_key:
        raise ValueError(
            f"AZURE_AI_FOUNDRY_KEY is empty in {env_path}. "
            "Paste KEY 1 from Azure portal, or use AZURE_AUTH_MODE=identity after az login."
        )
    return AzureSettings(
        endpoint=endpoint,
        model_name=os.getenv("AZURE_MODEL_NAME", "gpt-4.1-mini").strip(),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-21").strip(),
        auth_mode=mode,  # type: ignore[arg-type]
        api_key=api_key,
        env_path=str(env_path),
    )


def build_chat_model(auth_mode: AuthMode | None = None) -> AzureChatOpenAI:
    cfg = load_settings(auth_mode)
    kwargs: dict[str, object] = {
        "azure_endpoint": cfg.endpoint,
        "azure_deployment": cfg.model_name,
        "api_version": cfg.api_version,
        "temperature": TEMPERATURE,
        "max_tokens": TOKEN_BUDGET,
    }
    if cfg.auth_mode == "identity":
        # Borrow a Cognitive Services token from whoever is signed in (az login, VS Code, managed identity).
        kwargs["azure_ad_token_provider"] = get_bearer_token_provider(
            DefaultAzureCredential(),
            "https://cognitiveservices.azure.com/.default",
        )
    else:
        kwargs["api_key"] = cfg.api_key
    return AzureChatOpenAI(**kwargs)
