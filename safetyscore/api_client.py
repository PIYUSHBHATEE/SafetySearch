import httpx
from typing import Any, Dict, Optional, Tuple

class ApiClient:
    """A reusable helper class for making API requests to the openFDA API."""

    async def make_request(
        self, url: str, params: Optional[Dict[str, Any]]
    ) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """
        Makes an asynchronous GET request and handles common errors.

        Args:
            url: The URL to make the request to.
            params: A dictionary of query parameters for the request.

        Returns:
            A tuple containing (data, error_message).
            If the request is successful, data is the JSON response and error_message is None.
            If the request fails, data is None and error_message is a formatted string.
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params)
                response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
                return response.json(), None
        except httpx.HTTPStatusError as e:
            error_message = f"Error fetching data from API: {e.response.status_code} {e.response.reason_phrase}"
            return None, error_message
        except Exception as e:
            error_message = f"An unexpected error occurred: {e}"
            return None, error_message 