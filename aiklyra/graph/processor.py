import networkx as nx
from typing import Callable, Dict, List, Optional
from aiklyra.graph.filters.base_filter import BaseGraphFilter
from aiklyra.models import JobStatusResponse , ConversationFlowAnalysisResponse
from .graph_visualizers import (
    BaseGraphVisualizer , 
    InteractiveGraphVisualizer , 
    StaticGraphVisualizer , 
    SankeyGraphVisualizer
)
from pyvis.network import Network
import numpy as np 
import os 
class GraphProcessor:
    graph_visualizer = {
        'static_visualizer': StaticGraphVisualizer,
        'interactive_visualizer': InteractiveGraphVisualizer,
        'sankey_visualizer': SankeyGraphVisualizer
    }
    
    def __init__(self, job_status : JobStatusResponse):
        """
        Initialize the GraphProcessor with the analysis response.

        Args:
            job_status (JobStatusResponse): The job status response from the Aiklyra API.
        """
        analysis = job_status.result
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

    def get_visualizer(self, visualizer: str) -> BaseGraphVisualizer:
        """
        Get the specified graph visualizer.

        Args:
            visualizer (str): The visualizer to get. Options: 'static_visualizer', 'interactive_visualizer', 'sankey_visualizer'.

        Returns:
            BaseGraphVisualizer: The visualizer instance.
        """
        return self.graph_visualizer[visualizer]
    def get_graph(self) -> nx.DiGraph:
        """Get the graph."""
        return self.graph