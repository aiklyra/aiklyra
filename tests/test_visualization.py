import pytest
import networkx as nx
from aiklyra.graph.graph_visualizers import InteractiveGraphVisualizer, StaticGraphVisualizer
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

def test_interactive_graph_visualizer_render(sample_graph, tmpdir):
    """Test if the InteractiveGraphVisualizer renders without errors."""
    save_path = tmpdir.join("interactive_graph.html")

    # Render graph and save to a temporary directory
    InteractiveGraphVisualizer.visualize(graph=sample_graph, save_path=str(save_path))

    # Ensure the file was created
    assert save_path.check(file=True)

def test_interactive_graph_visualizer_no_save(sample_graph):
    """Test if the InteractiveGraphVisualizer renders to an inline browser."""

    # This test checks for no exceptions when rendering without save_path
    try:
        InteractiveGraphVisualizer.visualize(graph=sample_graph)
    except Exception as e:
        pytest.fail(f"InteractiveGraphVisualizer failed with exception: {e}")

def test_static_graph_visualizer_render(sample_graph, tmpdir):
    """Test if the StaticGraphVisualizer renders and saves the graph."""
    save_path = tmpdir.join("static_graph.png")

    # Render graph and save to a temporary directory
    StaticGraphVisualizer.visualize(
        graph=sample_graph,
        save_path=str(save_path),
        layout='spring',
        figsize=(10, 10),
        with_labels=True,
        node_color='green',
        edge_color='black'
    )

    # Ensure the file was created
    assert save_path.check(file=True)

def test_static_graph_visualizer_no_save(sample_graph):
    """Test if the StaticGraphVisualizer renders to the screen without saving."""

    try:
        StaticGraphVisualizer.visualize(graph=sample_graph)
    except Exception as e:
        pytest.fail(f"StaticGraphVisualizer failed with exception: {e}")

def test_interactive_graph_visualizer_edge_color_normalization(sample_graph):
    """Test if the InteractiveGraphVisualizer correctly normalizes edge colors."""

    # Define the save path
    save_path = os.path.join(os.getcwd(), "tests", "test_results", "graph", "interactive_graph_test.html")

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
        # Define the save path
        save_path = os.path.join(os.getcwd(),"tests" ,  "test_results", "graph", f"static_{layout}_graph_test.svg")

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
