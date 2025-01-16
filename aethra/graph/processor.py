import networkx as nx
from typing import Callable, Dict, List, Optional
from aethra.graph.filters.base_filter import BaseGraphFilter
import numpy as np 
class GraphProcessor:
    def __init__(self, transition_matrix: List[List[float]], intent_by_cluster: Dict[int, str]):
        """
        Initialize the GraphProcessor with the transition matrix and intent-to-cluster mapping.

        Args:
            transition_matrix (List[List[float]]): The transition matrix from the API.
            intent_by_cluster (Dict[int, str]): Mapping of intent cluster IDs to descriptions.
        """
        self.transition_matrix = transition_matrix
        self.intent_by_cluster = intent_by_cluster
        self.graph = self._construct_graph()

    def _construct_graph(self) -> nx.DiGraph:
        """Construct a directed graph from the transition matrix."""
        graph = nx.DiGraph()

        for intent in self.intent_by_cluster.values():
            graph.add_node(intent)

        for i, from_intent in self.intent_by_cluster.items():
            weights = self.transition_matrix[int(i)]
            for j, weight in enumerate(weights):
                to_intent = self.intent_by_cluster[int(j)]
                graph.add_edge(from_intent, to_intent, weight=weight)
        return graph

    def filter_graph(self, filter_strategy: BaseGraphFilter) -> nx.DiGraph:
        """
        Apply a filter strategy to the graph.

        Args:
            filter_strategy (BaseGraphFilter): A GraphFilter instance of a class inheriting from BaseGraphFilter.

        Returns:
            nx.DiGraph: The filtered graph.
        """
        transition_matrix_array = np.array(self.transition_matrix) if not isinstance(self.transition_matrix, np.ndarray) else self.transition_matrix

        new_graph = filter_strategy.apply(self.graph, transition_matrix_array, self.intent_by_cluster)
        self.intent_by_cluster , self.transition_matrix = GraphProcessor.extract_intent_and_matrix_from_graph(new_graph)
        self.graph = new_graph 
        return self.graph 
    @classmethod
    def extract_intent_and_matrix_from_graph(graph: nx.DiGraph):
        """
        Given a filtered DiGraph, extract:
        - a new intent_by_cluster dict
        - a new transition matrix

        Returns:
            new_intent_by_cluster (dict): Maps new index -> intent (node).
            new_transition_matrix (np.ndarray): 2D matrix of edge weights.
        """
        nodes = list(graph.nodes())

        node_to_index = {node: idx for idx, node in enumerate(nodes)}

        intent_by_cluster = {idx: node for idx, node in enumerate(nodes)}

        size = len(nodes)
        transition_matrix = np.zeros((size, size), dtype=float)

        for u, v, data in graph.edges(data=True):
            i = node_to_index[u]
            j = node_to_index[v]
            weight = data.get("weight", 0.0)
            transition_matrix[i, j] = weight

        return intent_by_cluster, transition_matrix 

    def visualize_graph(self, graph: Optional[nx.DiGraph] = None) -> None:
        """
        Visualize the graph using a simple layout.

        Args:
            graph (Optional[nx.DiGraph]): The graph to visualize. Defaults to the full graph.
        """
        if graph is None:
            graph = self.graph
        pos = nx.spring_layout(graph)
        nx.draw(graph, pos, with_labels=True, node_color='lightblue', edge_color='gray')
        labels = nx.get_edge_attributes(graph, 'weight')
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
