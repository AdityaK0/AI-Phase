from fastapi import APIRouter
from .service import AIService
from .schema import RequestData
ai_router = APIRouter(prefix="/ai", tags=["AI"])


@ai_router.post("/process_request")
def process_request(request_data: RequestData):
    ai_service = AIService()
    response_data = ai_service.process_request(request_data.dict())
    return response_data
