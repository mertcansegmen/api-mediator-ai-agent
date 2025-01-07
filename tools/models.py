from pydantic import BaseModel, Field
from typing import Dict, Optional

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
    
class ApiRequestBuilderResponse(BaseModel):
    result: str
    message: Optional[str] = None
    api_request: Optional['APIRequest'] = None
