from pydantic import BaseModel, Field


class SqlQuery(BaseModel):
    sql: str = Field(
        description="A complete BigQuery Standard SQL query to answer the user's request."
    )
