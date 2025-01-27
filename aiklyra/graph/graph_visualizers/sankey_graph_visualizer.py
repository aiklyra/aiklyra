from .base_graph_visualizer import BaseGraphVisualizer
import networkx as nx
import json


class SankeyGraphVisualizer(BaseGraphVisualizer):
    """
    A class for visualizing directed graphs as interactive Sankey diagrams using D3.js.

    This visualizer generates an HTML file that can be opened in a web browser to view
    an interactive Sankey diagram representation of a directed graph.

    Methods
    -------
    visualize(graph, output_file="sankey_diagram.html", **kwargs)
        Generates and saves a Sankey diagram based on the input graph.

    """

    def visualize(
        graph: nx.DiGraph,
        output_file="sankey_diagram.html",
        width=1000,
        height=700,
        node_width=20,
        node_padding=20,
        primary_color="rgba(103, 114, 229, 1)",
        secondary_color="rgba(172, 85, 251, 1)",
        tertiary_color="rgba(103, 114, 229, 0.2)",
        background_color="rgb(32, 35, 55)",
        font_family="Arial, sans-serif",
        font_size="12px",
    ):
        """
        Generates an interactive Sankey diagram for a directed graph.

        Parameters
        ----------
        graph : nx.DiGraph
            The directed graph to be visualized. Nodes and edges in the graph
            can have additional attributes, such as weights, which will influence
            the size of the links in the diagram.

        output_file : str, optional
            The name of the output HTML file (default is "sankey_diagram.html").

        width : int, optional
            The width of the SVG canvas in pixels (default is 1000).

        height : int, optional
            The height of the SVG canvas in pixels (default is 700).

        node_width : int, optional
            The width of each node in the diagram (default is 20).

        node_padding : int, optional
            The vertical padding between nodes in the diagram (default is 20).

        primary_color : str, optional
            The primary color for the nodes (default is "rgba(103, 114, 229, 1)").

        secondary_color : str, optional
            The secondary color for the nodes (default is "rgba(172, 85, 251, 1)").

        tertiary_color : str, optional
            The tertiary color used for gradient effects on the links (default is "rgba(103, 114, 229, 0.2)").

        background_color : str, optional
            The background color of the diagram (default is "rgb(32, 35, 55)").

        font_family : str, optional
            The font family used for node labels (default is "Arial, sans-serif").

        font_size : str, optional
            The font size used for node labels (default is "12px").

        Notes
        -----
        - The method creates an HTML file containing the diagram, which can be viewed in any modern browser.
        - D3.js and d3-sankey libraries are loaded from external CDNs.
        - Edge weights can be specified in the input graph to adjust the width of the links.

        Examples
        --------
        >>> import networkx as nx
        >>> from sankey_visualizer import SankeyGraphVisualizer
        >>> graph = nx.DiGraph()
        >>> graph.add_edge("A", "B", weight=3)
        >>> graph.add_edge("B", "C", weight=2)
        >>> visualizer = SankeyGraphVisualizer()
        >>> visualizer.visualize(graph, output_file="example_sankey.html")
        Sankey diagram saved to example_sankey.html. Open it in a browser to view the visualization.
        """
        nodes = [{"name": str(node)} for node in graph.nodes()]
        node_indices = {node: i for i, node in enumerate(graph.nodes())}
        links = [
            {
                "source": node_indices[edge[0]],
                "target": node_indices[edge[1]],
                "value": graph.edges[edge].get("weight", 1),
            }
            for edge in graph.edges()
        ]

        # HTML and JS template for the Sankey diagram
        html_template = html_template = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Sankey Diagram</title>
                <script src="https://d3js.org/d3.v7.min.js"></script>
                <script src="https://cdn.jsdelivr.net/npm/d3-sankey@0.12.3/dist/d3-sankey.min.js"></script>
                <style>
                    body {{
                        margin: 0;
                        padding: 0;
                        background-color: {background_color};
                        font-family: {font_family};
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                    }}

                    .node text {{
                        fill: white; 
                        font-size: {font_size};
                    }}

                    .link {{
                        fill: none;
                    }}
                </style>
            </head>
            <body>
                <script>
                    const data = {json.dumps({"nodes": nodes, "links": links}, indent=4)};

                    const width = {width};
                    const height = {height};

                    const svg = d3.select("body").append("svg")
                        .attr("width", width)
                        .attr("height", height);

                    const sankey = d3.sankey()
                        .nodeWidth({node_width})
                        .nodePadding({node_padding})
                        .extent([[50, 50], [width - 50, height - 50]]);

                    const graph = sankey(data);

                    svg.append("g")
                        .selectAll("path")
                        .data(graph.links)
                        .enter()
                        .append("path")
                        .attr("class", "link")
                        .attr("d", d3.sankeyLinkHorizontal())
                        .style("stroke-width", d => Math.max(1, d.width));

                    svg.append("g")
                        .selectAll("rect")
                        .data(graph.nodes)
                        .enter()
                        .append("rect")
                        .attr("x", d => d.x0)
                        .attr("y", d => d.y0)
                        .attr("height", d => d.y1 - d.y0)
                        .attr("width", sankey.nodeWidth())
                        .style("fill", "{primary_color}");

                    svg.append("g")
                        .selectAll("text")
                        .data(graph.nodes)
                        .enter()
                        .append("text")
                        .attr("x", d => d.x0)
                        .attr("y", d => d.y0)
                        .text(d => d.name);
                </script>
            </body>
            </html>
        """


        # Write the HTML to the specified file
        with open(output_file, "w") as f:
            f.write(html_template)

        print(f"Sankey diagram saved to {output_file}. Open it in a browser to view the visualization.")
