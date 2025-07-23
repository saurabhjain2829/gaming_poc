import streamlit as st
from PIL import Image
from pathlib import Path
import time
from PageHelper import process_data_prompt, initialize_session_state
from UIFragements import show_output
from schemas import GameDesignSchema 
import GameService_azureOpenAI as game_service
import base64
from DatabaseService import init_db, get_all_chats_from_db, save_chat_to_db, load_chat_from_db
from datetime import datetime

st.set_page_config(
    page_title="Game Story Generator App" ,
    page_icon=":slot_machine:"
)

original_title = '<label style="font-family:Courier; color:#4a4949; font-size: xx-large; font-weight: bold;">Generate Game Story</label>'
st.markdown(original_title, unsafe_allow_html=True)

init_db()
initialize_session_state()

DEFAULT_PREVIOUS_STORIES_NAME = "-- Select a Game Story --"
st.markdown("""
            <style>
            .stCheckbox {
                display: none !important;
            }
            .stCheckbox > label > div > div > div {
                font-size: 0.9rem !important;
                display:none !important;
            }

            .stMarkdownBadge {
                background-color: lightgrey !important;
                color:#4a4949 !important;
            }
            

            .stSidebar {
                width: 260px !important;
                padding-right: 8px !important;
                overflow-y: auto !important;
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

def get_story_options() :
    story_options =  {
           'bonusfeaturesoption': st.session_state["bonusfeaturesoption"], 
           'charactersoption': st.session_state["charactersoption"],
           'storiesoption': st.session_state["storiesoption"],
           'symbolsoption': st.session_state["symbolsoption"],
           'visualstyleoption': st.session_state["visualstyleoption"]
           }
    return story_options

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

# ---------- Sidebar Chat Tree ----------
with st.sidebar:
    st.markdown("## Previous Game Stories")
    st.markdown('<div class="sidebar-container">', unsafe_allow_html=True)
    for chat_name in st.session_state.chat_names:
        is_selected = (chat_name == st.session_state.selected_chat)
        btn_class = "chat-button-selected" if is_selected else "chat-button"

        # Truncate label text at 30 characters
        display_name = chat_name.split('_')[0]
        display_name = display_name if len(display_name) <= 30 else display_name[:30] + "..."
        #display_name = chat_name if len(chat_name) <= 30 else chat_name[:30] + "..."
        
        if st.button(f"{display_name}", key=f"chat_{chat_name}", help=f"{chat_name}"):

            input_obj, output_obj = load_chat_from_db(chat_name)

            if (input_obj and output_obj) : 
                st.session_state["gamedescription"] = input_obj["gamedescription"]

                savedStoryOptions = input_obj["storyoptions"]
                st.session_state["bonusfeaturesoption"] = savedStoryOptions['bonusfeaturesoption']
                st.session_state["charactersoption"] = savedStoryOptions['charactersoption']
                st.session_state["storiesoption"] = savedStoryOptions['storiesoption']
                st.session_state["symbolsoption"] = savedStoryOptions['symbolsoption']
                st.session_state["visualstyleoption"] = savedStoryOptions['visualstyleoption']

                st.session_state.show_story = True

                st.session_state.selected_chat = chat_name

                st.session_state.story_output = output_obj

                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

#Form widgets
gamedescription = st.text_area("Enter game description", key="gamedescription")

#st.badge("Enrich game story with Add-ons")
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
        with st.spinner("Generating game story. Please wait.", show_time=True):
            result = game_service.generate_game_details( st.session_state["gamedescription"],extract_exclude_options())
            if result is None:
                st.error("Failed to generate game details. Please try again.")
                st.session_state.show_story = False
                st.session_state.story_output = result
                break
            else:
                input_obj = {
                    "gamedescription": st.session_state["gamedescription"],
                    "storyoptions": get_story_options()
                }
                
                chat_name = result.gameTitle + datetime.now().strftime("_%Y%m%d%H%M%S")
                save_chat_to_db(chat_name, input_obj, result)

                st.session_state.chat_names = [chat_name] + st.session_state.chat_names
                st.session_state.selected_chat = chat_name

                st.session_state.show_story = True

                st.session_state.story_output = result

                st.rerun()

                break

show_output(st.session_state.story_output)