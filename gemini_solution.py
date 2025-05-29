import requests
import base64
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Function to call Gemini (or LLM) API and pass the image
def analyze_image_with_gemini(image_bytes):
    # Convert image to base64 (if required by Gemini API)
    image_base64 = base64.b64encode(image_bytes).decode('utf-8')

    # Example API request (replace with actual Gemini API details)
    api_url = "https://gemini-api.google.com/analyze-image"
    headers = {
        "Authorization": GEMINI_API_KEY,  # Replace with your actual Gemini API key
        "Content-Type": "application/json"
    }

    # Payload for API call
    payload = {
        "image_data": image_base64,
        "task": "analyze_food_or_equipment_issue"
    }

    # Retry mechanism
    retry_strategy = Retry(
        total=3,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS", "POST"],  # Updated this line
        backoff_factor=1
    )

    adapter = HTTPAdapter(max_retries=retry_strategy)
    http = requests.Session()
    http.mount("https://", adapter)

    try:
        # Make request to Gemini API
        response = http.post(api_url, json=payload, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses

        # Parse the result returned by the Gemini API
        return response.json().get("solution", "No solution provided")
    except requests.exceptions.RequestException as e:
        return f"Error in analyzing the image: {e}"

# Example function to handle image solution
def get_solution_from_gemini(image):
    return analyze_image_with_gemini(image)