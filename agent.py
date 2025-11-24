import os

from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

from models import SqlQuery

load_dotenv()

model = OpenAIChatModel(
    "gpt-4.1", provider=OpenAIProvider(api_key=os.getenv("OPENAI_API_KEY"))
)


def build_sql_agent(gameweek: int, schema_text: str) -> Agent[SqlQuery]:
    system = f"""
You are a BigQuery SQL generator. Output a single BigQuery Standard SQL query as `sql`.

Use ONLY the following schema when choosing tables/columns. If the user asks for fields not present here, choose the closest valid fields or ask for clarification.
\nSCHEMA CONTEXT\n{schema_text}\nEND SCHEMA CONTEXT\n
Rules:
- SELECT statements only; no DDL/DML or scripting.
- Use Standard SQL and fully-qualified tables: `plfpl-production.ism_GW{gameweek}.<table>`.
- Prefer explicit column lists and safe aggregations; avoid SELECT * unless needed.
- Include sensible LIMITs for non-aggregate queries (e.g., LIMIT 100).
"""
    return Agent(system_prompt=system, output_type=SqlQuery, model=model)


async def run_agent(query: str, gameweek: int, schema_text: str) -> str:
    agent = build_sql_agent(gameweek, schema_text)
    resp = await agent.run(query)
    return resp.output.sql
