import pytest
import networkx as nx
import numpy as np
from aethra import GraphProcessor, FRFilter, ThresholdFilter


@pytest.fixture
def setup_data():
    """
    Fixture to set up test data and graphs for testing.
    """
    graph = nx.DiGraph()
    graph.add_edge("Node A", "Node B", weight=0.5)
    graph.add_edge("Node A", "Node C", weight=0.2)
    graph.add_edge("Node B", "Node C", weight=0.8)
    graph.add_edge("Node C", "Node A", weight=0.1)  # Weak cycle edge

    transition_matrix = np.array([
        [0.0, 0.5, 0.2],
        [0.0, 0.0, 0.8],
        [0.1, 0.0, 0.0]
    ])
    intent_by_cluster = {
        0: "Node A",
        1: "Node B",
        2: "Node C"
    }

    return graph, transition_matrix, intent_by_cluster


def test_threshold_filter(setup_data):
    """
    Test the ThresholdFilter to ensure it removes edges below the threshold.
    """
    graph, transition_matrix, intent_by_cluster = setup_data

    # Apply a threshold filter
    threshold_filter = ThresholdFilter(threshold=0.3)
    filtered_graph = threshold_filter.apply(graph, transition_matrix, intent_by_cluster)

    # Check edges in the filtered graph
    expected_edges = [("Node A", "Node B", {"weight": 0.5}),
                      ("Node B", "Node C", {"weight": 0.8})]
    assert list(filtered_graph.edges(data=True)) == expected_edges


def test_fr_filter(setup_data):
    """
    Test the FRFilter for filtering, cycle removal, and subgraph reconnection.
    """
    graph, transition_matrix, intent_by_cluster = setup_data

    # Apply the FRFilter
    fr_filter = FRFilter(min_weight=0.3, top_k=2)
    processed_graph = fr_filter.apply(graph, transition_matrix, intent_by_cluster)

    # Validate that cycles are removed
    assert not list(nx.simple_cycles(processed_graph)), "Graph contains cycles after filtering."

    # Validate that subgraphs are reconnected
    subgraphs = list(nx.weakly_connected_components(processed_graph))
    assert len(subgraphs) == 1, "Graph contains disconnected subgraphs after reconnection."


def test_combined_filters(setup_data):
    """
    Test a pipeline of multiple filters applied sequentially.
    """
    graph, transition_matrix, intent_by_cluster = setup_data

    # Step 1: Apply ThresholdFilter
    threshold_filter = ThresholdFilter(threshold=0.3)
    filtered_graph = threshold_filter.apply(graph, transition_matrix, intent_by_cluster)

    # Step 2: Apply FRFilter
    fr_filter = FRFilter(min_weight=0.3, top_k=2)
    final_graph = fr_filter.apply(filtered_graph, transition_matrix, intent_by_cluster)

    # Validate that cycles are removed
    assert not list(nx.simple_cycles(final_graph)), "Graph contains cycles after filtering."

    # Validate the number of edges and structure
    expected_edges = set([
        ("Node A", "Node B"),
        ("Node B", "Node C")
    ])
    actual_edges = set((u, v) for u, v, _ in final_graph.edges(data=True))
    assert expected_edges == actual_edges


def test_edge_case_empty_graph():
    """
    Test the filters with an empty graph to ensure graceful handling.
    """
    empty_graph = nx.DiGraph()
    transition_matrix = np.array([])
    intent_by_cluster = {}

    # Apply ThresholdFilter
    threshold_filter = ThresholdFilter(threshold=1)
    filtered_graph = threshold_filter.apply(empty_graph, transition_matrix, intent_by_cluster)

    # Validate the result is still an empty graph
    assert filtered_graph.number_of_nodes() == 0
    assert filtered_graph.number_of_edges() == 0

    # Apply FRFilter
    fr_filter = FRFilter(min_weight=1, top_k=2)
    processed_graph = fr_filter.apply(empty_graph, transition_matrix, intent_by_cluster)

    # Validate the result is still an empty graph
    assert processed_graph.number_of_nodes() == 0
    assert processed_graph.number_of_edges() == 0
