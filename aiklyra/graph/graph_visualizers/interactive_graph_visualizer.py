from .base_graph_visualizer import BaseGraphVisualizer
from pyvis.network import Network
from typing import Optional
import networkx as nx 


class InteractiveGraphVisualizer(BaseGraphVisualizer):
    """
    A class for creating interactive graph visualizations using the PyVis library.

    This class provides a method to visualize a directed graph (`nx.DiGraph`) interactively in a web-based interface.
    The visualization is highly customizable, allowing users to configure node and edge styles, physics simulation
    parameters, and more. The resulting visualization can be displayed in a Jupyter notebook or saved as an HTML file.

    Attributes:
        None

    Methods:
        visualize(graph, save_path, notebook, width, height, directed, node_font_size, edge_font_size, 
                 arrow_scale_factor, physics_enabled, physics_solver, gravitational_constant, central_gravity, 
                 spring_length, spring_constant, damping, avoid_overlap, max_velocity, min_velocity, timestep, 
                 node_shape, node_border_width, node_color, edge_smooth_type, edge_color, arrow_to_enabled, 
                 arrow_middle_enabled, arrow_from_enabled):
            Creates an interactive graph visualization with customizable parameters.
    """
    def visualize(
        graph: nx.DiGraph, 
        save_path: Optional[str] = None,
        notebook: bool = True,
        width: str = "100%",
        height: str = "700px",
        directed: bool = True,
        node_font_size: int = 20,
        edge_font_size: int = 14,
        arrow_scale_factor: float = 1.0,
        physics_enabled: bool = True,
        physics_solver: str = "forceAtlas2Based",
        gravitational_constant: int = -86,
        central_gravity: float = 0.005,
        spring_length: int = 120,
        spring_constant: float = 0.04,
        damping: float = 0.57,
        avoid_overlap: float = 0.92,
        max_velocity: int = 50,
        min_velocity: int = 1,
        timestep: float = 0.5,
        node_shape: str = "dot",
        node_border_width: int = 1,
        node_color: Optional[str] = None,
        edge_smooth_type: str = "dynamic",
        edge_color: Optional[str] = None,
        arrow_to_enabled: bool = True,
        arrow_middle_enabled: bool = False,
        arrow_from_enabled: bool = False
    ):
        """
        Create an interactive graph visualization using PyVis with parameterized options.

        Args:
            graph (nx.DiGraph): Graph to be visualized.
            save_path (Optional[str]): Path to save the HTML visualization. If None, display the graph in the browser.
            notebook (bool): Whether to render the visualization in a Jupyter notebook. Default is False.
            width (str): Width of the visualization. Default is "100%".
            height (str): Height of the visualization. Default is "700px".
            directed (bool): Whether the graph is directed. Default is True.
            node_font_size (int): Font size for nodes. Default is 20.
            edge_font_size (int): Font size for edges. Default is 14.
            arrow_scale_factor (float): Scale factor for arrows. Default is 1.0.
            physics_enabled (bool): Whether to enable physics simulation. Default is True.
            physics_solver (str): Physics solver to use. Default is "forceAtlas2Based".
            gravitational_constant (int): Gravitational constant for the physics simulation. Default is -86.
            central_gravity (float): Central gravity for the physics simulation. Default is 0.005.
            spring_length (int): Spring length for the physics simulation. Default is 120.
            spring_constant (float): Spring constant for the physics simulation. Default is 0.04.
            damping (float): Damping for the physics simulation. Default is 0.57.
            avoid_overlap (float): Avoid overlap for the physics simulation. Default is 0.92.
            max_velocity (int): Maximum velocity for the physics simulation. Default is 50.
            min_velocity (int): Minimum velocity for the physics simulation. Default is 1.
            timestep (float): Time step for the physics simulation. Default is 0.5.
            node_shape (str): Shape of nodes (e.g., "dot", "ellipse"). Default is "dot".
            node_border_width (int): Border width for nodes. Default is 1.
            node_color (Optional[str]): Default color for nodes. Default is None.
            edge_smooth_type (str): Type of edge smoothing (e.g., "dynamic", "continuous"). Default is "dynamic".
            edge_color (Optional[str]): Default color for edges. Default is None.
            arrow_to_enabled (bool): Whether to enable arrow pointing to the target node. Default is True.
            arrow_middle_enabled (bool): Whether to enable arrow in the middle of the edge. Default is False.
            arrow_from_enabled (bool): Whether to enable arrow pointing from the source node. Default is False.
        """
        net = Network(
            notebook=notebook,
            width=width,
            height=height,
            directed=directed,
            cdn_resources="in_line"
        )
        if not hasattr(net, "template") or net.template is None:
            raise RuntimeError("PyVis failed to initialize its HTML template.")

        # Add nodes with parameters
        for node in graph.nodes:
            net.add_node(
                node, 
                label=str(node), 
                title=str(node), 
                shape=node_shape, 
                borderWidth=node_border_width,
                color=node_color
            )

        # Calculate edge weights for normalization
        min_weight = float('inf')
        max_weight = float('-inf')
        for u, v, data in graph.edges(data=True):
            weight = data.get('weight', 1)
            min_weight = min(min_weight, weight)
            max_weight = max(max_weight, weight)

        # Normalize weights and assign edge colors
        def get_edge_color(weight: float) -> str:
            normalized_weight = (weight - min_weight) / (max_weight - min_weight) if max_weight > min_weight else 0
            return edge_color or f'rgb({int(255 * normalized_weight)}, 0, {int(255 * (1 - normalized_weight))})'

        for u, v, data in graph.edges(data=True):
            weight = data.get('weight', 1)
            color = get_edge_color(weight)
            net.add_edge(
                u, 
                v, 
                value=weight, 
                title=f'Weight: {weight:.2f}', 
                color=color
            )

        # Set visualization options dynamically
        net.set_options(f"""
        var options = {{
            "nodes": {{
                "font": {{
                    "size": {node_font_size}
                }},
                "shape": "{node_shape}",
                "borderWidth": {node_border_width}
            }},
            "edges": {{
                "arrows": {{
                    "to": {{
                        "enabled": {str(arrow_to_enabled).lower()},
                        "scaleFactor": {arrow_scale_factor}
                    }},
                    "middle": {{
                        "enabled": {str(arrow_middle_enabled).lower()}
                    }},
                    "from": {{
                        "enabled": {str(arrow_from_enabled).lower()}
                    }}
                }},
                "font": {{
                    "size": {edge_font_size},
                    "align": "horizontal"
                }},
                "smooth": {{
                    "enabled": true,
                    "type": "{edge_smooth_type}"
                }}
            }},
            "physics": {{
                "enabled": {str(physics_enabled).lower()},
                "solver": "{physics_solver}",
                "{physics_solver}": {{
                    "gravitationalConstant": {gravitational_constant},
                    "centralGravity": {central_gravity},
                    "springLength": {spring_length},
                    "springConstant": {spring_constant},
                    "damping": {damping},
                    "avoidOverlap": {avoid_overlap}
                }},
                "maxVelocity": {max_velocity},
                "minVelocity": {min_velocity},
                "timestep": {timestep}
            }}
        }}
        """)

        # Show or save the graph
        if save_path:
            net.show(save_path)
        else:
            net.show("graph.html")
