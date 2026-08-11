from pydantic import BaseModel, Field


class QueryRequest(BaseModel):

    query: str
    k: int = Field(
        default=5,
        ge=1,
        le=20,
    )


class Source(BaseModel):

    title: str
    citation: str
    case_id: str
    decision_date: str
    chunk_number: int
    score: float
    preview: str


class RetrievalStats(BaseModel):

    retrieved: int
    latency: float
    avg_score: float


class QueryResponse(BaseModel):

    answer: str
    sources: list[Source]
    stats: RetrievalStats