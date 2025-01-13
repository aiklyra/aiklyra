from .base_filter import BaseGraphFilter
import networkx as nx
import numpy as np
from typing import Dict


class FRFilter(BaseGraphFilter):
    """
    A filter that performs edge filtering based on weight, removes cycles, 
    and reconnects disconnected subgraphs using the transition matrix.

    Attributes:
        min_weight (float): Minimum weight threshold for keeping edges.
        top_k (int): Number of top edges to keep for each node.
    """

    def __init__(self, min_weight: float = 0.0, top_k: int = 5):
        """
        Initialize the FRFilter.

        Args:
            min_weight (float): Minimum weight threshold for keeping edges. Defaults to 0.0.
            top_k (int): Number of top edges to keep for each node. Defaults to 5.
        """
        self.min_weight = min_weight
        self.top_k = top_k

    def apply(self, graph: nx.DiGraph, transition_matrix: np.ndarray, intent_by_cluster: Dict[str, str]) -> nx.DiGraph:
        """
        Apply the filter and reconnect logic to a graph.

        This method processes a directed graph to achieve the following:
            1. Filters edges based on a minimum weight threshold.
            2. Keeps only the top-k edges for each node based on edge weights.
            3. Detects and resolves cycles by removing the weakest edge in each cycle.
            4. Reconnects disconnected subgraphs to ensure that all components are part of a single connected graph.

        Args:
            graph (nx.DiGraph): 
                The directed graph to process. This graph should represent relationships
                between intents, where each edge has a 'weight' attribute indicating the 
                strength of the connection.

            transition_matrix (np.ndarray): 
                A 2D array representing transition probabilities or weights between clusters.
                The value at position [i][j] indicates the weight of transitioning from 
                cluster i to cluster j.

            intent_by_cluster (Dict[str, str]): 
                A dictionary mapping cluster indices (as strings) to their corresponding 
                intents (descriptions). For example:
                    {"0": "Intent A", "1": "Intent B", ...}

        Returns:
            nx.DiGraph: 
                The processed directed graph with the following modifications:
                    - Edges with weights below the minimum threshold are removed.
                    - Each node retains only its top-k strongest outgoing edges.
                    - Cycles are resolved by removing the weakest edge in each cycle.
                    - Detached subgraphs are reconnected to the main graph based on the
                    strongest available transition weight in the transition matrix.

        Process:
            1. Filtering:
                - All edges with weights below the specified `min_weight` are removed.
            
            2. Top-K Retention:
                - For each node, only the top-k outgoing edges (based on weight) are kept,
                ensuring the graph remains manageable and meaningful.

            3. Cycle Resolution:
                - Simple cycles in the graph are detected.
                - The weakest edge in each cycle is removed to eliminate the cycle while 
                minimizing the impact on graph connectivity.

            4. Reconnection:
                - Small, detached subgraphs are identified.
                - Each subgraph is reconnected to the main graph by finding the strongest
                transition (based on the transition matrix) between nodes in the subgraph 
                and nodes in the main graph.

        Example:
            >>> graph = nx.DiGraph()
            >>> graph.add_edge("Intent A", "Intent B", weight=0.5)
            >>> graph.add_edge("Intent A", "Intent C", weight=0.2)
            >>> graph.add_edge("Intent B", "Intent C", weight=0.8)
            >>> transition_matrix = np.array([[0.0, 0.5, 0.2],
                                            [0.0, 0.0, 0.8],
                                            [0.0, 0.0, 0.0]])
            >>> intent_by_cluster = {"0": "Intent A", "1": "Intent B", "2": "Intent C"}
            >>> filter = FRFilter(min_weight=0.3, top_k=1)
            >>> processed_graph = filter.apply(graph, transition_matrix, intent_by_cluster)
            >>> list(processed_graph.edges(data=True))
            [('Intent A', 'Intent B', {'weight': 0.5}),
            ('Intent B', 'Intent C', {'weight': 0.8})]
        """
        # Add edges with weights above the minimum threshold
        filtered_graph = nx.DiGraph()
        for i, from_intent in intent_by_cluster.items():
            weights = transition_matrix[int(i)]
            for j, weight in enumerate(weights):
                if weight >= self.min_weight and int(i) != int(j):
                    to_intent = intent_by_cluster[str(j)]
                    filtered_graph.add_edge(from_intent, to_intent, weight=weight)

        # Keep only the top-k edges for each node
        incoming_edges = {}
        for u, v, data in filtered_graph.edges(data=True):
            if v not in incoming_edges:
                incoming_edges[v] = []
            incoming_edges[v].append((u, data['weight']))

        for v, edges in incoming_edges.items():
            edges.sort(key=lambda x: x[1], reverse=True)
            top_edges = edges[:self.top_k]
            filtered_graph.remove_edges_from([(u, v) for u, _ in edges])
            for u, weight in top_edges:
                filtered_graph.add_edge(u, v, weight=weight)

        # Remove weakest edges in cycles
        filtered_graph = self._remove_weakest_edge_in_cycles(filtered_graph)

        # Reconnect subgraphs
        filtered_graph = self._reconnect_subgraphs(filtered_graph, transition_matrix, intent_by_cluster)

        return filtered_graph

    def _remove_weakest_edge_in_cycles(self , G: nx.DiGraph) -> nx.DiGraph:
        """
        Detect and remove the weakest edge in cycles within a graph.

        Args:
            G (nx.DiGraph): The graph to process.

        Returns:
            nx.DiGraph: The graph with cycles resolved.
        """
        try:
            cycles = list(nx.simple_cycles(G))
        except nx.NetworkXNoCycle:
            cycles = []

        while cycles:
            for cycle in cycles:
                edges_in_cycle = [(cycle[i], cycle[(i + 1) % len(cycle)]) for i in range(len(cycle))]
                valid_edges = [edge for edge in edges_in_cycle if G.has_edge(*edge)]

                if valid_edges:
                    weakest_edge = min(valid_edges, key=lambda edge: G.edges[edge]['weight'])
                    G.remove_edge(*weakest_edge)
            try:
                cycles = list(nx.simple_cycles(G))
            except nx.NetworkXNoCycle:
                cycles = []

        return G

    def _reconnect_subgraphs(
        self , 
        G: nx.DiGraph, 
        transition_matrix: np.ndarray, 
        intent_by_cluster: Dict[str, str]
    ) -> nx.DiGraph:
        """
        Reconnect small subgraphs to the main graph using the transition matrix.

        Args:
            G (nx.DiGraph): The graph to process.
            transition_matrix (np.ndarray): Matrix representing transition weights between clusters.
            intent_by_cluster (Dict[str, str]): Dictionary mapping cluster indices to their intents.

        Returns:
            nx.DiGraph: The reconnected graph.
        """
        subgraphs = list(nx.weakly_connected_components(G))

        if len(subgraphs) <= 1:
            return G

        main_subgraph = max(subgraphs, key=len)

        for subgraph in subgraphs:
            if subgraph == main_subgraph:
                continue

            max_weight = -np.inf
            best_edge = None

            for node in subgraph:
                for main_node in main_subgraph:
                    node_idx = list(intent_by_cluster.keys())[list(intent_by_cluster.values()).index(node)]
                    main_node_idx = list(intent_by_cluster.keys())[list(intent_by_cluster.values()).index(main_node)]

                    weight = transition_matrix[int(node_idx), int(main_node_idx)]

                    if weight > max_weight:
                        max_weight = weight
                        best_edge = (node, main_node)

            if best_edge:
                G.add_edge(*best_edge, weight=max_weight)

        return G
