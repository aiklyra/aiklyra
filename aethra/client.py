import requests
from typing import Dict, List, Union
from .models import ConversationFlowAnalysisRequest, ConversationFlowAnalysisResponse
from .exceptions import (
    AethraAPIError,
    InvalidAPIKeyError,
    InsufficientCreditsError,
    AnalysisError
)


class AethraClient:
    BASE_ANALYSE_ENDPOINT = "conversation-flow-analysis/base_analyse-conversation-flow"

    def __init__(self, api_key: str, base_url: str = "http://localhost:8002"):
        """
        Initialize the Aethra client.

        Args:
            api_key (str): The user's API key.
            base_url (str, optional): The base URL of the Aethra API. Defaults to "http://localhost:8002".
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",  # Use Authorization header
            "Content-Type": "application/json"
        }

    def analyse(
        self,
        conversation_data: Dict[str, List[Dict[str, str]]],
        min_clusters: int = 5,
        max_clusters: int = 10,
        top_k_nearest_to_centroid: int = 10,
    ) -> ConversationFlowAnalysisResponse:
        """
        Analyze conversation flow.

        Args:
            conversation_data (Dict[str, List[Dict[str, str]]]): The conversation data.
            min_clusters (int, optional): Minimum number of clusters. Defaults to 5.
            max_clusters (int, optional): Maximum number of clusters. Defaults to 10.
            top_k_nearest_to_centroid (int, optional): Top K nearest to centroid. Defaults to 10.
        Returns:
            ConversationFlowAnalysisResponse: The analysis result.

        Raises:
            InvalidAPIKeyError: If the API key is invalid.
            InsufficientCreditsError: If the user has insufficient credits.
            AnalysisError: If the analysis fails.
            AethraAPIError: For other API-related errors.
        """
        if not isinstance(conversation_data, dict):
            raise ValueError("conversation_data must be a dictionary.")
        if min_clusters <= 0 or max_clusters <= 0:
            raise ValueError("min_clusters and max_clusters must be positive integers.")
        if min_clusters > max_clusters:
            raise ValueError("Max clusters needs to be greater than Min Clusters")

        url = f"{self.base_url}/{AethraClient.BASE_ANALYSE_ENDPOINT}"
        payload = ConversationFlowAnalysisRequest(
            conversation_data=conversation_data,
            min_clusters=min_clusters,
            max_clusters=max_clusters,
            top_k_nearest_to_centroid=top_k_nearest_to_centroid,
        ).model_dump()

        try:
            response = requests.post(url, headers=self.headers, json=payload)
        except requests.RequestException as e:
            raise AethraAPIError(f"Request failed: {e}")

        if response.status_code == 200:
            try:
                return ConversationFlowAnalysisResponse(**response.json())
            except Exception as e:
                raise AnalysisError(f"Failed to parse response: {e}")
        elif response.status_code == 403:
            detail = response.json().get("detail", "")
            if "Invalid API Key" in detail:
                raise InvalidAPIKeyError("Invalid API Key.")
            elif "Insufficient credits" in detail:
                raise InsufficientCreditsError("Insufficient credits.")
            else:
                raise AethraAPIError(f"Forbidden: {detail}")
        else:
            raise AethraAPIError(f"Error {response.status_code}: {response.text}")
