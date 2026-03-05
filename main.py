#!/usr/bin/env python3
"""Pit Bot agent code."""

import os
import typer
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider
from pathlib import Path
from agentic.openai import OpenAICompatibleAPI

## Global Variables

OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL", "http://127.0.0.1:1234/v1")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "lm-studio")
MODEL_NAME = os.environ.get("MODEL_NAME", "openai/gpt-oss-20b")
SYSTEM_PROMPT_PATH = "system_prompt.md"

here = Path(__file__).parent
system_prompt = (here / SYSTEM_PROMPT_PATH).read_text()
fact_file = (here / "fact_file.md").read_text()

model = OpenAIChatModel(
    MODEL_NAME,
    provider=OpenAIProvider(
        base_url=OPENAI_BASE_URL,
        api_key=OPENAI_API_KEY,
    ),
)
agent = Agent(model, system_prompt=system_prompt)


@agent.system_prompt
def fact_file_contents() -> str:
    return fact_file


# -------------------------------------------------------------------------------------------------
# Pit Bot Agent
# -------------------------------------------------------------------------------------------------

app = typer.Typer(no_args_is_help=True, help="Pit Bot Agent")


@app.command(short_help="Command Line Interface (CLI)")
def cli():
    """Command Line Interface (CLI)."""
    agent.to_cli_sync(prog_name="pit-bot")


@app.command(short_help="OpenAI Compatible API Interface")
def serve(host: str | None = None, port: int | None = None):
    """OpenAI Compatible API interface."""

    host = host or os.environ.get("HOST", "0.0.0.0")
    port = port or int(os.environ.get("PORT", 8000))

    openai_api = OpenAICompatibleAPI(
        agent=agent,
        title="Pit Bot OpenAI Compatible API",
        description="OpenAI-compatible API for the Pit Bot.",
        model_name=MODEL_NAME,
    )

    openai_api.run(host=host, port=port)


if __name__ == "__main__":
    app()
