import utils
import streamlit as st
import pandas as pd
import pygwalker as pyg
from pygwalker.api.streamlit import StreamlitRenderer

import bushy_client as bc


import streamlit.components.v1 as components
import json

st.set_page_config(page_title="FEG graphs", page_icon="📉", layout="wide")
st.header('📉FEG graphs')
st.write('Allows users to interact with the FEG')

# Retrieve and load the task configuration
config_name = "graphs"
config = bc.get_config_from_server_cached(config_name)

if config and config_name in config:
    TASK_DEFINITIONS = config
    TASK_KEYS = TASK_DEFINITIONS[config_name].keys()
    TASK_PARAMETERS = {k: v['params'] for k, v in TASK_DEFINITIONS[config_name].items()}
    TASK_NAMES = {k: v['name'] for k, v in TASK_DEFINITIONS[config_name].items()}
    TASK_DESCRIPTIONS = {k: v['description'] for k, v in TASK_DEFINITIONS[config_name].items()}
    TASK_KEYS_TO_NAMES = {v['name']: k for k, v in TASK_DEFINITIONS[config_name].items()}

    class GraphChatbot:

        def __init__(self):
            utils.sync_st_session()
            self.df = pd.DataFrame()

        def main(self):
            st.sidebar.header("Graphs")
            name = st.sidebar.radio("Select graphs:", sorted(list(TASK_KEYS_TO_NAMES.keys())))

            # Get the corresponding key for the selected description
            task_key = TASK_KEYS_TO_NAMES[name]

            # Display input fields based on selected task
            parameters = TASK_PARAMETERS[task_key]
            inputs = {}
            if parameters:  # Check if there are any parameters
                st.sidebar.header("Graphs Parameters")
                for param in parameters:
                    inputs[param] = st.sidebar.text_input(param.capitalize().replace('_', ' '), placeholder=f"Enter {param}")

            st.write("## Graphs")

            # Button to generate report
            if st.sidebar.button("Generate graph"):
                # Display the selected option
                st.chat_message('user').write(TASK_NAMES[task_key])

                # Get response from the API
                response_data = bc.get_graph_response_cached(task_key, inputs)
                
                if response_data and 'response' in response_data:
                    if response_data:
                        graph_json = response_data['response']

                        # HTML and JavaScript code for D3.js visualization
                        html_code = f"""
                        <!DOCTYPE html>
                        <html>
                        <head>
                            <title>Graph Visualization</title>
                            <script src="https://d3js.org/d3.v6.min.js"></script>
                            <style>
                                .node {{ stroke: #fff; stroke-width: 1.5px; }}
                                .link {{ stroke: #999; stroke-opacity: 0.6; }}
                                body, html {{ margin: 0; padding: 0; width: 100%; height: 100%; overflow: hidden; }}
                                svg {{ display: block; }}
                            </style>
                        </head>
                        <body>
                            <div id="graph-container" style="width: 100vw; height: 100vh;"></div>
                            <script>
                                // Load the graph data
                                const graph = {graph_json};
                                console.log("Graph data:", graph);  // Debugging message

                                const container = document.getElementById('graph-container');
                                const width = container.clientWidth;
                                const height = container.clientHeight;

                                const svg = d3.select("#graph-container").append("svg")
                                    .attr("width", width)
                                    .attr("height", height)
                                    .call(d3.zoom().on("zoom", (event) => {{
                                        svg.attr("transform", event.transform);
                                    }}))
                                    .append("g");

                                // Define a color scale
                                const color = d3.scaleOrdinal(d3.schemeCategory10);

                                const simulation = d3.forceSimulation(graph.nodes)
                                    .force("link", d3.forceLink(graph.relationships).id(d => d.element_id))
                                    .force("charge", d3.forceManyBody())
                                    .force("center", d3.forceCenter(width / 2, height / 2));

                                const link = svg.append("g")
                                    .attr("class", "links")
                                    .selectAll("line")
                                    .data(graph.relationships)
                                    .enter().append("line")
                                    .attr("class", "link");

                                const node = svg.append("g")
                                    .attr("class", "nodes")
                                    .selectAll("image")
                                    .data(graph.nodes)
                                    .enter().append("image")
                                    .attr("class", "node")
                                    .attr("width", 20)
                                    .attr("height", 20)
                                    .attr("xlink:href", d => {{
                                        switch (d.labels[0]) {{
                                        case 'Player':
                                            return 'https://img.icons8.com/fluency/48/000000/person-male.png'; // Customer icon
                                        case 'Email':
                                            return 'https://img.icons8.com/fluency/48/000000/new-post.png'; // Email icon
                                        case 'Phone':
                                            return 'https://img.icons8.com/fluency/48/000000/phone.png'; // Phone icon
                                        case 'Ip':
                                            return 'https://img.icons8.com/fluency/48/000000/router.png'; // IP icon
                                        case 'Transaction':
                                            return 'https://img.icons8.com/fluency/48/000000/exchange.png'; // Transaction icon
                                        case 'User':
                                            return 'https://img.icons8.com/fluency/48/000000/user-male-circle.png'; // User icon
                                        case 'DeviceHash':
                                            return 'https://img.icons8.com/fluency/48/000000/computer.png'; // Device icon
                                        case 'DeviceId':
                                            return 'https://img.icons8.com/fluency/48/000000/computer.png'; // Device icon
                                        default:
                                            return 'https://img.icons8.com/fluency/48/000000/question-mark.png'; // Default icon
                                        }}
                                    }})
                                    .call(d3.drag()
                                        .on("start", dragstarted)
                                        .on("drag", dragged)
                                        .on("end", dragended));

                                node.append("title")
                                    .text(d => {{
                                        if (d.labels[0] === 'Player') {{
                                            return d.user_name;  // Show the username if the label is 'Player'
                                        }} else {{
                                            return d.value;  // Otherwise, show the value
                                        }}
                                    }});

                                simulation.on("tick", () => {{
                                    link.attr("x1", d => d.source.x)
                                        .attr("y1", d => d.source.y)
                                        .attr("x2", d => d.target.x)
                                        .attr("y2", d => d.target.y);

                                    node.attr("x", d => d.x - 10)  // Center the image
                                        .attr("y", d => d.y - 10); // Center the image
                                }});

                                function dragstarted(event, d) {{
                                    if (!event.active) simulation.alphaTarget(0.3).restart();
                                    d.fx = d.x;
                                    d.fy = d.y;
                                }}

                                function dragged(event, d) {{
                                    d.fx = event.x;
                                    d.fy = event.y;
                                }}

                                function dragended(event, d) {{
                                    if (!event.active) simulation.alphaTarget(0);
                                    d.fx = null;
                                    d.fy = null;
                                }}

                                // Resize the SVG when the window is resized
                                window.addEventListener('resize', () => {{
                                    const width = container.clientWidth;
                                    const height = container.clientHeight;
                                    svg.attr('width', width).attr('height', height);
                                    simulation.force('center', d3.forceCenter(width / 2, height / 2));
                                    simulation.alpha(1).restart();
                                }});
                            </script>
                        </body>
                        </html>
                        """

                        # Display the HTML content in Streamlit
                        components.html(html_code, width=1024, height=800)
                    else:
                        st.write("No data available for the selected parameters.")
                else:
                    st.error("Failed to retrieve data from the API or no response data available.", icon="🔥")

            # Display explanation
            st.sidebar.subheader("Graphs Explanation")
            st.sidebar.write(TASK_DESCRIPTIONS[task_key])

    if __name__ == "__main__":
        obj = GraphChatbot()
        obj.main()

else:
    st.error("Failed to load the configuration. Please try again later.", icon="🔥")