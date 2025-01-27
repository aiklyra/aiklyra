import json
import networkx as nx
import tempfile
import webbrowser
from pathlib import Path

class SankeyGraphVisualizer:
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
                    background-color: rgb(32, 35, 55);
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
                        .attr("stop-color", "rgba(150, 85, 255, 1)")
                        .attr("stop-opacity", 1);

                    gradient.append("stop")
                        .attr("offset", "100%")
                        .attr("stop-color", "rgba(103, 114, 229, 0.2)")
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
                    .style("fill", d => d.type === "client" ? "rgba(103, 114, 229, 1)" : "rgba(172, 85, 251, 1)");

                svg.append("g")
                    .selectAll("text")
                    .data(graph.nodes)
                    .enter()
                    .append("text")
                    .attr("x", d => (d.x0 + d.x1) / 2)
                    .attr("y", d => d.y0 - 5)
                    .attr("dy", "0")
                    .attr("text-anchor", "middle")
                    .text(d => d.name)
                    .style("fill", "white");
            </script>
        </body>
        </html>
        """

    def visualize(graph: nx.DiGraph):
        nodes = [{"name": str(node), "type": "client" if "client" in str(node).lower() else "agent"}
                 for node in graph.nodes()]
        node_index = {node: i for i, node in enumerate(graph.nodes())}
        links = [{"source": node_index[u], "target": node_index[v], "value": data.get("value", 1)}
                 for u, v, data in graph.edges(data=True)]

        sankey_data = {
            "nodes": nodes,
            "links": links
        }
        html_content = SankeyGraphVisualizer.template.replace("{data}", json.dumps(sankey_data))

        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".html") as tmpfile:
            tmpfile.write(html_content)
            tmpfile_path = tmpfile.name

        webbrowser.open(f"file://{Path(tmpfile_path).resolve()}")


