from abc import ABC , abstractmethod
from typing import Any
from networkx import DiGraph
class BaseGraphVisualizer(ABC):
    @classmethod
    @abstractmethod
    def visualize( 
        graph : DiGraph, 
        *args , 
        **kwargs) -> Any:
        """
        Visualize the graph using a specified layout.

        Args:
            graph (DiGraph): The graph to visualize.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Any: The visualization object.
        """
        pass
    