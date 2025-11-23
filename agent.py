import os

from dotenv import load_dotenv
from pydantic_ai import Agent, Tool
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

from models import SearchResults
from search import search_tool

load_dotenv()

model = OpenAIChatModel(
    "gpt-4.1", provider=OpenAIProvider(api_key=os.getenv("OPENAI_API_KEY"))
)

web_agent = Agent(
    system_prompt="You are a research assistant. Answer questions using live web data and provide the main content explaining the topic in detail",
    tools=[Tool(search_tool, takes_ctx=False)],
    output_type=SearchResults,
    model=model,
)


async def run_agent(query):
    response = await web_agent.run(query)
    return response.output.results, response.output.main_content
