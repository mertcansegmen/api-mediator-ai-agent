from typing import Optional
from pydantic import BaseModel
from tools.api_requestor import APIRequest

class ApiRequestBuilderResponse(BaseModel):
    result: str
    message: Optional[str] = None
    api_request: Optional['APIRequest'] = None
