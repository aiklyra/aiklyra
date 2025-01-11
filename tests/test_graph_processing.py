import unittest
import networkx as nx
import numpy as np
from aethra import GraphProcessor , FRFilter , ThresholdFilter


class TestGraphProcessingAndFiltering(unittest.TestCase):

    def setUp(self):
        """
        Set up test data and graphs for testing.
        """
        # Create a sample directed graph
        self.graph = nx.DiGraph()
        self.graph.add_edge("Node A", "Node B", weight=0.5)
        self.graph.add_edge("Node A", "Node C", weight=0.2)
        self.graph.add_edge("Node B", "Node C", weight=0.8)
        self.graph.add_edge("Node C", "Node A", weight=0.1)  # Weak cycle edge

        # Create a sample transition matrix and intent mapping
        self.transition_matrix = np.array([
            [0.0, 0.5, 0.2],
            [0.0, 0.0, 0.8],
            [0.1, 0.0, 0.0]
        ])
        self.intent_by_cluster = {
            "0": "Node A",
            "1": "Node B",
            "2": "Node C"
        }

    def test_threshold_filter(self):
        """
        Test the ThresholdFilter to ensure it removes edges below the threshold.
        """
        # Apply a threshold filter
        threshold_filter = ThresholdFilter(threshold=0.3)
        filtered_graph = threshold_filter.apply(self.graph)

        # Check edges in the filtered graph
        expected_edges = [("Node A", "Node B", {"weight": 0.5}),
                          ("Node B", "Node C", {"weight": 0.8})]
        self.assertEqual(list(filtered_graph.edges(data=True)), expected_edges)

    def test_fr_filter(self):
        """
        Test the FRFilter for filtering, cycle removal, and subgraph reconnection.
        """
        # Apply the FRFilter
        fr_filter = FRFilter(min_weight=0.3, top_k=2)
        processed_graph = fr_filter.apply(self.graph, self.transition_matrix, self.intent_by_cluster)

        # Validate that cycles are removed
        self.assertFalse(list(nx.simple_cycles(processed_graph)), "Graph contains cycles after filtering.")

        # Validate that subgraphs are reconnected
        subgraphs = list(nx.weakly_connected_components(processed_graph))
        self.assertEqual(len(subgraphs), 1, "Graph contains disconnected subgraphs after reconnection.")

    def test_combined_filters(self):
        """
        Test a pipeline of multiple filters applied sequentially.
        """
        # Step 1: Apply ThresholdFilter
        threshold_filter = ThresholdFilter(threshold=0.3)
        filtered_graph = threshold_filter.apply(self.graph)

        # Step 2: Apply FRFilter
        fr_filter = FRFilter(min_weight=0.3, top_k=2)
        final_graph = fr_filter.apply(filtered_graph, self.transition_matrix, self.intent_by_cluster)

        # Validate that cycles are removed
        self.assertFalse(list(nx.simple_cycles(final_graph)), "Graph contains cycles after filtering.")

        # Validate the number of edges and structure
        expected_edges = set([
            ("Node A", "Node B"),
            ("Node B", "Node C")
        ])
        actual_edges = set((u, v) for u, v, _ in final_graph.edges(data=True))
        self.assertEqual(expected_edges, actual_edges)

    def test_edge_case_empty_graph(self):
        """
        Test the filters with an empty graph to ensure graceful handling.
        """
        empty_graph = nx.DiGraph()

        # Apply ThresholdFilter
        threshold_filter = ThresholdFilter(threshold=1)
        filtered_graph = threshold_filter.apply(empty_graph)

        # Validate the result is still an empty graph
        self.assertTrue(filtered_graph.number_of_nodes() == 0 and filtered_graph.number_of_edges() == 0)

        # Apply FRFilter
        fr_filter = FRFilter(min_weight=1, top_k=2)
        processed_graph = fr_filter.apply(empty_graph, self.transition_matrix, self.intent_by_cluster)

        # Validate the result is still an empty graph
        self.assertTrue(processed_graph.number_of_nodes() == 0 and processed_graph.number_of_edges() == 0)


if __name__ == "__main__":
    unittest.main()
