import requests
from pydantic import BaseModel, ValidationError, field_validator
from typing import List, Optional, Dict, Literal
import json
import re
import os
from tools.api_requestor import APIRequest, send_request
from tools.deepseek import call_deepseek
from api_request_builders.models import ApiRequestBuilderResponse
from dotenv import load_dotenv

load_dotenv()

class ResponseExample(BaseModel):
    method: Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"]
    server: str
    path: str
    query: Optional[Dict[str, str]] = None
    headers: Optional[Dict[str, str]] = None
    body: Optional[str] = None

class InteractionExample(BaseModel):
    prompt: str
    response: str

    @field_validator('response')
    def validate_response_is_response_example(cls, value):
        try:
            # Parse the string into a JSON object
            parsed_json = json.loads(value)
            # Validate the JSON against the ResponseExample model
            ResponseExample(**parsed_json)
        except json.JSONDecodeError:
            raise ValueError("response must be a valid JSON string")
        except ValueError as e:
            raise ValueError(f"response JSON does not match ResponseExample schema: {e}")
        return value

def _create_system_prompt (api: str) -> str:
    """
    Create a system prompt based on the API name.

    Args:
        api (str): The name of the API(coincap, nager or weatherapi).

    Returns:
        str: The system prompt for the API.
    """

    if api == "coincap":
        api_name = "CoinCap v2"
        api_server = "https://api.coincap.io"
        api_example_path = "v2/assets/bitcoin/history"
        additional_info = '''
            - If 'start' and 'end' timestamps are needed, the 'end' timestamp must be greater than the 'start' timestamp. CoinCap's API requires the 'end' timestamp to be greater than the 'start' timestamp.
        '''
        examples = [
            InteractionExample(
                prompt="What was the Bitcoin price on April 20, 2024?",
                response='''{
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
                }'''
            ),
            InteractionExample(
                prompt="Get the current price of Ethereum.",
                response='''{
                    "method": "GET",
                    "server": "https://api.coincap.io",
                    "path": "/v2/assets/ethereum",
                    "query": null,
                    "headers": null,
                    "body": null
                }'''
            )
        ]
    elif api == "nager":
        api_name = "Nager.Date v3"
        api_server = "https://date.nager.at"
        api_example_path = "api/v3/NextPublicHolidays/US"
        additional_info = ""
        examples = [
            InteractionExample(
                prompt="What are the next public holidays in the United States?",
                response='''{
                    "method": "GET",
                    "server": "https://date.nager.at",
                    "path": "/api/v3/NextPublicHolidays/US",
                    "query": null,
                    "headers": null,
                    "body": null
                }'''
            ),
            InteractionExample(
                prompt="What are the public holidays in France in 2025?",
                response='''{
                    "method": "GET",
                    "server": "https://date.nager.at",
                    "path": "/api/v3/PublicHolidays/2025/FR",
                    "query": null,
                    "headers": null,
                    "body": null
                }'''
            )
        ]
    elif api == "weatherapi":
        api_name = "WeatherAPI"
        api_server = "http://api.weatherapi.com/v1"
        api_example_path = "/current.json"
        additional_info = f"""
            "You need an API key to access WeatherAPI's free plan. "
            "Include 'key={os.getenv('WEATHER_API_KEY')}' as a query parameter."
        """
        examples = [
            InteractionExample(
                prompt="What is the current weather in New York City?",
                response=f'''{{
                    "method": "GET",
                    "server": "http://api.weatherapi.com/v1",
                    "path": "/current.json",
                    "query": {{
                        "q": "New York City",
                        "key": "{os.getenv('WEATHER_API_KEY')}"
                    }},
                    "headers": null,
                    "body": null
                }}'''
            ),
            InteractionExample(
                prompt="What is the weather forecast for Tokyo for the next 3 days?",
                response=f'''{{
                    "method": "GET",
                    "server": "http://api.weatherapi.com/v1",
                    "path": "/forecast.json",
                    "query": {{
                        "q": "Tokyo",
                        "days": "3",
                        "key": "{os.getenv('WEATHER_API_KEY')}"
                    }},
                    "headers": null,
                    "body": null
                }}'''
            )
        ]
    else:
        raise ValueError("Invalid API name. Please provide a valid API name.")        
    
    system_prompt = f"""
        You are an advanced HTTP request builder for {api_name} API. Your task is to analyze user prompts and generate structured HTTP request objects in JSON format. Follow these rules:

        1. **Understand the Intent**:
            - Extract the necessary information from the user’s prompt.
            - Identify the API, endpoint, and parameters required to fulfill the request.
        
        2. **Construct the HTTP Request Object**:
            - Include the following fields in the JSON response:
                - **method**: The HTTP method (e.g., GET, POST, PUT, PATCH, DELETE).
                - **server**: The base server URL of the API, which is currently "{api_server}".
                - **path**: The endpoint path, such as "{api_example_path}".
                - **query**: A dictionary of query parameters (if applicable).
                - **headers**: A dictionary of required headers (e.g., for authentication, but the coincap api does not need authentication.).
                - **body**: The request body, applicable for POST/PUT methods, but all coincap endpoints are currently GET.
        
        3. **Output Requirements**:
            - Always return a valid JSON object.
            - Ensure the response is correctly structured for execution.
            - Do not include explanations or comments.

        4. **Behavior**:
            - If the API is not capable of fulfilling the request, return an object with property "error" explaining the reason why you can not answer.
            - Use the language of the prompt to generate the response.
        
        ### Additional Notes:
            {additional_info}

        ### Example Interaction:
        """
    
    for example in examples:
        system_prompt += f"""
        **User Prompt**: "{example.prompt}"
        
        **Response**:
        ```json
        {example.response}
        ```
        """

    return system_prompt

def _generate_api_request(user_prompt: str, system_prompt) -> ApiRequestBuilderResponse:
    try:
        response_data = call_deepseek(user_prompt, system_prompt)
        
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
    
def _generate_human_readable_response_from_api_response(initial_user_prompt: str, api_response: dict) -> str:
    """
    Generates a human-readable response by sending the initial prompt and API response to DeepSeek Chat.

    Args:
        initial_user_prompt (str): The initial user prompt.
        api_response (dict): The response from the API.

    Returns:
        str: A human-readable response.
    """
    try:
        usr_prompt = f"""
        The user asked: "{initial_user_prompt}".
        The API returned the following response: {api_response}.
        Please provide a human-readable response based on the user's prompt and the API response.
        """
        sys_prompt = "You are a helpful assistant that generates human-readable responses based on API data."
        response_data = call_deepseek(usr_prompt, sys_prompt)
        assistant_content = response_data["choices"][0]["message"]["content"]

        return assistant_content

    except requests.RequestException as e:
        print(f"Error calling DeepSeek API: {e}")
        return "Sorry, I couldn't generate a response. Please try again later."

def make_humanized_api_request(user_prompt: str, api: str) -> str:
    """
    Given a user prompt and an API name, generate a human-readable response.

    Args:
    user_prompt (str): The user prompt that was sent to the API.
    api (str): The name of the API(coincap, nager or weatherapi nager).

    Returns:
    str: A human-readable response.
    """

    system_prompt_for_request_builder = _create_system_prompt(api)

    api_request_builder_response = _generate_api_request(user_prompt, system_prompt_for_request_builder)

    if api_request_builder_response.result == "success":
        print(f"Generated API Request:")
        print(api_request_builder_response.api_request.json())
        print()

        api_requestor_response = send_request(api_request_builder_response.api_request)
        if api_requestor_response.result == "success":
            print(f"API Response:")
            print(api_requestor_response.api_response)
            print()

            human_readable_response = _generate_human_readable_response_from_api_response(user_prompt, api_requestor_response.api_response)
            return human_readable_response
        else:
            return api_requestor_response.message
    else:
        return api_request_builder_response.message