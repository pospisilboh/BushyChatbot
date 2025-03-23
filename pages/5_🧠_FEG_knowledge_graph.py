import utils
import streamlit as st
import pandas as pd

import pygwalker as pyg
from pygwalker.api.streamlit import StreamlitRenderer

import bushy_client as bc

st.set_page_config(page_title="FEG Knowledge graph", page_icon="🧠", layout="wide")
st.header('🧠FEG Knowledge graph')
st.write('Allows users to interact with the FEG')

# Retrieve and load the task configuration
config_name = "kg"
config = bc.get_config_from_server_cached(config_name)

if config and config_name in config:
    TASK_DEFINITIONS = config
    TASK_KEYS = TASK_DEFINITIONS[config_name].keys()
    TASK_PARAMETERS = {k: v['params'] for k, v in TASK_DEFINITIONS[config_name].items()}
    TASK_NAMES = {k: v['name'] for k, v in TASK_DEFINITIONS[config_name].items()}
    TASK_DESCRIPTIONS = {k: v['description'] for k, v in TASK_DEFINITIONS[config_name].items()}
    TASK_KEYS_TO_NAMES = {v['name']: k for k, v in TASK_DEFINITIONS[config_name].items()}
    TASK_FILES = {k: v['file'] for k, v in TASK_DEFINITIONS[config_name].items()}

    class GraphChatbot:

        def __init__(self):
            utils.sync_st_session()
            self.df = pd.DataFrame()

        def main(self):
            st.sidebar.header("Knowledge graph")
            name = st.sidebar.radio("Select Knowledge graph:", sorted(list(TASK_KEYS_TO_NAMES.keys())))

            # Get the corresponding key for the selected description
            task_key = TASK_KEYS_TO_NAMES[name]

            # Display input fields based on selected task
            parameters = TASK_PARAMETERS[task_key]
            inputs = {}
            if parameters:  # Check if there are any parameters
                st.sidebar.header("Knowledge graph Parameters")
                for param in parameters:
                    inputs[param] = st.sidebar.text_input(param.capitalize().replace('_', ' '), placeholder=f"Enter {param}")

            st.write("## Knowledge graph")

            # Button to generate report
            if st.sidebar.button("Show Knowledge Graph"):
                # Display the selected option
                st.chat_message('user').write(TASK_NAMES[task_key])

                st.image(TASK_FILES[task_key], use_container_width=True)

                # Display explanation
                # st.subheader("Knowledge graph Explanation")
                st.markdown(TASK_DESCRIPTIONS[task_key])

    if __name__ == "__main__":
        obj = GraphChatbot()
        obj.main()

else:
    st.error("Failed to load the configuration. Please try again later.", icon="🔥")