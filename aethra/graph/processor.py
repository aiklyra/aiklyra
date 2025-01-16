import networkx as nx
from typing import Callable, Dict, List, Optional
from aethra.graph.filters.base_filter import BaseGraphFilter
from aethra.models import ConversationFlowAnalysisResponse 
from pyvis.network import Network
import numpy as np 
import os 
class GraphProcessor:
    def __init__(self, analysis: ConversationFlowAnalysisResponse):
        """
        Initialize the GraphProcessor with the analysis response.

        Args:
            analysis (ConversationFlowAnalysisResponse): The response object containing transition matrix 
                                                        and intent-to-cluster mapping.
        """
        self.transition_matrix = analysis.transition_matrix
        self.intent_by_cluster = analysis.intent_by_cluster
        self.graph = self._construct_graph()

    def _construct_graph(self) -> nx.DiGraph:
        """Construct a directed graph from the transition matrix."""
        graph = nx.DiGraph()

        for intent in self.intent_by_cluster.values():
            graph.add_node(intent)

        for i, from_intent in self.intent_by_cluster.items():
            weights = self.transition_matrix[int(i)]
            for j, weight in enumerate(weights):
                to_intent = self.intent_by_cluster[int(j)]
                graph.add_edge(from_intent, to_intent, weight=weight)
        return graph

    def filter_graph(self, filter_strategy: BaseGraphFilter) -> nx.DiGraph:
        """
        Apply a filter strategy to the graph.

        Args:
            filter_strategy (BaseGraphFilter): A GraphFilter instance of a class inheriting from BaseGraphFilter.

        Returns:
            nx.DiGraph: The filtered graph.
        """
        transition_matrix_array = np.array(self.transition_matrix) if not isinstance(self.transition_matrix, np.ndarray) else self.transition_matrix

        new_graph = filter_strategy.apply(self.graph, transition_matrix_array, self.intent_by_cluster)
        self.intent_by_cluster , self.transition_matrix = self.extract_intent_and_matrix_from_graph(new_graph)
        self.graph = new_graph 
        return self.graph 

    def extract_intent_and_matrix_from_graph(self , graph: nx.DiGraph):
        """
        Given a filtered DiGraph, extract:
        - a new intent_by_cluster dict
        - a new transition matrix

        Returns:
            new_intent_by_cluster (dict): Maps new index -> intent (node).
            new_transition_matrix (np.ndarray): 2D matrix of edge weights.
        """
        nodes = list(graph.nodes())

        node_to_index = {node: idx for idx, node in enumerate(nodes)}

        intent_by_cluster = {idx: node for idx, node in enumerate(nodes)}

        size = len(nodes)
        transition_matrix = np.zeros((size, size), dtype=float)

        for u, v, data in graph.edges(data=True):
            i = node_to_index[u]
            j = node_to_index[v]
            weight = data.get("weight", 0.0)
            transition_matrix[i, j] = weight

        return intent_by_cluster, transition_matrix 

    def plot_graph_html(G: nx.DiGraph, file_name: str) -> None:
        """
        Generates an HTML visualization of the directed graph using PyVis and saves it to a file.

        Args:
            G (nx.DiGraph): The directed graph to be visualized.
            file_name (str): Name of the output HTML file (without extension).
        """
        net = Network(notebook=False, width="100%", height="700px", directed=True, cdn_resources="in_line")

        # Add nodes and edges from NetworkX graph to PyVis network
        for node in G.nodes:
            net.add_node(node, label=str(node), title=str(node))

        # Find the minimum and maximum weights
        min_weight = float('inf')
        max_weight = float('-inf')
        for u, v, data in G.edges(data=True):
            weight = data.get('weight', 1)
            min_weight = min(min_weight, weight)
            max_weight = max(max_weight, weight)

        # Normalize the weight to a 0-1 scale and map to color
        def get_edge_color(weight: float) -> str:
            normalized_weight = (weight - min_weight) / (max_weight - min_weight) if max_weight > min_weight else 0
            color = f'rgb({int(255 * normalized_weight)}, 0, {int(255 * (1 - normalized_weight))})'
            return color

        for u, v, data in G.edges(data=True):
            weight = data.get('weight', 1)
            color = get_edge_color(weight)
            net.add_edge(u, v, value=weight, title=f'weight: {weight:.2f}', color=color)

        # Set options for better visualization and enable the physics control panel
        net.set_options("""
        var options = {
            "nodes": {
                "font": {
                    "size": 20
                }
            },
            "edges": {
                "arrows": {
                    "to": {
                        "enabled": true,
                        "scaleFactor": 1
                    }
                },
                "font": {
                    "size": 14,
                    "align": "horizontal"
                },
                "smooth": {
                    "enabled": true,
                    "type": "dynamic"
                }
            },
            "physics": {
                "enabled": true,
                "solver": "forceAtlas2Based",
                "forceAtlas2Based": {
                    "theta": 0.5,
                    "gravitationalConstant": -86,
                    "centralGravity": 0.005,
                    "springLength": 120,
                    "springConstant": 0.04,
                    "damping": 0.57,
                    "avoidOverlap": 0.92
                },
                "maxVelocity": 41,
                "minVelocity": 1,
                "timestep": 0.5,
                "wind": {
                    "x": 0,
                    "y": 0
                }
            },
            "configure": {
                "enabled": true,
                "filter": "nodes,edges,physics",
                "showButton": true
            }
        }
        """)

        # Generate the graph and save it to an HTML file
        if not os.path.exists("output"):
            os.mkdir("output")
        net.show(os.path.join("output" , f"{file_name}.json"))

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
