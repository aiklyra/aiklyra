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
                        .attr("stop-opacity", 0);
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
                    .attr("x", d => d.x0 + 10) // Position text 10px to the left of the node's left edge
                    .attr("y", d => (d.y0 + d.y1) / 2 ) // Center text vertically relative to the node
                    .attr("text-anchor", "end") // Align text to the "end" (right side before rotation)
                    .attr("dominant-baseline", "middle") // Center text vertically
                    .attr("transform", d => `rotate(-90, ${d.x0 - 10}, ${(d.y0 + d.y1) / 2})`) // Rotate text -90 degrees around (x, y)
                    .text(d => d.name)
                    .style("fill", "rgb(233, 233, 233)");
            </script>
        </body>
        </html>
        """

    @staticmethod
    def visualize(graph: nx.DiGraph, save_path: Optional[str] = None) -> str:
        """
        Visualizes a directed graph as a Sankey diagram and returns the HTML content.

        Args:
            graph (nx.DiGraph): The directed graph to visualize.
            save_path (Optional[str]): The path to save the HTML content. If None, a temporary file is used.

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
            webbrowser.open(f"file://{Path(save_path).resolve()}")
        else:
            with tempfile.NamedTemporaryFile("w", delete=False, suffix=".html") as tmpfile:
                tmpfile.write(html_content)
                tmpfile_path = tmpfile.name
            webbrowser.open(f"file://{Path(tmpfile_path).resolve()}")

        return html_content

if __name__ == '__main__':
    import networkx as nx

    # Create a directed graph
    G = nx.DiGraph()

    # Add nodes
    G.add_node("Agent Greets the Client")  # Start with a polite greeting
    G.add_node("Agent Identifies Issue")  # Ask diagnostic questions to understand the problem
    G.add_node("Agent Correctly Uses Tool")  # Attempt to use a tool for stock extraction
    G.add_node("Error & Client Upset")  # Error during database access and client becomes mad
    G.add_node("Agent Answers FAQ Questions")  # Client asks FAQs, agent responds correctly
    G.add_node("Agent Wrongly Uses Tool")  # Agent uses the database tool incorrectly
    G.add_node("End of Interaction")  # End interaction politely and with gratitude

    # Add edges with probabilities
    G.add_edge("Agent Greets the Client", "Agent Identifies Issue", value=50)  # Proceed to identifying issue
    G.add_edge("Agent Greets the Client", "Agent Answers FAQ Questions", value=30)  # Client directly asks FAQs
    G.add_edge("Agent Greets the Client", "Agent Wrongly Uses Tool", value=20)  # Agent misuses database tool early

    G.add_edge("Agent Identifies Issue", "Agent Correctly Uses Tool", value=50)  # Correct use of database tool
    G.add_edge("Agent Identifies Issue", "Agent Wrongly Uses Tool", value=30)  # Misuse of database tool
    G.add_edge("Agent Identifies Issue", "Agent Answers FAQ Questions", value=20)  # Client has FAQs instead

    G.add_edge("Agent Correctly Uses Tool", "End of Interaction", value=40)  # Successful issue resolution

    G.add_edge("Agent Wrongly Uses Tool", "Agent Correctly Uses Tool", value=50)  # Correct mistake, try again
    G.add_edge("Agent Wrongly Uses Tool", "Error & Client Upset", value=30)  # Repeated issues, client upset

    G.add_edge("Agent Answers FAQ Questions", "End of Interaction", value=50)  # End happily after FAQ resolution

    G.add_edge("Error & Client Upset", "End of Interaction", value=90)  # Apologize and end politely
    # Visualize the graph
    SankeyGraphVisualizer.visualize(G, save_path="output/sankey_diagram.html")