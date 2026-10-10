# Vanguard Intelligent Agents Lab


**Group name** Vanguard  
**Jaydon Hylton (2210144)** **Chadwick Cox (1800729)** **Semoy Smith (1505625)**

Group assignment: Autonomous Agentic Workflows with Azure AI Foundry, LangChain, and DuckDB (Intelligent Agents / FDE). Stack: **gpt-4.1-mini**, **LangChain**, **DuckDB**.

## Azure

| Item | Value |
|------|--------|
| Resource | `ws-vanguard-lab1` |
| Deployment name | `gpt-4.1-mini` |
| Model version | `2025-04-14` |
| API version | `2024-10-21` |
| Guardrails | `TEMPERATURE = 0.0`, `TOKEN_BUDGET = 256` in `vanguard/azure_chat.py` |
| Local auth | `.env`: `AZURE_AI_FOUNDRY_ENDPOINT`, `AZURE_AI_FOUNDRY_KEY`, `AZURE_MODEL_NAME` |
| Identity auth | `DefaultAzureCredential` (`azure-identity`) |

## Run locally

```powershell
uv sync
Copy-Item .env.example .env
```
