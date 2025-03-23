import streamlit as st
#import utils

#if not utils.check_password():
#    st.stop() # Do not continue if check_password is not True.

st.set_page_config(
    page_title="Bushy",
    page_icon='💬',
    layout='wide',
)

st.header("Bushy Assistant")
st.image("bushy.png", width=150)

st.write("""
Here are a few examples of chatbot implementations catering to different use cases:

- **🗯️FEG Chatbot**: Engage in interactive conversations with the LLM within the FEG system.
- **✅FEG Tasks**: Capable of fulfilling various defined tasks within the FEG system.         
- **📋FEG Reports**: Generate and view reports on various aspects of operations and performance within FEG.   
- **📈FEG Analytics**: Analyze and visualize various aspects of operations and performance within FEG through interactive charts.
- **🧠FEG Knowledge graph**: A comprehensive representation of all relevant entities and their interconnections within the FEG ecosystem.  
- **💬Basic Chatbot**: Engage in interactive conversations with the LLM.
- **🌐Chatbot with Internet Access**: An internet-enabled chatbot capable of answering user queries about recent events.
- **📄Chat with your documents**: Enable the chatbot to access custom documents to answer user queries based on that information.
- **🛢Chat with SQL database**: Enable the chatbot to interact with a SQL database through simple, conversational commands.
- **🔗Chat with Websites**: Enable the chatbot to interact with website contents.

To explore usage of each, please navigate to the corresponding section.
""")