from .base_filter import BaseGraphFilter
import networkx as nx

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
            threshold (float): The minimum weight threshold for edges (0<threshold<1). 
                               Edges with weights below this value will be removed.
        """
        self.threshold = threshold

    def apply(self, graph: nx.DiGraph) -> nx.DiGraph:
        """
        Apply the threshold filter to a directed graph.

        This method creates a copy of the input graph and removes any edges whose
        weights are below the specified threshold.

        Args:
            graph (nx.DiGraph): The directed graph to filter. Each edge in the graph 
                                is expected to have a 'weight' attribute.

        Returns:
            nx.DiGraph: A new graph with edges below the threshold removed.
        """
        filtered_graph = graph.copy()
        for u, v, data in list(filtered_graph.edges(data=True)):
            if data['weight'] < self.threshold:
                filtered_graph.remove_edge(u, v)
        return filtered_graph
