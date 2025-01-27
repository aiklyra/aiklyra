import requests
from typing import Dict, List, Union
from .models import ConversationFlowAnalysisRequest, ConversationFlowAnalysisResponse
from .exceptions import (
    AiklyraAPIError,
    InvalidAPIKeyError,
    InsufficientCreditsError,
    AnalysisError,
    ValidationError
)


class AiklyraClient:
    """
    A client for interacting with the Aiklyra API to analyze conversation flows.

    This class provides methods to send conversation data to the Aiklyra API for analysis. It handles
    authentication, request formatting, and response parsing. The client supports customizable parameters
    for clustering and filtering conversation data by role.

    Attributes:
        BASE_ANALYSE_ENDPOINT (str): The endpoint for the base conversation flow analysis.
        api_key (str): The API key used for authentication.
        base_url (str): The base URL of the Aiklyra API.
        headers (Dict[str, str]): The headers for API requests, including the authorization token.

    Methods:
        __init__(api_key, base_url): Initializes the Aiklyra client with an API key and base URL.
        analyse(conversation_data, min_clusters, max_clusters, top_k_nearest_to_centroid, role):
            Sends conversation data to the Aiklyra API for analysis and returns the results.
    """
    BASE_ANALYSE_ENDPOINT = "conversation-flow-analysis/base_analyse-conversation-flow"

    def __init__(self, api_key: str, base_url: str = "http://localhost:8002"):
        """
        Initialize the Aiklyra client.

        Args:
            api_key (str): The user's API key.
            base_url (str, optional): The base URL of the Aiklyra API. Defaults to "http://localhost:8002".
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.headers = {
            "Authorization": f"Bearer {self.api_key}", 
            "Content-Type": "application/json"
        }

    def analyse(
        self,
        conversation_data: Dict[str, List[Dict[str, str]]],
        min_clusters: int = 5,
        max_clusters: int = 10,
        top_k_nearest_to_centroid: int = 10,
        role : str = "Any"
    ) -> ConversationFlowAnalysisResponse:
        """
        Analyze conversation flow.

        Args:
            conversation_data (Dict[str, List[Dict[str, str]]]): The conversation data.
            min_clusters (int, optional): Minimum number of clusters. Defaults to 5.
            max_clusters (int, optional): Maximum number of clusters. Defaults to 10.
            top_k_nearest_to_centroid (int, optional): Top K nearest to centroid. Defaults to 10.
            role (str, optional): Role to be analyzed in the conversations/behaviour track. Defaults to "Any".
        Returns:
            ConversationFlowAnalysisResponse: The analysis result.

        Raises:
            InvalidAPIKeyError: If the API key is invalid.
            InsufficientCreditsError: If the user has insufficient credits.
            AnalysisError: If the analysis fails.
            AiklyraAPIError: For other API-related errors.
        """
        if not isinstance(conversation_data, dict):
            raise ValidationError("conversation_data must be a dictionary.")
        if min_clusters <= 0 or max_clusters <= 0:
            raise ValidationError("min_clusters and max_clusters must be positive integers.")
        if min_clusters > max_clusters:
            raise ValidationError("Max clusters needs to be greater than Min Clusters")
        

        if role != "Any":
            filtered_by_role = {}
            for conv_id , conv in conversation_data.items():
                filtered_by_role[conv_id] = [msg for msg in conv if msg["role"] == role]
            conversation_data = filtered_by_role
        
        
        url = f"{self.base_url}/{AiklyraClient.BASE_ANALYSE_ENDPOINT}"
        payload = ConversationFlowAnalysisRequest(
            conversation_data=conversation_data,
            min_clusters=min_clusters,
            max_clusters=max_clusters,
            top_k_nearest_to_centroid=top_k_nearest_to_centroid,
            role = role
        ).model_dump()

        try:
            response = requests.post(url, headers=self.headers, json=payload)
        except requests.RequestException as e:
            raise AiklyraAPIError(f"Request failed: {e}")

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
                raise AiklyraAPIError(f"Forbidden: {detail}")
        else:
            raise AiklyraAPIError(f"Error {response.status_code}: {response.text}")
