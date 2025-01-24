from .base_graph_visualizer import BaseGraphVisualizer
from networkx import DiGraph
import matplotlib.pyplot as plt
from typing import Any , Tuple , Optional
import networkx as nx
from networkx import spring_layout , circular_layout , shell_layout , random_layout

class StaticGraphVisualizer(BaseGraphVisualizer):
    layout = {
        'spring': spring_layout,
        'circular': circular_layout,
        'shell': shell_layout,
        'random': random_layout,
    }
    def visualize(
        graph : DiGraph ,
        layout: str = 'spring', 
        save_path: Optional[str] = None , 
        figsize : Tuple[int] = (30, 40) , 
        with_labels : bool = True , 
        node_color : str = 'lightblue' ,
        edge_color : str = 'gray' , 
        edge_attribute : str = 'weight'
    ) :
        """
        Visualize the graph using a specified layout.

        Args:
            graph (DiGraph): The graph to visualize.
            layout (str): The layout to use for visualization. Options: 'spring', 'circular', 'shell', 'random'.
            save_path (Optional[str]): Path to save the visualization as an image. If None, just show the plot.
            figsize (Tuple[int]): The size of the figure (width, height) Defaults to (30 , 40).
            with_labels (bool): Whether to display node labels.
            node_color (str): The color of the nodes.
            edge_color (str): The color of the edges.
            edge_attribute (str): The edge attributes to display.
        """
        pos = StaticGraphVisualizer.layout[layout](graph)
        plt.figure(figsize=figsize)
        nx.draw(graph, pos, with_labels=with_labels, node_color=node_color, edge_color=edge_color)
        labels = nx.get_edge_attributes(graph, edge_attribute)
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
        
        if save_path:
            plt.savefig(save_path)
        plt.show()

