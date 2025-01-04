import requests
from pydantic import ValidationError
import json
import re
import os
from tools.api_requestor import APIRequest, send_request
from api_request_builders.models import ApiRequestBuilderResponse
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('DEEPSEEK_API_KEY')
API_URL = "https://api.deepseek.com/chat/completions"

system_prompt = """
You are an advanced HTTP request builder for coincap v2 REST API. Your task is to analyze user prompts and generate structured HTTP request objects in JSON format. Follow these rules:

1. **Understand the Intent**:
   - Extract the necessary information from the user’s prompt.
   - Identify the API, endpoint, and parameters required to fulfill the request.

2. **Construct the HTTP Request Object**:
   - Include the following fields in the JSON response:
     - **method**: The HTTP method (e.g., GET, POST, PUT, PATCH, DELETE).
     - **server**: The base server URL of the API, which is currently "https://api.coincap.io".
     - **path**: The endpoint path, such as "v2/assets/bitcoin/history".
     - **query**: A dictionary of query parameters (if applicable).
     - **headers**: A dictionary of required headers (e.g., for authentication, but the coincap api does not need authentication.).
     - **body**: The request body, applicable for POST/PUT methods, but all coincap endpoints are currently GET.

3. **Output Requirements**:
   - Always return a valid JSON object.
   - Ensure the response is correctly structured for execution.
   - Do not include explanations or comments.

4. **Behavior**:
   - If the coincap API is not capable of fulfilling the request, return an object with property "error" explaining the reason why you can not answer.
   - For time-based data, infer or calculate UNIX timestamps as required.
   - Use the language of the prompt to generate the response.

5. **Additional Notes**:
    - If "start" and "end" timestamps are needed, the "end" timestamp must be greater than the "start" timestamp. CoinCap's API requires the "end" timestamp to be greater than the "start" timestamp.
    - Today is 4th January 2025, 00:21 AM.


### Example Interaction:

**User Prompt**: "What was the Bitcoin price on April 20, 2024?"

**Response**:
```json
{
    "method": "GET",
    "server": "https://api.coincap.io",
    "path": "/v2/assets/bitcoin/history",
    "query": {
        "interval": "d1",
        "start": "1713571200000",
        "end": "1713657600000"
    },
    "headers": null,
    "body": null
}
"""

# Some additional info for you:
# - Today is 2025-01-01 10.21 PM.

# TODO: find a way to get the current date and time and let the model know.
# TODO: make chaining with multiple api calls.

def generate_response_from_api_response(initial_user_prompt: str, api_response: dict) -> str:
    """
    Generates a human-readable response by sending the initial prompt and API response to DeepSeek Chat.

    Args:
        initial_user_prompt (str): The initial user prompt.
        api_response (dict): The response from the CoinCap API.

    Returns:
        str: A human-readable response.
    """
    try:
        # Prepare the prompt for DeepSeek Chat
        prompt = f"""
        The user asked: "{initial_user_prompt}".
        The API returned the following response: {api_response}.
        Please provide a human-readable response based on the user's prompt and the API response.
        """

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}",
        }

        data = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant that generates human-readable responses based on API data."},
                {"role": "user", "content": prompt}
            ],
            "stream": False
        }

        # Send the request to DeepSeek Chat
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()

        # Extract the assistant's response
        response_data = response.json()
        assistant_content = response_data["choices"][0]["message"]["content"]

        return assistant_content

    except requests.RequestException as e:
        print(f"Error calling DeepSeek API: {e}")
        return "Sorry, I couldn't generate a response. Please try again later."

def generate_api_request(user_prompt: str) -> ApiRequestBuilderResponse:
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}",
        }
        
        data = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "stream": False
        }
        
        response = requests.post(API_URL, headers=headers, json=data)
        
        response.raise_for_status()

        response_data = response.json()
        assistant_content = response_data["choices"][0]["message"]["content"]

        if not assistant_content:
            print("No assistant content.")
            return None

        assistant_content = re.sub(r'```json|```', '', assistant_content).strip()

        parsed_content = json.loads(assistant_content)
        
        if parsed_content is None:
            print("Assistant returned null.")
            return None

        # If LLM returns an error message, return it
        if(parsed_content.get("error")):
            error_message_from_llm = parsed_content.get("error")
            return ApiRequestBuilderResponse(result="error", message=error_message_from_llm, api_request=None)
        
        api_request = APIRequest(**parsed_content)
        return ApiRequestBuilderResponse(result="success", message=None, api_request=api_request)
    
    except (json.JSONDecodeError, ValidationError, KeyError, IndexError) as e:
        # log: f"Error parsing the assistant's response: {e}"
        print(f"Error parsing the assistant's response: {e}")

        return ApiRequestBuilderResponse(
            result="error", 
            message="An unknown error occured", 
            api_request=None
        )
    
    except requests.RequestException as e:
        # log: f"Error calling DeepSeek API: {e}"
        print(f"Error calling DeepSeek API: {e}")

        return ApiRequestBuilderResponse(
            result="error", 
            message="An unknown error occured", 
            api_request=None
        )
    
def generate_human_readable_response(user_prompt: str):
    api_request_builder_response = generate_api_request(user_prompt)

    if api_request_builder_response.result == "success":
        print(f"Generated API Request:")
        print(api_request_builder_response.api_request.json())
        print()

        api_requestor_response = send_request(api_request_builder_response.api_request)
        if api_requestor_response.result == "success":
            print(f"API Response:")
            print(api_requestor_response.api_response)
            print()

            human_readable_response = generate_response_from_api_response(user_prompt, api_requestor_response.api_response)
            return human_readable_response
        else:
            return api_requestor_response.message
    else:
        return api_request_builder_response.message
