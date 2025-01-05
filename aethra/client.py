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
    def __init__(self, api_key: str, base_url: str = "http://localhost:8002"):
        """
        Initialize the ConvoLens client.

        Args:
            api_key (str): The user's API key.
            base_url (str, optional): The base URL of the ConvoLens API. Defaults to "http://localhost:8002".
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.headers = {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json"
        }

    def analyse(
        self,
        conversation_data: Dict[str, List[Dict[str, str]]],
        min_clusters: int = 5,
        max_clusters: int = 10,
        embedding_model: str = "text-embedding-ada-002",
        top_k_nearest_to_centroid: int = 10,
        tau: float = 0.1
    ) -> ConversationFlowAnalysisResponse:
        """
        Analyze conversation flow.

        Args:
            conversation_data (Dict[str, List[Dict[str, str]]]): The conversation data.
            min_clusters (int, optional): Minimum number of clusters. Defaults to 5.
            max_clusters (int, optional): Maximum number of clusters. Defaults to 10.
            embedding_model (str, optional): Embedding model to use. Defaults to "text-embedding-ada-002".
            top_k_nearest_to_centroid (int, optional): Top K nearest to centroid. Defaults to 10.
            tau (float, optional): Tau value. Defaults to 0.1.

        Returns:
            ConversationFlowAnalysisResponse: The analysis result.

        Raises:
            InvalidAPIKeyError: If the API key is invalid.
            InsufficientCreditsError: If the user has insufficient credits.
            AnalysisError: If the analysis fails.
            ConvoLensAPIError: For other API-related errors.
        """
        url = f"{self.base_url}/conversation-flow-analysis/analyse-conversation-flow"
        payload = ConversationFlowAnalysisRequest(
            conversation_data=conversation_data,
            min_clusters=min_clusters,
            max_clusters=max_clusters,
            embedding_model=embedding_model,
            top_k_nearest_to_centroid=top_k_nearest_to_centroid,
            tau=tau
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
