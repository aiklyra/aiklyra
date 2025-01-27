import pytest
import networkx as nx
from aiklyra.graph.graph_visualizers import InteractiveGraphVisualizer, StaticGraphVisualizer, SankeyGraphVisualizer
import os


@pytest.fixture
def sample_graph():
    """Fixture for creating a sample directed graph with weights."""
    graph = nx.DiGraph()
    graph.add_node(1)
    graph.add_node(2)
    graph.add_node(3)
    graph.add_edge(1, 2, weight=0.5)
    graph.add_edge(2, 3, weight=1.5)
    graph.add_edge(3, 1, weight=2.0)
    return graph


@pytest.fixture
def simple_graph():
    """Fixture for a simple graph with no edge weights."""
    graph = nx.DiGraph()
    graph.add_edges_from([(1, 2), (2, 3), (3, 4)])
    return graph


def test_interactive_graph_visualizer_render(sample_graph):
    """Test if the InteractiveGraphVisualizer renders without errors."""
    save_path = os.path.join(
        os.getcwd(), "tests", "test_results", "graph", "interactive", "interactive_graph.html"
    )

    # Ensure the directory exists
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    # Render graph and save to the specified directory
    InteractiveGraphVisualizer.visualize(graph=sample_graph, save_path=save_path)

    # Ensure the file was created
    assert os.path.exists(save_path)


def test_interactive_graph_visualizer_no_save(sample_graph):
    """Test if the InteractiveGraphVisualizer renders to an inline browser."""
    try:
        InteractiveGraphVisualizer.visualize(graph=sample_graph)
    except Exception as e:
        pytest.fail(f"InteractiveGraphVisualizer failed with exception: {e}")


def test_static_graph_visualizer_render(sample_graph):
    """Test if the StaticGraphVisualizer renders and saves the graph."""
    save_path = os.path.join(
        os.getcwd(), "tests", "test_results", "graph", "static", "static_graph.png"
    )

    # Ensure the directory exists
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    # Render graph and save to the specified directory
    StaticGraphVisualizer.visualize(
        graph=sample_graph,
        save_path=save_path,
        layout='spring',
        figsize=(10, 10),
        with_labels=True,
        node_color='green',
        edge_color='black'
    )

    # Ensure the file was created
    assert os.path.exists(save_path)


def test_static_graph_visualizer_no_save(sample_graph):
    """Test if the StaticGraphVisualizer renders to the screen without saving."""
    try:
        StaticGraphVisualizer.visualize(graph=sample_graph)
    except Exception as e:
        pytest.fail(f"StaticGraphVisualizer failed with exception: {e}")


def test_interactive_graph_visualizer_edge_color_normalization(sample_graph):
    """Test if the InteractiveGraphVisualizer correctly normalizes edge colors."""
    save_path = os.path.join(
        os.getcwd(), "tests", "test_results", "graph", "interactive", "interactive_graph_test.html"
    )

    # Ensure the directory exists
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    try:
        # Call the visualize method
        InteractiveGraphVisualizer.visualize(
            graph=sample_graph,
            save_path=save_path
        )
    except Exception as e:
        pytest.fail(f"InteractiveGraphVisualizer edge color normalization failed: {e}")


def test_static_graph_visualizer_layouts(sample_graph):
    """Test if the StaticGraphVisualizer works with different layouts."""
    layouts = ['spring', 'circular', 'shell', 'random']
    for layout in layouts:
        save_path = os.path.join(
            os.getcwd(), "tests", "test_results", "graph", "static", f"static_{layout}_graph_test.svg"
        )

        # Ensure the directory exists
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        try:
            # Call the visualize method
            StaticGraphVisualizer.visualize(
                graph=sample_graph,
                layout=layout,
                save_path=save_path
            )
        except Exception as e:
            pytest.fail(f"StaticGraphVisualizer failed with layout '{layout}': {e}")


# --- Tests for SankeyGraphVisualizer ---

def test_sankey_graph_visualizer_render(sample_graph):
    """Test if the SankeyGraphVisualizer renders without errors."""
    save_path = os.path.join(
        os.getcwd(), "tests", "test_results", "graph", "sankey", "sankey_graph.html"
    )

    # Ensure the directory exists
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    try:
        # Render graph and save to the specified directory
        SankeyGraphVisualizer.visualize(graph=sample_graph, save_path=save_path)
    except Exception as e:
        pytest.fail(f"SankeyGraphVisualizer failed with exception: {e}")

    # Ensure the file was created
    assert os.path.exists(save_path)


def test_sankey_graph_visualizer_no_weights(simple_graph):
    """Test if the SankeyGraphVisualizer works with a graph that has no weights."""
    save_path = os.path.join(
        os.getcwd(), "tests", "test_results", "graph", "sankey", "sankey_no_weights.html"
    )

    # Ensure the directory exists
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    try:
        # Render graph and save to the specified directory
        SankeyGraphVisualizer.visualize(graph=simple_graph, save_path=save_path)
    except Exception as e:
        pytest.fail(f"SankeyGraphVisualizer failed with exception: {e}")

    # Ensure the file was created
    assert os.path.exists(save_path)




def test_sankey_graph_visualizer_large_graph():
    """Test if the SankeyGraphVisualizer handles a large graph."""
    graph = nx.DiGraph()
    for i in range(100):
        graph.add_edge(i, i + 1, weight=i * 0.1)

    save_path = os.path.join(
        os.getcwd(), "tests", "test_results", "graph", "sankey", "sankey_large_graph.html"
    )

    # Ensure the directory exists
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    try:
        # Render graph and save to the specified directory
        SankeyGraphVisualizer.visualize(graph=graph, save_path=save_path)
    except Exception as e:
        pytest.fail(f"SankeyGraphVisualizer failed with a large graph: {e}")

    # Ensure the file was created
    assert os.path.exists(save_path)
