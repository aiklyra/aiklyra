from abc import ABC, abstractmethod
import networkx as nx
import numpy as np
from typing import Dict

class BaseGraphFilter(ABC):
    """
    Abstract base class for graph filters.

    This class provides a blueprint for creating filters that can be applied to 
    directed graphs (`nx.DiGraph`) to modify their structure or properties based 
    on custom filtering logic. Subclasses must implement the `apply` method.

    Attributes:
        None: This base class does not define attributes but specifies the structure
              that subclasses must adhere to.
    """

    @abstractmethod
    def apply(
        self,
        G: nx.DiGraph,
        transition_matrix: np.ndarray,
        intent_by_cluster: Dict[str, str]
    ) -> nx.DiGraph:
        """
        Abstract method to apply a filter to a graph.

        Subclasses must implement this method to define the specific filtering logic. 
        The method takes a directed graph and additional supporting data to process 
        and return a new filtered graph. The filtering operation should not modify 
        the original input graph but instead return a modified copy.

        Args:
            G (nx.DiGraph): 
                The directed graph to filter. The graph is expected to have edges with 
                attributes like 'weight' or other relevant metadata required for filtering.
            transition_matrix (np.ndarray): 
                A transition matrix representing probabilities or relationships between nodes. 
                This may be used in the filtering process to guide decisions.
            intent_by_cluster (Dict[str, str]): 
                A mapping of cluster IDs to intent descriptions. This dictionary provides 
                additional semantic context about the nodes or edges in the graph.

        Returns:
            nx.DiGraph: 
                A new directed graph that has been processed according to the filtering 
                logic defined in the subclass. The structure and attributes of the graph 
                will depend on the specific implementation.

        Raises:
            NotImplementedError: 
                This method must be implemented by subclasses. Calling it directly on 
                `BaseGraphFilter` will result in a `NotImplementedError`.

        Example:
            The `apply` method must be overridden in a subclass. Here's an example implementation 
            in a concrete subclass:

            >>> class ThresholdFilter(BaseGraphFilter):
            >>>     def __init__(self, threshold):
            >>>         self.threshold = threshold
            >>> 
            >>>     def apply(self, G, transition_matrix, intent_by_cluster):
            >>>         filtered_graph = G.copy()
            >>>         for u, v, data in G.edges(data=True):
            >>>             if data['weight'] < self.threshold:
            >>>                 filtered_graph.remove_edge(u, v)
            >>>         return filtered_graph

        Notes:
            - Subclasses are free to interpret and use the `transition_matrix` and `intent_by_cluster` 
              as needed for their filtering logic.
            - The filtering process is non-destructive; the original graph is not modified.
        """
        pass
