import networkx as nx
from typing import Callable, Dict, List, Optional
from filters import BaseGraphFilter
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

        return filter_strategy.apply(self.graph, transition_matrix_array, self.intent_by_cluster)

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
