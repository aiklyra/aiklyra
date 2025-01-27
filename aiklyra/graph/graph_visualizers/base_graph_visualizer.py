from abc import ABC , abstractmethod
from typing import Any
from networkx import DiGraph
class BaseGraphVisualizer(ABC):
    """
    An abstract base class for graph visualization.

    This class defines the interface for graph visualization. Subclasses must implement the `visualize` method
    to provide specific visualization functionality for directed graphs (`DiGraph`). The `visualize` method
    is expected to take a graph as input and return a visualization object, which could be a plot, an interactive
    visualization, or any other representation.

    Attributes:
        None

    Methods:
        visualize(graph): Abstract method to visualize the given graph.
    """
    @classmethod
    @abstractmethod
    def visualize( 
        graph : DiGraph
        ) -> Any:
        """
        Visualize the graph using a specified layout.

        Args:
            graph (DiGraph): The graph to visualize.
        Returns:
            Any: The visualization object.
        """
        pass
    