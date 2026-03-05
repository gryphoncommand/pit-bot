# Pit Bot

An AI assistant for your FRC competition pit. Pit Bot answers questions from judges, scouts, sponsors, and curious visitors — so your drive team can stay focused on the match.

Built by **FRC Team 3966 — Gryphon Command** at L&N STEM Academy, Knoxville, TN.

---

## What It Does

Pit Bot is a conversational AI agent that knows everything about your team. Deploy it on a laptop in your pit, point it at a local language model, and visitors can ask it questions like:

- "What does your robot do this season?"
- "How many students are on the team?"
- "What awards have you won?"
- "How do I join FRC?"

It stays on-topic (FRC and your team only), represents your team with the right tone, and never makes up facts it doesn't know.

## How It Works

```text
Visitor question
      |
      v
  Pit Bot agent  <--  system_prompt.md  (persona, rules, tone)
      |          <--  fact_file.md      (everything about your team)
      |
      v
  Local LLM  (runs on your laptop via LM Studio — no internet required)
      |
      v
  Answer
```

The entire application lives in a single Python file ([main.py](main.py)). It uses [pydantic-ai](https://github.com/pydantic/pydantic-ai) to build the agent and can run two ways:

- **CLI mode** — chat with the bot directly in your terminal
- **API server mode** — exposes an OpenAI-compatible HTTP API so any chat UI can connect to it

---

## Prerequisites

You need three things on your laptop before you start:

### 1. Python 3.13+

Check your version:

```bash
python --version
```

Download from [python.org](https://python.org) if needed.

### 2. uv (Python package manager)

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 3. LM Studio (local LLM runner)

Download from [lmstudio.ai](https://lmstudio.ai). This runs an AI model locally on your laptop — no internet or API keys needed at competition.

Once installed:

1. Download a model (the `gpt-oss-20b` or any instruction-tuned model works well)
2. Start the local server in LM Studio (usually at `http://localhost:1234`)

---

## Quick Start

```bash
# 1. Clone this repo
git clone https://github.com/gryphoncommand/pit-bot.git
cd pit-bot

# 2. Install dependencies
uv sync

# 3. Start LM Studio and load a model, then run Pit Bot in CLI mode
uv run main.py cli

# 4. Or run the API server (connect any chat UI to http://localhost:8000)
uv run main.py serve
```

That's it. The bot is running.

---

## Configuration

Pit Bot reads configuration from environment variables. The defaults work out of the box with LM Studio:

| Variable          | Default                    | What It Does                                   |
| ----------------- | -------------------------- | ---------------------------------------------- |
| `OPENAI_BASE_URL` | `http://127.0.0.1:1234/v1` | URL of your LLM backend                        |
| `OPENAI_API_KEY`  | `lm-studio`                | API key (LM Studio doesn't require a real one) |
| `MODEL_NAME`      | `openai/gpt-oss-20b`       | Model identifier                               |
| `HOST`            | `0.0.0.0`                  | Address to bind in serve mode                  |
| `PORT`            | `8000`                     | Port to listen on in serve mode                |

To override any of these, set them before running:

```bash
MODEL_NAME="my-model" uv run main.py serve
```

---

## Running with Docker

If you'd rather not install Python, you can use Docker instead.

```bash
# Build the image
docker build -t pit-bot:local .

# Run it (connects to LM Studio running on your host machine)
bash scripts/docker_run.sh
```

The Docker container runs in `serve` mode by default and exposes the API on port 8000.

---

## Adapting Pit Bot for Your Team

You only need to edit two files:

### `fact_file.md` — Your Team's Knowledge Base

This is what the bot knows about your team. Replace the Gryphon Command content with facts about your own team:

- Team number, name, school, location
- Current season robot name, game strategy, and mechanisms
- Awards history
- Team roster, coaches, and mentors
- Sponsors
- Outreach programs and community partnerships
- Anything you'd want a judge or scout to know

The more specific and accurate this file is, the better the bot answers.

### `system_prompt.md` — Bot Persona and Rules

This defines how the bot talks and what it's allowed to discuss. You can customize:

- The bot's name and identity
- Tone (enthusiastic, formal, etc.)
- Topics it will and won't answer
- Any specific instructions for your team's situation

Keep the gracious professionalism rules — never talk negatively about other teams.

---

## Testing the API

With the server running (`uv run main.py serve`), send a test message:

```bash
bash scripts/openai_api_curl.sh
```

Or manually with curl:

```bash
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "Who are you?"}]}' \
  | jq
```

The API is OpenAI-compatible, so you can point any chat frontend that supports custom OpenAI endpoints at `http://localhost:8000`.

---

## Project Structure

```text
pit-bot/
├── main.py            # Entire application — agent, CLI, and API server
├── system_prompt.md   # Bot persona, tone, and rules
├── fact_file.md       # Team knowledge base (update this every season)
├── Dockerfile         # Container build
├── pyproject.toml     # Python dependencies
└── scripts/
    ├── docker_run.sh        # Run the Docker container
    └── openai_api_curl.sh   # Test the API endpoint
```

---

## Questions or Ideas?

- Check out our [Chief Delphi Open Alliance thread](https://www.chiefdelphi.com/t/gryphon-command-3966-open-alliance-build-thread-2026/510471) — we document our build process publicly
- Find us on The Blue Alliance: [Team 3966](https://www.thebluealliance.com/team/3966)
- Instagram: [@gryphoncommand3966](https://instagram.com/gryphoncommand3966)

Feel free to fork this repo and adapt Pit Bot for your own team. Gracious Professionalism extends to open source too.
