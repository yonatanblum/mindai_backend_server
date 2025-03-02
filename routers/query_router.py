from fastapi import APIRouter, HTTPException
from schemas.query_service_schemas.query_schemas import QueryRequest
from services.query_service.query_processor import QueryProcessor  # ✅ Correct import

router = APIRouter()
query_processor = QueryProcessor()


@router.post("/process_query", response_model=dict)
async def process_query(request: QueryRequest):
    """
    Endpoint to process user queries using GPT-4o.
    """
    try:
        intent, params = await query_processor.process_query(request.query)
        if not intent:
            raise HTTPException(status_code=400, detail="Query could not be processed")

        return {"intent": intent, "params": params}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
