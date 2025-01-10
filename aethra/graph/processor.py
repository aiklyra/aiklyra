import networkx as nx
from typing import Callable, Dict, List, Optional

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
        for i, row in enumerate(self.transition_matrix):
            for j, weight in enumerate(row):
                if weight > 0: 
                    graph.add_edge(i, j, weight=weight)
        nx.set_node_attributes(graph, self.intent_by_cluster, "intent")
        return graph

    def filter_graph(self, filter_strategy: Callable[[nx.DiGraph], nx.DiGraph]) -> nx.DiGraph:
        """
        Apply a filter strategy to the graph.

        Args:
            filter_strategy (Callable[[nx.DiGraph], nx.DiGraph]): A function that filters the graph.

        Returns:
            nx.DiGraph: The filtered graph.
        """
        return filter_strategy(self.graph)

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
