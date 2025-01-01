from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class Utterance(BaseModel):
    role: str = Field(default="user")
    content: str = Field(default="")

class ConversationFlowAnalysisRequest(BaseModel):
    conversation_data: Dict[str, List[Utterance]]
    min_clusters: Optional[int] = Field(default=5)
    max_clusters: Optional[int] = Field(default=10)
    embedding_model: str = Field(default="text-embedding-ada-002")
    top_k_nearest_to_centroid: int = Field(default=10)
    tau: float = Field(default=0.1)

class ConversationFlowAnalysisResponse(BaseModel):
    transition_matrix: List[List[float]]
    intent_by_cluster: Dict[int, str]
