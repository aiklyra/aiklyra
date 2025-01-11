from .base_filter import BaseGraphFilter
import networkx as nx
import numpy as np
from typing import Dict

class ThresholdFilter(BaseGraphFilter):
    """
    A filter that removes edges from a graph whose weights are below a specified threshold.

    Attributes:
        threshold (float): The minimum weight an edge must have to remain in the graph.
    """

    def __init__(self, threshold: float):
        """
        Initialize the ThresholdFilter.

        Args:
            threshold (float): The minimum weight threshold for edges (0 < threshold <= 1). 
                               Edges with weights below this value will be removed.

        Raises:
            ValueError: If the threshold is not within the range (0, 1].
        """
        if threshold <= 0 or threshold > 1:
            raise ValueError("Threshold must be a value in the range (0, 1].")
        self.threshold = threshold

    def apply(
        self, graph: nx.DiGraph, transition_matrix: np.ndarray, intent_by_cluster: Dict
    ) -> nx.DiGraph:
        """
        Apply the threshold filter to a directed graph.

        This method processes a directed graph by filtering out edges whose weights
        fall below the specified threshold. The filtering operation is non-destructive,
        meaning the input graph remains unchanged, and a new filtered graph is returned.

        Args:
            graph (nx.DiGraph): 
                The directed graph to filter. Each edge in the graph is expected to have a
                'weight' attribute. The 'weight' attribute represents the strength or importance
                of the connection between two nodes.
            transition_matrix (np.ndarray):
                The transition matrix associated with the graph. This may be used for
                additional processing, but it is not modified by this filter.
            intent_by_cluster (Dict):
                A mapping of cluster IDs to their respective intents or descriptions. This
                may also be used for additional context but is not modified in this filter.

        Returns:
            nx.DiGraph: 
                A new directed graph with the following modifications:
                    - All edges with weights below the specified threshold are removed.
                    - The structure and properties of the input graph are otherwise preserved.

        Raises:
            KeyError: If an edge in the graph does not have a 'weight' attribute.

        Example:
            >>> import networkx as nx
            >>> graph = nx.DiGraph()
            >>> graph.add_edge("Node A", "Node B", weight=0.5)
            >>> graph.add_edge("Node A", "Node C", weight=0.2)
            >>> graph.add_edge("Node B", "Node C", weight=0.8)
            >>> threshold_filter = ThresholdFilter(threshold=0.3)
            >>> filtered_graph = threshold_filter.apply(graph, None, None)
            >>> list(filtered_graph.edges(data=True))
            [('Node A', 'Node B', {'weight': 0.5}), ('Node B', 'Node C', {'weight': 0.8})]

        Notes:
            - The threshold value is determined when the `ThresholdFilter` object is initialized.
            - If no edges meet the threshold criteria, the resulting graph may contain nodes but no edges.
            - The method assumes that all edges in the graph have a 'weight' attribute. If the attribute
              is missing, an exception may be raised.

        Limitations:
            - This method does not modify the nodes or their attributes.
            - The filtering process only considers the 'weight' attribute. Additional criteria
              for filtering would require extending this class or method.
        """
        filtered_graph = graph

        for u, v, data in list(filtered_graph.edges(data=True)):
            if data["weight"] < self.threshold:
                filtered_graph.remove_edge(u, v)

        return filtered_graph
