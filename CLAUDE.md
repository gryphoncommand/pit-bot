# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

Pit Bot is an AI assistant for FRC Team 3966 (Gryphon Command). It answers questions from pit visitors at robotics competitions. The bot runs as either a CLI or an OpenAI-compatible HTTP API server.

## Commands

This project uses `uv` for dependency management.

```bash
# Install dependencies
uv sync

# Run CLI mode (interactive chat)
uv run python main.py cli

# Run API server mode (OpenAI-compatible, defaults to 0.0.0.0:8000)
uv run python main.py serve

# Run API server with custom host/port
uv run python main.py serve --host 127.0.0.1 --port 9000

# Build Docker image
docker build -t pit-bot:local .

# Run Docker container (connects to LM Studio on host)
bash scripts/docker_run.sh

# Test the API endpoint
bash scripts/openai_api_curl.sh
```

## Architecture

**Entry point:** `main.py` — single file containing the entire application.

**Two modes via typer CLI:**

- `cli` — interactive terminal chat using pydantic-ai's built-in CLI
- `serve` — starts an OpenAI-compatible HTTP API via the `agentic` library

**Agent construction:**

- Uses `pydantic-ai` `Agent` with an `OpenAIChatModel` pointed at any OpenAI-compatible endpoint
- System prompt is loaded from `system_prompt.md` at startup
- `fact_file.md` is injected as a dynamic system prompt via `@agent.system_prompt` decorator
- Both files are read once at import time from the same directory as `main.py`

**Key dependency — `agentic`:** Sourced from a private git fork (`github.com/cmlccie/agentic`) rather than PyPI. This provides `OpenAICompatibleAPI` which wraps the pydantic-ai agent with FastAPI to expose OpenAI-compatible endpoints. See `pyproject.toml` `[tool.uv.sources]` for the override.

**Configuration via environment variables:**

| Variable          | Default                    | Purpose                         |
| ----------------- | -------------------------- | ------------------------------- |
| `OPENAI_BASE_URL` | `http://127.0.0.1:1234/v1` | LLM backend (LM Studio default) |
| `OPENAI_API_KEY`  | `lm-studio`                | API key for backend             |
| `MODEL_NAME`      | `openai/gpt-oss-20b`       | Model identifier                |
| `HOST`            | `0.0.0.0`                  | Serve mode bind address         |
| `PORT`            | `8000`                     | Serve mode port                 |

**Docker:** The `Dockerfile` inherits from `ghcr.io/cmlccie/agentic/python:latest` (base image from the same `agentic` fork). It copies `main.py`, `system_prompt.md`, `fact_file.md`, and `README.md` into `/app`, sets `main.py` as the entrypoint, and defaults to `serve` mode.

## Content Files

- `system_prompt.md` — defines Pit Bot's persona, scope, tone, and constraints
- `fact_file.md` — structured reference document about Team 3966 injected into every conversation; update this after each competition season
