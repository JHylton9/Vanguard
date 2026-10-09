# Vanguard Intelligent Agents Lab

**Jaydon Hylton (2210144)** · **Chadwick Cox (1800729)** · **Semoy Smith (1505625)**

Group assignment: autonomous academic advising with Azure AI Foundry (`gpt-4.1-mini`), LangChain, Pydantic structured output, and DuckDB.

## Deliverables

Each notebook is independently runnable (local Jupyter or Google Colab).

| Part | File |
|------|------|
| 1 | `Vanguard_part1_workflow_azure.ipynb` |
| 2 | `Vanguard_part2_chat_model.ipynb` |
| 3 | `Vanguard_part3_structured_io.ipynb` |
| 4 | `Vanguard_part4_duckdb_tool_agent.ipynb` |

Supporting data: `data/student_transcripts.csv` (Part 4 also writes this file from the notebook).

## Local setup

```powershell
uv sync
Copy-Item .env.example .env
```

```env
AZURE_AI_FOUNDRY_ENDPOINT=https://ws-vanguard-lab1.openai.azure.com/
AZURE_AI_FOUNDRY_KEY=
AZURE_MODEL_NAME=gpt-4.1-mini
AZURE_OPENAI_API_VERSION=2024-10-21
AZURE_AUTH_MODE=local
```

Kernel: `.venv/Scripts/python.exe`

## Google Colab

`AZURE_OPENAI_API_VERSION` must be `2024-10-21` (REST API version). Model version `2025-04-14` is the Foundry deployment setting only.