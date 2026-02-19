from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider
from pathlib import Path

here = Path(__file__).parent
system_prompt = (here / "system_prompt.md").read_text()
team_information = (here / "team_information.md").read_text()

model = OpenAIChatModel(
    "openai/gpt-oss-20b",
    provider=OpenAIProvider(
        base_url="http://127.0.0.1:1234/v1",
        api_key="lm-studio",
    ),
)
agent = Agent(model, system_prompt=system_prompt)


@agent.system_prompt
def team_information_facts() -> str:
    return team_information


if __name__ == "__main__":
    agent.to_cli_sync(prog_name="pit-bot")
