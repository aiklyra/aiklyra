import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network
from typing import Optional

class GraphVisualizer:
    def __init__(self, graph: nx.DiGraph):
        """
        Initialize the GraphVisualizer with the given graph.

        Args:
            graph (nx.DiGraph): A directed graph to visualize.
        """
        self.graph = graph

    def visualize(self, layout: str = 'spring', save_path: Optional[str] = None):
        """
        Visualize the graph using a specified layout.

        Args:
            layout (str): The layout to use for visualization. Options: 'spring', 'circular', 'shell', 'random'.
            save_path (Optional[str]): Path to save the visualization as an image. If None, just show the plot.
        """
        pos = self._get_layout(layout)
        plt.figure(figsize=(10, 8))
        nx.draw(self.graph, pos, with_labels=True, node_color='lightblue', edge_color='gray')
        labels = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=labels)
        
        if save_path:
            plt.savefig(save_path)
        plt.show()

    def _get_layout(self, layout: str):
        """
        Get the layout for the graph visualization.

        Args:
            layout (str): The layout to use. Options: 'spring', 'circular', 'shell', 'random'.

        Returns:
            dict: Node positions for the layout.
        """
        if layout == 'spring':
            return nx.spring_layout(self.graph)
        elif layout == 'circular':
            return nx.circular_layout(self.graph)
        elif layout == 'shell':
            return nx.shell_layout(self.graph)
        elif layout == 'random':
            return nx.random_layout(self.graph)
        else:
            raise ValueError(f"Unsupported layout: {layout}")

    def visualize_interactive(self, save_path: Optional[str] = None):
        """
        Create an interactive graph visualization using PyVis.

        Args:
            save_path (Optional[str]): Path to save the HTML visualization. If None, display the graph in the browser.
        """
        net = Network(notebook=False, width="100%", height="700px", directed=True, cdn_resources="in_line")

        for node in self.graph.nodes:
            net.add_node(node, label=str(node), title=str(node))

        min_weight = float('inf')
        max_weight = float('-inf')
        for u, v, data in self.graph.edges(data=True):
            weight = data.get('weight', 1)
            min_weight = min(min_weight, weight)
            max_weight = max(max_weight, weight)

        def get_edge_color(weight: float) -> str:
            normalized_weight = (weight - min_weight) / (max_weight - min_weight) if max_weight > min_weight else 0
            return f'rgb({int(255 * normalized_weight)}, 0, {int(255 * (1 - normalized_weight))})'

        for u, v, data in self.graph.edges(data=True):
            weight = data.get('weight', 1)
            color = get_edge_color(weight)
            net.add_edge(u, v, value=weight, title=f'Weight: {weight:.2f}', color=color)

        net.set_options("""
        var options = {
            "nodes": {"font": {"size": 20}},
            "edges": {"arrows": {"to": {"enabled": true, "scaleFactor": 1}}},
            "physics": {"enabled": true, "solver": "forceAtlas2Based"}
        }
        """)

        if save_path:
            net.show(save_path)
        else:
            net.show("graph.html")
