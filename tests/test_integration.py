import pytest
import json
from unittest.mock import patch, MagicMock
import numpy as np
from difflib import SequenceMatcher
from aethra import AethraClient, GraphProcessor, FRFilter


@pytest.fixture
def mock_conversation_data():
    """
    Fixture to provide mock conversation data for testing.
    """
    return {
        "session_1": [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there!"},
        ],
        "session_2": [
            {"role": "user", "content": "How are you?"},
            {"role": "assistant", "content": "I'm doing great!"},
        ],
    }


@pytest.fixture
def mock_analysis_response():
    """
    Fixture to provide a mock analysis response with stochastic results.
    """
    return {
        "transition_matrix": [
            [0.5, 0.5],
            [0.0, 0.0]
        ],
        "intent_by_cluster": {
            "0": "Greeting and establishing rapport",
            "1": "Response to Greeting"
        }
    }


def assert_intent_similarity(expected_intents, actual_intents, threshold=0.8):
    """
    Assert that the intents in the response are similar to a certain degree.

    Args:
        expected_intents (dict): Expected intents.
        actual_intents (dict): Actual intents.
        threshold (float): Similarity threshold (0 to 1).

    Raises:
        AssertionError: If any intent similarity is below the threshold.
    """
    for key, expected_intent in expected_intents.items():
        actual_intent = actual_intents.get(key, "")
        similarity = SequenceMatcher(None, expected_intent, actual_intent).ratio()
        assert similarity >= threshold, (
            f"Intent '{expected_intent}' and '{actual_intent}' are not similar enough. "
            f"Similarity: {similarity:.2f}"
        )


@patch("aethra.client.requests.post")
def test_overall_library_with_tolerance(mock_post, mock_conversation_data, mock_analysis_response):
    """
    Integration test for the overall library functionality with stochasticity handling.
    """
    # Mock AethraClient API response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_analysis_response
    mock_post.return_value = mock_response

    # Initialize the AethraClient
    client = AethraClient(
        api_key="mock_api_key",
        base_url="http://localhost:8002/"
    )

    # Perform the analysis
    analysis = client.analyse(
        conversation_data=mock_conversation_data,
        min_clusters=20,
        max_clusters=25,
        top_k_nearest_to_centroid=10
    )

    # Expected values
    expected_transition_matrix = np.array([
        [0.5, 0.5],
        [0.0, 0.0]
    ])
    expected_intent_by_cluster = {
        "0": "Greeting and small talk",
        "1": "Overall Intent: Greeting/Positive Response"
    }

    # Assert transition matrices are equal within a tolerance
    np.testing.assert_allclose(
        np.array(analysis.transition_matrix),
        expected_transition_matrix,
        rtol=1e-2,  # Relative tolerance
        atol=1e-3   # Absolute tolerance
    )


    # Process the graph
    graph_processor = GraphProcessor(analysis)

    # Apply filters to the graph
    filter_and_reconnect = FRFilter(min_weight=0.1, top_k=1)
    graph_processor.filter_graph(filter_strategy=filter_and_reconnect)

    # Verify that the graph is processed without errors
    assert graph_processor.graph is not None
    assert len(graph_processor.graph.edges) > 0

    # Optionally, verify additional properties of the graph
    edges = list(graph_processor.graph.edges(data=True))
    assert all("weight" in data for _, _, data in edges), "Filtered graph edges must contain weights."
