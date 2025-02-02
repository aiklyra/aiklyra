import requests
from typing import Dict, List, Any, Optional
from pydantic import BaseModel
from aiklyra.models import (
    ConversationFlowAnalysisRequest ,
    JobSubmissionResponse,
    JobStatusResponse
) 
from aiklyra.exceptions import (
    AiklyraAPIError,
    AnalysisError,
    ValidationError,
)




class AiklyraClient:
    """
    A client for interacting with the Aiklyra API to analyze conversation flows.

    This client now uses asynchronous endpoints:
      - Submitting the conversation analysis job returns a job_id.
      - The job status endpoint returns the job status, including results when ready.

    Attributes:
        BASE_ANALYSE_ENDPOINT (str): The endpoint for submitting conversation analysis jobs.
        JOB_STATUS_ENDPOINT (str): The base endpoint for checking job status.
        base_url (str): The base URL of the Aiklyra API.
        headers (Dict[str, str]): The headers for API requests.
    
    Methods:
        __init__(base_url): Initializes the Aiklyra client with the base URL.
        submit_analysis(conversation_data, ...): Submits the conversation analysis job and returns a job_id.
        check_job_status(job_id): Checks the status of a submitted job.
    """
    BASE_ANALYSE_ENDPOINT = "conversation-flow-analysis/analyse-conversation"
    JOB_STATUS_ENDPOINT = "conversation-flow-analysis/job-status"

    def __init__(self, base_url: str = "http://localhost:8002"):
        """
        Initialize the Aiklyra client.

        Args:
            base_url (str, optional): The base URL of the Aiklyra API. Defaults to "http://localhost:8002".
        """
        self.base_url = base_url.rstrip('/')
        self.headers = {
            "Content-Type": "application/json",
            "accept": "application/json"
        }

    def submit_analysis(
        self,
        conversation_data: Dict[str, List[Dict[str, str]]],
        min_clusters: int = 5,
        max_clusters: int = 10,
        top_k_nearest_to_centroid: int = 10,
        role: str = "Any"
    ) -> JobSubmissionResponse:
        """
        Submit a conversation analysis job.

        The analysis is asynchronous. This method submits the job and returns a job_id.

        Args:
            conversation_data (Dict[str, List[Dict[str, str]]]): The conversation data.
            min_clusters (int, optional): Minimum number of clusters. Defaults to 5.
            max_clusters (int, optional): Maximum number of clusters. Defaults to 10.
            top_k_nearest_to_centroid (int, optional): Top K nearest to centroid. Defaults to 10.
            role (str, optional): Role to be analyzed in the conversations. Defaults to "Any".

        Returns:
            JobSubmissionResponse: Contains the job_id for the submitted job.

        Raises:
            InsufficientCreditsError: If the user has insufficient credits.
            AnalysisError: If the analysis fails.
            AiklyraAPIError: For other API-related errors.
        """
        if not isinstance(conversation_data, dict):
            raise ValidationError("conversation_data must be a dictionary.")
        if min_clusters <= 0 or max_clusters <= 0:
            raise ValidationError("min_clusters and max_clusters must be positive integers.")
        if min_clusters > max_clusters:
            raise ValidationError("max_clusters must be greater than or equal to min_clusters.")

        # If a specific role is provided, filter the conversation data accordingly.
        if role != "Any":
            filtered_by_role = {}
            for conv_id, conv in conversation_data.items():
                filtered_by_role[conv_id] = [msg for msg in conv if msg.get("role") == role]
            conversation_data = filtered_by_role

        url = f"{self.base_url}/{AiklyraClient.BASE_ANALYSE_ENDPOINT}"
        # Build the payload using the ConversationFlowAnalysisRequest model.
        payload = ConversationFlowAnalysisRequest(
            conversation_data=conversation_data,
            min_clusters=min_clusters,
            max_clusters=max_clusters,
            top_k_nearest_to_centroid=top_k_nearest_to_centroid,
            role=role
        ).model_dump()

        try:
            response = requests.post(url, headers=self.headers, json=payload)
        except requests.RequestException as e:
            raise AiklyraAPIError(f"Request failed: {e}")

        if response.status_code == 200:
            try:
                return JobSubmissionResponse(**response.json())
            except Exception as e:
                raise AnalysisError(f"Failed to parse job submission response: {e}")
        else:
            raise AiklyraAPIError(f"Error {response.status_code}: {response.text}")

    def check_job_status(self, job_id: str) -> JobStatusResponse:
        """
        Check the status of a submitted job.

        Args:
            job_id (str): The ID of the job to check.

        Returns:
            JobStatusResponse: The current status of the job, including results if available.

        Raises:
            AiklyraAPIError: If the API call fails or returns an unexpected status.
        """
        url = f"{self.base_url}/{AiklyraClient.JOB_STATUS_ENDPOINT}/{job_id}"
        try:
            response = requests.get(url, headers=self.headers)
        except requests.RequestException as e:
            raise AiklyraAPIError(f"Request failed: {e}")

        if response.status_code == 200:
            try:
                return JobStatusResponse(**response.json())
            except Exception as e:
                raise AnalysisError(f"Failed to parse job status response: {e}")
        else:
            raise AiklyraAPIError(f"Error {response.status_code}: {response.text}")
