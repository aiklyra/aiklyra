from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any, Literal

class Utterance(BaseModel):
    """
    Represents a single utterance in a conversation.

    Attributes:
        role (str): The role of the speaker (e.g., "user", "assistant"). Defaults to "user".
        content (str): The content of the utterance. Defaults to an empty string.
    """
    role: str = Field(default="user")
    content: str = Field(default="")


class ConversationFlowAnalysisRequest(BaseModel):
    """
    Represents a request for conversation flow analysis.

    This class encapsulates the data required to analyze the flow of conversations, including
    the conversation data, clustering parameters, and other analysis options.

    Attributes:
        conversation_data (Dict[str, List[Utterance]]): A dictionary where keys are conversation IDs
            and values are lists of utterances in the conversation.
        min_clusters (Optional[int]): The minimum number of clusters to generate. This roughly corresponds
            to the maximum expected number of intents (actions or behaviors) exhibited by the analyzed
            agent in the interactions. Defaults to 5.
        max_clusters (Optional[int]): The maximum number of clusters to generate. This roughly corresponds
            to the minimum expected number of intents (actions or behaviors) exhibited by the analyzed
            agent in the interactions. Defaults to 10.
        top_k_nearest_to_centroid (int): The number of nearest utterances to include for each cluster centroid.
            Defaults to 10.
    """
    conversation_data: Dict[str, List[Utterance]]
    min_clusters: Optional[int] = Field(default=5)
    max_clusters: Optional[int] = Field(default=10)
    top_k_nearest_to_centroid: int = Field(default=10)


class ConversationFlowAnalysisResponse(BaseModel):
    """
    Represents the response from a conversation flow analysis.

    This class encapsulates the results of the analysis, including the transition matrix and
    the mapping of clusters to intents.

    Attributes:
        transition_matrix (List[List[float]]): A 2D matrix representing transition probabilities
            between conversation states or clusters.
        intent_by_cluster (Dict[int, str]): A dictionary mapping cluster IDs to their corresponding
            intents or labels.
    """
    transition_matrix: List[List[float]]
    intent_by_cluster: Dict[int, str]
    
    
class JobSubmissionResponse(BaseModel):
    job_id: str

class JobStatusResponse(BaseModel):
    job_id: str 
    status: Literal["PENDING", "STARTED", "SUCCESS", "FAILURE", "RETRY", "REVOKED"] = Field(default="PENDING")
    estimated_wait_time: Optional[int] = None
    result: Optional[ConversationFlowAnalysisResponse] =  Field(default=None)
    error: Optional[str] = None
