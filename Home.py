import streamlit as st
from PIL import Image
from pathlib import Path
import time
from PageHelper import process_data_prompt, initialize_session_state
from UIFragements import show_output
from final_schemas import GameDesignSchema 
import final_game_service as final_game_service

st.set_page_config(
    page_title="Game Story Generator App" ,
    page_icon=":slot_machine:"
)

original_title = '<label style="font-family:Courier; color:Blue; font-size: xx-large; font-weight: bold;">Generate Game Story</label>'
st.markdown(original_title, unsafe_allow_html=True)

initialize_session_state()

def clear_form(): 
  st.session_state["gamedescription"] = ""
  st.session_state["bonusfeaturesoption"] = True
  st.session_state["charactersoption"] = True
  st.session_state["storiesoption"] = True
  st.session_state["symbolsoption"] = True
  st.session_state["visualstyleoption"] = True
  st.session_state.shown_images = set()
  st.session_state.show_story = False

# Folder to watch
IMAGE_DIR = Path("images")
if not IMAGE_DIR.exists():
    IMAGE_DIR.mkdir()

def get_new_images():
    image_files = sorted(IMAGE_DIR.glob("*.png"))  # Can filter for jpg/png if needed
    new_images = []
    for img in image_files:
        if img.name not in st.session_state.shown_images:
            new_images.append(img)
            st.session_state.shown_images.add(img.name)
    return new_images

# Main loop to check for new images
def display_images(image_count):
    index = 0
    while (index < image_count):
        new_images = get_new_images()
        if new_images:
            for img_path in new_images:
            #with placeholder.container():
                #st.image(str(img_path), caption=img_path.name, use_column_width=True)
                img = Image.open(img_path)
                st.image(img, caption=img_path)
                index = index + 1
        time.sleep(1)  # Check every second

resultoutput = "This is the JSON result"

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
    bonusfeaturesoption = st.checkbox("BonusFeatures", key="bonusfeaturesoption")
with checks[4]:
    visualstyleoption = st.checkbox("VisualStyle", key="visualstyleoption")

col1, col2 = st.columns([1, 1])
with col1:
    create = st.button("Create Story")
    if create:
        while True: 
            with st.spinner("Preparing game story. Please wait.", show_time=True):
                result = final_game_service.generate_game_details( st.session_state["gamedescription"],"")
                st.session_state.show_story = True
                break
        
        #st.write(f"**Description:** {gamedescription}")
        #st.write(f"**Result updated** {resultoutput}")
        #process_data_prompt()
        show_output(result)
        #display_images(5)
        #show_output()

with col2:
    reset = st.button("Reset",on_click=clear_form)
    #if reset:
        #st.session_state.show_image = False

# Cache to store already shown images
#if 'shown_images' not in st.session_state:
#     st.session_state.shown_images = set()