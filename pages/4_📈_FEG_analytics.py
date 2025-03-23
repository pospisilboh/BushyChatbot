import utils
import streamlit as st
import pandas as pd
import uuid

import pygwalker as pyg
from pygwalker.api.streamlit import StreamlitRenderer

import bushy_client as bc

st.set_page_config(page_title="FEG analytics", page_icon="📈", layout="wide")
st.header('📈FEG analytics')
st.write('Allows users to interact with the FEG')

# Retrieve and load the task configuration
config_name = "analytics"
config = bc.get_config_from_server_cached(config_name)

if config and config_name in config:
    TASK_DEFINITIONS = config
    TASK_KEYS = TASK_DEFINITIONS[config_name].keys()
    TASK_PARAMETERS = {k: v['params'] for k, v in TASK_DEFINITIONS[config_name].items()}
    TASK_NAMES = {k: v['name'] for k, v in TASK_DEFINITIONS[config_name].items()}
    TASK_DESCRIPTIONS = {k: v['description'] for k, v in TASK_DEFINITIONS[config_name].items()}
    TASK_KEYS_TO_NAMES = {v['name']: k for k, v in TASK_DEFINITIONS[config_name].items()}
    TASK_VIZ_SPECS = {k: v['vis_spec'] for k, v in TASK_DEFINITIONS[config_name].items()}

    class GraphChatbot:

        def __init__(self):
            utils.sync_st_session()
            self.df = pd.DataFrame()

        def main(self):
            st.sidebar.header("Analytics")
            name = st.sidebar.radio("Select Analytics:", sorted(list(TASK_KEYS_TO_NAMES.keys())))

            # Get the corresponding key for the selected description
            task_key = TASK_KEYS_TO_NAMES[name]

            # Display input fields based on selected task
            parameters = TASK_PARAMETERS[task_key]
            inputs = {}
            if parameters:  # Check if there are any parameters
                st.sidebar.header("Analytics Parameters")
                for param in parameters:
                    inputs[param] = st.sidebar.text_input(param.capitalize().replace('_', ' '), placeholder=f"Enter {param}")

            st.write("## Analytics")

            # Button to generate report
            if st.sidebar.button("Generate analytics"):
                # Display the selected option
                st.chat_message('user').write(TASK_NAMES[task_key])

                # Get response from the API
                response_data = bc.get_analytics_response_cached(task_key, inputs)
                
                if response_data and 'response' in response_data:
                    # Convert the JSON response to a DataFrame
                    self.df = pd.DataFrame(response_data['response'])
                    
                    if not self.df.empty:
                        with st.form(key=str(uuid.uuid4())):
                            pyg_app = StreamlitRenderer(self.df, spec=TASK_VIZ_SPECS[task_key])
                            pyg_app.explorer()
                            st.form_submit_button(disabled=False)
                    else:
                        st.write("No data available for the selected parameters.")
                else:
                    st.error("Failed to retrieve data from the API or no response data available.", icon="🔥")

            # Display explanation
            st.sidebar.subheader("Analytics Explanation")
            st.sidebar.write(TASK_DESCRIPTIONS[task_key])

    if __name__ == "__main__":
        obj = GraphChatbot()
        obj.main()

else:
    st.error("Failed to load the configuration. Please try again later.", icon="🔥")