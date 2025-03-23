import utils
import streamlit as st
import bushy_client as bc

st.set_page_config(page_title="FEG Tasks", page_icon="✅", layout="wide")
st.header('✅FEG Tasks')
st.write('Allows users to interact with the FEG')

# Initialize session state for messages if it does not exist
# if 'messages' not in st.session_state:
#     st.session_state.messages = []

# Retrieve and load the task configuration
config_name = "tasks"
config = bc.get_config_from_server_cached(config_name)

if config and config_name in config:
    TASK_DEFINITIONS = config
    TASK_KEYS = TASK_DEFINITIONS[config_name].keys()
    TASK_PARAMETERS = {k: v['params'] for k, v in TASK_DEFINITIONS[config_name].items()}
    TASK_NAMES = {k: v['name'] for k, v in TASK_DEFINITIONS[config_name].items()}
    TASK_DESCRIPTIONS = {k: v['description'] for k, v in TASK_DEFINITIONS[config_name].items()}
    TASK_KEYS_TO_NAMES = {v['name']: k for k, v in TASK_DEFINITIONS[config_name].items()}

    class TaskBot:

        def __init__(self):
            utils.sync_st_session()

        def main(self):
            st.sidebar.header("Tasks")
            name = st.sidebar.radio("Select Task:", sorted(list(TASK_KEYS_TO_NAMES.keys())))

            # Get the corresponding key for the selected description
            task_key = TASK_KEYS_TO_NAMES[name]

            # Display input fields based on selected task
            parameters = TASK_PARAMETERS[task_key]
            inputs = {}
            if parameters:  # Check if there are any parameters
                st.sidebar.header("Task Parameters")
                for param in parameters:
                    inputs[param] = st.sidebar.text_input(param.capitalize().replace('_', ' '), placeholder=f"Enter {param}")

            st.write("## Task")

            if st.sidebar.button("Submit"):
                # Display the selected option
                st.chat_message('user').write(TASK_NAMES[task_key])
                # utils.display_msg(task_name, 'user')

                # Get response from the API
                response_text = bc.get_task_response_cached(task_key, inputs)

                if response_text:
                    st.chat_message('assistant').write("### Task Results", )

                    # Display the response in markdown format
                    st.markdown(response_text)

            # Display description
            st.sidebar.subheader("Task Description")
            st.sidebar.write(TASK_DESCRIPTIONS[task_key])

    if __name__ == "__main__":
        obj = TaskBot()
        obj.main()

else:
    st.error("Failed to load the configuration. Please try again later.", icon="🔥")