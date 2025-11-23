from pydantic import BaseModel, Field
from typing import List


# Each individual search result
class SearchResult(BaseModel):
    title: str
    url: str
    snippet: str


# Final Agent output
class SearchResults(BaseModel):
    results: List[SearchResult]
    main_content: str = Field(description="The main content of the blog")
