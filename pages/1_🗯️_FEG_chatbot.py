import utils
import streamlit as st
import bushy_client as bc

st.set_page_config(page_title="FEG Chatbot", page_icon="🗯️")
st.header('🗯️FEG Chatbot')
st.write('Allows users to interact with the FEG')

# Initialize session state for messages if it does not exist
if 'messages' not in st.session_state:
    st.session_state.messages = []

#if not utils.check_password():
#    st.stop()  # Do not continue if check_password is not True.
 
# Retrieve and load the task configuration
config_name = "chats"
config = bc.get_config_from_server_cached(config_name)

if config and config_name in config:
    TASK_DEFINITIONS = config
    TASK_NAMES = sorted(TASK_DEFINITIONS[config_name].keys())
    TASK_PARAMETERS = TASK_DEFINITIONS[config_name]
    TASK_EXPLANATIONS = TASK_DEFINITIONS['explanations']

    AREA_NAMES = sorted(TASK_DEFINITIONS['areas'].keys())
    BRAND_NAMES = sorted(TASK_DEFINITIONS['brands'].keys())

    class RagChatbot:

        #def __init__(self):
            #utils.sync_st_session()

        #@utils.enable_chat_history
        def main(self):
            st.sidebar.header("Areas")
            area_name= st.sidebar.selectbox("Select area:", AREA_NAMES)

            st.sidebar.header("Brands")
            brand_name= st.sidebar.selectbox("Select brand:", BRAND_NAMES)

            st.sidebar.header("Retrievers")
            task_name = st.sidebar.radio("Select Retriever:", TASK_NAMES)

            # Display explanation and when to use in the sidebar
            st.sidebar.subheader("When to Use")
            st.sidebar.write(TASK_EXPLANATIONS[task_name]["When to Use"])
            st.sidebar.subheader("Retriever Explanation")
            st.sidebar.write(TASK_EXPLANATIONS[task_name]["Explanation"])

            st.write("## Chat")
            user_query = st.chat_input(placeholder="Ask me anything!")
            if user_query:
                utils.display_msg(user_query, 'user')
    
                # Get response from the API
                response_data = bc.get_chat_response(area_name, brand_name, task_name, user_query)
                response_text = response_data.get("response", "No response from server")
                retriever_type = response_data.get("retriever_type", "No retriever_type from server")

                if response_text:
                    # Display the response
                    if retriever_type in ['JiraRetriever', 'CmdbRetriever', 'ArticleRetriever']:
                        # Update the session state messages with the response
                        st.session_state.messages.append({"role": "assistant", "content": response_text['content']})
                        utils.print_qa(RagChatbot, user_query, response_text['content'])
                        st.chat_message("assistant").write(response_text['content'])
                    else:
                        # Update the session state messages with the response
                        st.session_state.messages.append({"role": "assistant", "content": response_text['answer']})
                        utils.print_qa(RagChatbot, user_query, response_text['answer'])
                        st.chat_message("assistant").write(response_text['answer'])

                        ref_title = f":orange[Metadata]"
                        with st.popover(ref_title):
                            metadata = response_text['retriever_result']['metadata']
                            keys_to_check = ['__retriever', 'cypher']
                            for key in keys_to_check:
                                if key in metadata:
                                    st.caption(metadata[key])

                        # Iterate through the items and print the content
                        idx = 1  # Initialize the sequence index
                        for item in response_text['retriever_result']['items']:
                            ref_title = f":blue[Reference {idx}]"  # Use the index in the reference title
                            with st.popover(ref_title):
                                st.caption(item)
                            idx += 1                    

    if __name__ == "__main__":
        obj = RagChatbot()
        obj.main()

else:
    st.error("Failed to load the configuration. Please try again later.", icon="🔥")
