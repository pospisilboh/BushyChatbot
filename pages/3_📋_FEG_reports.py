import utils
import streamlit as st
import pandas as pd
import bushy_client as bc

st.set_page_config(page_title="FEG Reports", page_icon="📋", layout="wide")
st.header('📋FEG Reports')
st.write('Allows users to interact with the FEG')

# Retrieve and load the task configuration
config_name = "reports"
config = bc.get_config_from_server_cached(config_name)

if config and config_name in config:
    TASK_DEFINITIONS = config
    TASK_KEYS = TASK_DEFINITIONS[config_name].keys()
    TASK_PARAMETERS = {k: v['params'] for k, v in TASK_DEFINITIONS[config_name].items()}
    TASK_NAMES = {k: v['name'] for k, v in TASK_DEFINITIONS[config_name].items()}
    TASK_DESCRIPTIONS = {k: v['description'] for k, v in TASK_DEFINITIONS[config_name].items()}
    TASK_KEYS_TO_NAMES = {v['name']: k for k, v in TASK_DEFINITIONS[config_name].items()}

    class ReportChatbot:
        def __init__(self):
            utils.sync_st_session()

        def main(self):
            st.sidebar.header("Reports")
            name = st.sidebar.radio("Select Report:", sorted(list(TASK_KEYS_TO_NAMES.keys())))

            # Get the corresponding key for the selected description
            task_key = TASK_KEYS_TO_NAMES[name]

            # Display input fields based on selected task
            parameters = TASK_PARAMETERS[task_key]
            inputs = {}
            if parameters:  # Check if there are any parameters
                st.sidebar.header("Report Parameters")
                for param in parameters:
                    inputs[param] = st.sidebar.text_input(param.capitalize().replace('_', ' '), placeholder=f"Enter {param}")

            st.write("## Report")

            # Button to generate report
            if st.sidebar.button("Generate Report"):
                # Display the selected option
                st.chat_message('user').write(TASK_NAMES[task_key])

                # Get response from the API
                response_data = bc.get_report_response_cached(task_key, inputs)

                if response_data:
                    # Display the response in a table
                    st.chat_message('assistant').write("### Report Results")

                    # Convert the JSON response to a DataFrame
                    df = pd.DataFrame(response_data['response'])

                    # Display the DataFrame in a Streamlit table
                    # st.table(df)

                    st.dataframe(df, use_container_width=True)

            # Display explanation
            st.sidebar.subheader("Report Explanation")
            st.sidebar.write(TASK_DESCRIPTIONS[task_key])

    if __name__ == "__main__":
        obj = ReportChatbot()
        obj.main()
else:
    st.error("Failed to load the configuration. Please try again later.", icon="🔥")