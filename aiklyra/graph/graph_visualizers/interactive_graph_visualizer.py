from .base_graph_visualizer import BaseGraphVisualizer
from pyvis.network import Network
from typing import Optional
import networkx as nx 
 


class InteractiveGraphVisualizer(BaseGraphVisualizer):
    def visualize(
        graph : nx.DiGraph , 
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
        avoid_overlap: float = 0.92
    ):
        """
        Create an interactive graph visualization using PyVis with parameterized options.

        Args:
            graph (nx.DiGraph) : graph to be visualized 
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


        # Add nodes with default labels and titles
        for node in graph.nodes:
            net.add_node(node, label=str(node), title=str(node))

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
            return f'rgb({int(255 * normalized_weight)}, 0, {int(255 * (1 - normalized_weight))})'

        for u, v, data in graph.edges(data=True):
            weight = data.get('weight', 1)
            color = get_edge_color(weight)
            net.add_edge(u, v, value=weight, title=f'Weight: {weight:.2f}', color=color)

        # Set visualization options dynamically
        net.set_options(f"""
        var options = {{
            "nodes": {{
                "font": {{
                    "size": {node_font_size}
                }}
            }},
            "edges": {{
                "arrows": {{
                    "to": {{
                        "enabled": true,
                        "scaleFactor": {arrow_scale_factor}
                    }}
                }},
                "font": {{
                    "size": {edge_font_size},
                    "align": "horizontal"
                }},
                "smooth": {{
                    "enabled": true,
                    "type": "dynamic"
                }}
            }},
            "physics": {{
                "enabled": {str(physics_enabled).lower()},
                "solver": "{physics_solver}",
                "{physics_solver}": {{
                    "theta": 0.5,
                    "gravitationalConstant": {gravitational_constant},
                    "centralGravity": {central_gravity},
                    "springLength": {spring_length},
                    "springConstant": {spring_constant},
                    "damping": {damping},
                    "avoidOverlap": {avoid_overlap}
                }},
                "maxVelocity": 41,
                "minVelocity": 1,
                "timestep": 0.5
            }}
        }}
        """)

        # Show or save the graph
        if save_path:
            net.show(save_path)
        else:
            net.show("graph.html")
    