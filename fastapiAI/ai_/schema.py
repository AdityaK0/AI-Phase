
from pydantic import BaseModel,Field
from datetime import datetime

class RequestData(BaseModel):
    prompt:str = Field(..., description="The prompt to be processed by the AI model.",required=True)
    time_at:datetime = Field(default_factory=datetime.utcnow, description="The timestamp when the request was made.")   
    
    