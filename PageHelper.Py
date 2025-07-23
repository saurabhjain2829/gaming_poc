import streamlit as st
from PromptDataProcessor import process_data
from DatabaseService import get_all_chats_from_db

def initialize_session_state(): 
    if "gamedescription" not in st.session_state:
        st.session_state["gamedescription"] = ""
        st.session_state["bonusfeaturesoption"] = True
        st.session_state["charactersoption"] = True
        st.session_state["storiesoption"] = True
        st.session_state["symbolsoption"] = True
        st.session_state["visualstyleoption"] = True
        st.session_state.shown_images = set()
        st.session_state.show_story = False
        st.session_state.table_data = []
        st.session_state.chat_names = get_all_chats_from_db()
        st.session_state.selected_chat = None
        st.session_state.story_output = None

initialize_session_state()

#Dictionary of story options
story_options = {
           'bonusfeaturesoption': st.session_state["bonusfeaturesoption"], 
           'charactersoption': st.session_state["charactersoption"],
           'storiesoption': st.session_state["storiesoption"],
           'symbolsoption': st.session_state["symbolsoption"],
           'visualstyleoption': st.session_state["visualstyleoption"]}

#Function to prompt processor
def process_data_prompt():
        process_data(story_options, st.session_state["gamedescription"])

