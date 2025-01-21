from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class Utterance(BaseModel):
    role: str = Field(default="user")
    content: str = Field(default="")

class ConversationFlowAnalysisRequest(BaseModel):
    conversation_data: Dict[str, List[Utterance]]
    min_clusters: Optional[int] = Field(default=5)
    max_clusters: Optional[int] = Field(default=10)
    top_k_nearest_to_centroid: int = Field(default=10)

class ConversationFlowAnalysisResponse(BaseModel):
    transition_matrix: List[List[float]]
    intent_by_cluster: Dict[int, str]
