from agents import Agent, ModelSettings, set_default_openai_client
from openai import AsyncOpenAI
from logging import getLogger

from licht.lib.config import get_settings

settings = get_settings()
logger = getLogger(__name__)

client = AsyncOpenAI(
    api_key=settings.llm_api_key,
    base_url=settings.llm_api_base
)
set_default_openai_client(client)

async def get_agent(instructions: str, temperature: float, tools: list):
    agent = Agent(
        name="licht",
        instructions=instructions,
        model=settings.llm_model,
        model_settings=ModelSettings(
            temperature=temperature,
        ),
        
        tools=tools
    )
    return agent