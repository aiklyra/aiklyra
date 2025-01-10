from abc import ABC, abstractmethod
import networkx as nx 

class BaseGraphFilter(ABC):
    @abstractmethod
    def apply(self, graph: nx.DiGraph) -> nx.DiGraph:
        """Apply the filter to a graph."""
        pass
