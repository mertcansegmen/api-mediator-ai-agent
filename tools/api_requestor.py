import requests
from pydantic import BaseModel, Field
from typing import Dict, Optional
import json

class APIRequest(BaseModel):
    method: str = Field(..., pattern="^(GET|POST|PUT|PATCH|DELETE)$")  # HTTP methods
    server: str  # Base server URL (e.g., "https://api.coincap.io")
    path: str  # Endpoint path (e.g., "/v2/assets/bitcoin/history")
    query: Optional[Dict[str, str]] = None  # Query parameters
    headers: Optional[Dict[str, str]] = None  # Headers
    body: Optional[Dict] = None  # Body for POST/PUT requests

    def to_full_url(self) -> str:
        """Construct the full URL including query parameters."""
        if self.query:
            query_string = "&".join([f"{key}={value}" for key, value in self.query.items()])
            return f"{self.server}{self.path}?{query_string}"
        return f"{self.server}{self.path}"

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
