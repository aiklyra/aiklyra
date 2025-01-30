import json
import networkx as nx
import tempfile
import webbrowser
from pathlib import Path
from typing import Optional, Dict, List, Any

class SankeyGraphVisualizer:
    """
    A class to visualize a directed graph as a Sankey diagram using D3.js.

    Attributes:
        template (str): HTML template for the Sankey diagram visualization.
    """

    template = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Sankey Diagram</title>
            <script src="https://d3js.org/d3.v7.min.js"></script>
            <script src="https://cdn.jsdelivr.net/npm/d3-sankey@0.12.3/dist/d3-sankey.min.js"></script>
            <style>
                body {
                    margin: 0;
                    padding: 0;
                    background-color: rgb(0, 12, 27); /* Updated background color */
                    font-family: Arial, sans-serif;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                }

                .node text {
                    fill: white; 
                    font-size: 12px;
                }

                .link {
                    fill: none;
                }
            </style>
        </head>
        <body>
            <script>
                const data = {data};

                const width = 1000;
                const height = 700;

                const svg = d3.select("body").append("svg")
                    .attr("width", width)
                    .attr("height", height);

                const sankey = d3.sankey()
                    .nodeWidth(20)
                    .nodePadding(20)
                    .extent([[50, 50], [width - 50, height - 50]]);

                const graph = sankey({
                    nodes: data.nodes.map(d => Object.assign({}, d)),
                    links: data.links.map(d => Object.assign({}, d))
                });

                const defs = svg.append("defs");
                graph.links.forEach((link, i) => {
                    const gradient = defs.append("linearGradient")
                        .attr("id", `gradient${i}`)
                        .attr("gradientUnits", "userSpaceOnUse")
                        .attr("x1", link.source.x1)
                        .attr("y1", (link.source.y0 + link.source.y1) / 2)
                        .attr("x2", link.target.x0)
                        .attr("y2", (link.target.y0 + link.target.y1) / 2);

                    gradient.append("stop")
                        .attr("offset", "0%")
                        .attr("stop-color", "rgba(196, 253, 235,0.9)") /* Edges start white */
                        .attr("stop-opacity", 1);

                    gradient.append("stop")
                        .attr("offset", "100%")
                        .attr("stop-color", "rgba(196, 253, 235,0.9)") /* Edges turn transparent */
                        .attr("stop-opacity", 0.3);
                        .attr("stop-opacity", 0.3);
                });

                svg.append("g")
                    .selectAll("path")
                    .data(graph.links)
                    .enter()
                    .append("path")
                    .attr("class", "link")
                    .attr("d", d3.sankeyLinkHorizontal())
                    .style("stroke", (d, i) => `url(#gradient${i})`)
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
                    .style("fill", "rgba(196, 253, 235 ,0.8)"); /* Nodes set to white */

                svg.append("g")
                    .selectAll("text")
                    .data(graph.nodes)
                    .enter()
                    .append("text")
                    .attr("x", d => (d.x0 + d.x1) / 2 + 20) 
                    .attr("y", d => d.y0 - 8) 
                    .attr("dy", "0") 
                    .attr("text-anchor", "middle") 
                    .attr("x", d => (d.x0 + d.x1) / 2 + 20) 
                    .attr("y", d => d.y0 - 8) 
                    .attr("dy", "0") 
                    .attr("text-anchor", "middle") 
                    .text(d => d.name)
                    .style("fill", "rgba(255, 253, 235,0.9)") /* Text color set to white */
                    .style("font-size", "17px")
                    .style("font-family", "Courier New")
                    .style("font-weight", "bold"); 
                    .style("fill", "rgba(255, 253, 235,0.9)") /* Text color set to white */
                    .style("font-size", "17px")
                    .style("font-family", "Courier New")
                    .style("font-weight", "bold"); 
            </script>
        </body>
        </html>
        """

    @staticmethod
    def visualize(graph: nx.DiGraph, save_path: Optional[str] = None , render : bool = False ) -> str:
        """
        Visualizes a directed graph as a Sankey diagram and returns the HTML content.

        Args:
            graph (nx.DiGraph): The directed graph to visualize.
            save_path (Optional[str]): The path to save the HTML content. If None, a temporary file is used.
            render (bool): Whether to render the visualization in the browser. Default is False.
        Returns:
            str: The HTML content of the Sankey diagram.
        """
        nodes: List[Dict[str, Any]] = [{"name": str(node), "type": "client" if "client" in str(node).lower() else "agent"}
                                       for node in graph.nodes()]
        node_index: Dict[Any, int] = {node: i for i, node in enumerate(graph.nodes())}
        links: List[Dict[str, Any]] = [{"source": node_index[u], "target": node_index[v], "value": data.get("value", 1)}
                                       for u, v, data in graph.edges(data=True)]

        sankey_data: Dict[str, List[Dict[str, Any]]] = {
            "nodes": nodes,
            "links": links
        }
        html_content: str = SankeyGraphVisualizer.template.replace("{data}", json.dumps(sankey_data))

        if save_path:
            # Create the directory if it doesn't exist
            Path(save_path).parent.mkdir(parents=True, exist_ok=True)
            with open(save_path, "w") as file:
                file.write(html_content)
            if render :
                webbrowser.open(f"file://{Path(save_path).resolve()}")
        else:
            with tempfile.NamedTemporaryFile("w", delete=False, suffix=".html") as tmpfile:
                tmpfile.write(html_content)
                tmpfile_path = tmpfile.name
            if render :
                webbrowser.open(f"file://{Path(tmpfile_path).resolve()}")

        return html_content

if __name__ == '__main__':
    nodes = [
    "Customer Inquiry",         # "Hello" - Initial customer message
    "Agent Uses Tool",          # "Automated Acknowledgment" -> Changed
    "Clarification Request",    # "Response2" - Customer seeking clarification
    "Agent Response",           # "Response3" - Human agent responds
    "Customer Provides Info",   # "Response4" - Customer shares details
    "Solution Provided",        # "Response5" - Agent suggests a solution
    "Escalation to Supervisor", # "Response7" - Issue is escalated
    "Final Resolution",         # "Response8" - Issue resolved
    "End"        # "Exit" - Conversation ends
    ]



    links = [
    (0, 1, 10),  # Customer Inquiry -> Agent Uses Tool
    (0, 2, 20),  # Customer Inquiry -> Clarification Request
    (1, 5, 5),   # Agent Uses Tool -> Solution Provided
    (2, 3, 8),   # Clarification Request -> Agent Response
    (2, 4, 12),  # Clarification Request -> Customer Provides Info
    (3, 6, 4),   # Agent Response -> Escalation to Supervisor
    (3, 7, 6),   # Agent Response -> Final Resolution
    (4, 8, 3),   # Customer Provides Info -> End of Interaction
    (5, 8, 10),  # Solution Provided -> End of Interaction (New)
    (6, 8, 10),  # Escalation to Supervisor -> End of Interaction (New)
    (7, 8, 10)   # Final Resolution -> End of Interaction (New)
    ]
    nodes = [
    "Customer Inquiry",         # "Hello" - Initial customer message
    "Agent Uses Tool",          # "Automated Acknowledgment" -> Changed
    "Clarification Request",    # "Response2" - Customer seeking clarification
    "Agent Response",           # "Response3" - Human agent responds
    "Customer Provides Info",   # "Response4" - Customer shares details
    "Solution Provided",        # "Response5" - Agent suggests a solution
    "Escalation to Supervisor", # "Response7" - Issue is escalated
    "Final Resolution",         # "Response8" - Issue resolved
    "End"        # "Exit" - Conversation ends
    ]



    links = [
    (0, 1, 10),  # Customer Inquiry -> Agent Uses Tool
    (0, 2, 20),  # Customer Inquiry -> Clarification Request
    (1, 5, 5),   # Agent Uses Tool -> Solution Provided
    (2, 3, 8),   # Clarification Request -> Agent Response
    (2, 4, 12),  # Clarification Request -> Customer Provides Info
    (3, 6, 4),   # Agent Response -> Escalation to Supervisor
    (3, 7, 6),   # Agent Response -> Final Resolution
    (4, 8, 3),   # Customer Provides Info -> End of Interaction
    (5, 8, 10),  # Solution Provided -> End of Interaction (New)
    (6, 8, 10),  # Escalation to Supervisor -> End of Interaction (New)
    (7, 8, 10)   # Final Resolution -> End of Interaction (New)
    ]

    # Create a directed graph
    G = nx.DiGraph()
    index_to_name = {i: name for i, name in enumerate(nodes)}
    # Add nodes with labels
    for i, name in enumerate(nodes):
        G.add_node(name)

    # Add edges with weights
    for src, tgt, weight in links:
        G.add_edge(index_to_name[src], index_to_name[tgt], weight=weight)

    index_to_name = {i: name for i, name in enumerate(nodes)}
    # Add nodes with labels
    for i, name in enumerate(nodes):
        G.add_node(name)

    # Add edges with weights
    for src, tgt, weight in links:
        G.add_edge(index_to_name[src], index_to_name[tgt], weight=weight)

    SankeyGraphVisualizer.visualize(G, save_path="output/sankey_diagram.html")
