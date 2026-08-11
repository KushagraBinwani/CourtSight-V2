from fastapi import APIRouter

from app.schemas import (
    QueryRequest,
    QueryResponse,
    Source,
)
from app.services import courtsight


router = APIRouter()


@router.post(
    "/query",
    response_model=QueryResponse,
)
def query(
    request: QueryRequest,
):

    response = courtsight.answer(
        query=request.query,
    )

    sources = []

    for result in response["results"]:

        chunk = result.embedded_chunk.chunk

        preview = (
            chunk.text[:300] + "..."
            if len(chunk.text) > 300
            else chunk.text
        )

        sources.append(
            Source(
                title=chunk.title,
                citation=chunk.case_id,
                case_id=chunk.case_id,
                decision_date="",
                chunk_number=chunk.chunk_number,
                score=round(result.score, 4),
                preview=preview,
            )
        )

    return QueryResponse(
        answer=response["answer"],
        sources=sources,
        stats=response["stats"],
    )