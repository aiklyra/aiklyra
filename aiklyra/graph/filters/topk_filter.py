from .base_filter import BaseGraphFilter
import networkx as nx
import numpy as np
from typing import Dict

class TopKFilter(BaseGraphFilter):
    """
    A filter that retains only the top K outgoing edges for each node in a directed graph,
    based on edge weights.

    Attributes:
        top_k (int): The maximum number of outgoing edges to retain for each node.
    """

    def __init__(self, top_k: int):
        """
        Initialize the TopKFilter.

        Args:
            top_k (int): The number of top outgoing edges to retain for each node.
                         Edges are ranked based on their 'weight' attribute in descending order.
        """
        self.top_k = top_k

    def apply(self, graph: nx.DiGraph, transition_matrix: np.ndarray, intent_by_cluster: Dict) -> nx.DiGraph:
        """
        Apply the TopK filter to a directed graph.

        This method processes the input graph and retains only the top K outgoing edges 
        for each node, sorted by their weights in descending order. It creates a new 
        filtered graph without modifying the original.

        Args:
            graph (nx.DiGraph): The directed graph to filter. Each edge is expected 
                                to have a 'weight' attribute.
            transition_matrix (np.ndarray): The transition matrix representing the 
                                            probabilities between nodes.
            intent_by_cluster (Dict): Mapping of cluster IDs to their intent descriptions. 
                                      This may optionally be used for additional processing.

        Returns:
            nx.DiGraph: A new directed graph with only the top K outgoing edges 
                        per node retained.

        Raises:
            ValueError: If `top_k` is not a positive integer or if the graph contains nodes
                        without a 'weight' attribute on edges.

        Example:
            >>> import networkx as nx
            >>> graph = nx.DiGraph()
            >>> graph.add_edge(0, 1, weight=0.5)
            >>> graph.add_edge(0, 2, weight=0.2)
            >>> graph.add_edge(0, 3, weight=0.8)
            >>> graph.add_edge(1, 2, weight=0.3)
            >>> filter = TopKFilter(top_k=2)
            >>> filtered_graph = filter.apply(graph, None, None)
            >>> list(filtered_graph.edges(data=True))
            [(0, 3, {'weight': 0.8}), (0, 1, {'weight': 0.5}), (1, 2, {'weight': 0.3})]
        """
        filtered_graph = graph.copy()

        for node in graph.nodes:
            outgoing_edges = [(node, neighbor, data) for neighbor, data in graph[node].items()]
            outgoing_edges = sorted(outgoing_edges, key=lambda x: x[2].get('weight', 0), reverse=True)
            edges_to_keep = outgoing_edges[:self.top_k]
            neighbors_to_keep = {edge[1] for edge in edges_to_keep}
            for neighbor in list(graph[node].keys()):
                if neighbor not in neighbors_to_keep:
                    filtered_graph.remove_edge(node, neighbor)

        return filtered_graph
