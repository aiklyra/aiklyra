from .base_filter import BaseGraphFilter
import networkx as nx

class TopKFilter(BaseGraphFilter):
    """
    A filter that keeps only the top K edges for each node in a directed graph,
    based on edge weights.

    Attributes:
        top_k (int): The maximum number of outgoing edges to keep for each node.
    """

    def __init__(self, top_k: int):
        """
        Initialize the TopKFilter.

        Args:
            top_k (int): The number of top edges to retain for each node, 
                         based on their weights.
        """
        self.top_k = top_k

    def apply(self, graph: nx.DiGraph) -> nx.DiGraph:
        """
        Apply the TopK filter to a directed graph.

        This method creates a copy of the input graph and retains only the top K
        outgoing edges for each node, based on edge weights.

        Args:
            graph (nx.DiGraph): The directed graph to filter. Each edge in the graph
                                is expected to have a 'weight' attribute.

        Returns:
            nx.DiGraph: A new graph with only the top K edges per node retained.

        Example:
            >>> import networkx as nx
            >>> graph = nx.DiGraph()
            >>> graph.add_edge(0, 1, weight=0.5)
            >>> graph.add_edge(0, 2, weight=0.2)
            >>> graph.add_edge(0, 3, weight=0.8)
            >>> graph.add_edge(1, 2, weight=0.3)
            >>> filter = TopKFilter(top_k=2)
            >>> filtered_graph = filter.apply(graph)
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
