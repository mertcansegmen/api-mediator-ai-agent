import requests
from pydantic import BaseModel
from typing import Optional
from tools.models import APIRequest
import json

class ApiRequestorResponse(BaseModel):
    result: str
    message: Optional[str] = None
    api_response: Optional[str] = None

def send_request(api_request: APIRequest) -> ApiRequestorResponse:
    try:
        url = api_request.to_full_url()
        response = requests.request(
            method=api_request.method,
            url=url,
            headers=api_request.headers,
            json=api_request.body,  # Body is sent as JSON
        )

        response.raise_for_status()  # Raise an error for bad status codes
        
        return ApiRequestorResponse(result="success", api_response=json.dumps(response.json()))
    except requests.exceptions.RequestException as e:
        print(f"API Request failed: {e}")
        return ApiRequestorResponse(result="error", message="An error occurred during the API request.")
