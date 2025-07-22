import streamlit as st
from PIL import Image
from pathlib import Path
import time
from PageHelper import process_data_prompt, initialize_session_state
from UIFragements import show_output
from schemas import GameDesignSchema 
import GameService_azureOpenAI as game_service
import base64

st.set_page_config(
    page_title="Game Story Generator App" ,
    page_icon=":slot_machine:"
)

original_title = '<label style="font-family:Courier; color:#4a4949; font-size: xx-large; font-weight: bold;">Generate Game Story</label>'
st.markdown(original_title, unsafe_allow_html=True)

initialize_session_state()

st.markdown("""
            <style>

            .stCheckbox > label > div > div > div {
                font-size: 0.9rem !important;
            }

            .stMarkdownBadge {
                background-color: lightgrey !important;
                color:#4a4949 !important;
            }
            

            </style>
        """, unsafe_allow_html=True)
def extract_exclude_options():
    story_options = {
           'bonusfeaturesoption': st.session_state["bonusfeaturesoption"], 
           'charactersoption': st.session_state["charactersoption"],
           'storiesoption': st.session_state["storiesoption"],
           'symbolsoption': st.session_state["symbolsoption"],
           'visualstyleoption': st.session_state["visualstyleoption"]}
    mapping_dict ={'visualstyleoption': 'visualstyle', 'charactersoption': 'characters',
               'storiesoption': 'story', 'symbolsoption':'symbols', 'bonusfeaturesoption':'bonusfeatures'}
    exclude_sections=[]
    for key, value  in story_options.items():
        if value is False:
            exclude_sections.append(mapping_dict[key])
    return exclude_sections

def clear_form(): 
  st.session_state["gamedescription"] = ""
  st.session_state["bonusfeaturesoption"] = True
  st.session_state["charactersoption"] = True
  st.session_state["storiesoption"] = True
  st.session_state["symbolsoption"] = True
  st.session_state["visualstyleoption"] = True
  st.session_state.shown_images = set()
  st.session_state.show_story = False

# --- Function to set a local PNG image as the background ---
def set_background(png_file):
    with open(png_file, "rb") as image_file:
        img_bytes = image_file.read()
        encoded = base64.b64encode(img_bytes).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

#set_background("background.png")

#Form widgets
gamedescription = st.text_area("Enter game description", key="gamedescription")

st.badge("Enrich game story with Add-ons")
checks = st.columns(5)
with checks[0]:
    storiesoption = st.checkbox("Core Story", key="storiesoption")
with checks[1]:
    charactersoption = st.checkbox("Characters", key="charactersoption")
with checks[2]:
    symbolsoption = st.checkbox("Symbols", key="symbolsoption")
with checks[3]:
    bonusfeaturesoption = st.checkbox("Bonus Features", key="bonusfeaturesoption")
with checks[4]:
    visualstyleoption = st.checkbox("Visual Style", key="visualstyleoption")

create = st.button("Create Story")

if create:
    while True: 
        with st.spinner("Preparing game story. Please wait.", show_time=True):
            result = game_service.generate_game_details( st.session_state["gamedescription"],extract_exclude_options())
            if result is None:
                st.error("Failed to generate game details. Please try again.")
                st.session_state.show_story = False
                break
            else:
                st.session_state.show_story = True
                break
    show_output(result)