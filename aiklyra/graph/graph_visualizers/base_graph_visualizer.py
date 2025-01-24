from abc import ABC , abstractmethod
from typing import Any
from networkx import DiGraph
class BaseGraphVisualizer(ABC):
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
    