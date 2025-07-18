import streamlit as st
import pandas as pd
import os
from PageHelper import initialize_session_state
from final_schemas import GameDesignSchema 
from pathlib import Path
import time
from PIL import Image

initialize_session_state()

# Folder to watch
IMAGE_DIR = Path("images")
if not IMAGE_DIR.exists():
    IMAGE_DIR.mkdir()

def get_new_images(imagesToRender):
    image_files = sorted(IMAGE_DIR.glob("*.png"))  # Can filter for jpg/png if needed
    new_images = []
    for img in image_files:
        if ((img.name in imagesToRender) and (img.name not in st.session_state.shown_images)):
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
                img = Image.open(img_path)
                st.image(img, caption=img_path)
                index = index + 1
        time.sleep(1)  # Check every second


# Customizing the expander widget with pink borders, blue bold headers, and ensuring expanders are opene

def show_output(prompt): 
    if st.session_state.show_story:
        st.markdown("""
            <style>
            /* Style to make the expander widget open by default */
            details[open] > summary {
                font-weight: bold;
                color: blue;
            }
            .st-expanderHeader {
                font-weight: bold;
                color: blue;
            }
            .st-expanderHeader:hover {
                cursor: pointer;
            }
            .st-expanderHeader > div {
                font-weight: bold;
                color: blue;
            }
            .stExpander > div {
                border: 2px solid pink !important;
            }
            .stDataFrame {
                border: 2px solid red;
            }
        
             /* Style for internal expander headers (Subsection titles) */
            details[open] > summary {
                font-weight: bold;
                color: brown;
            }
            .internal-expander-header {
                font-weight: bold;
                color: brown;
            }

            /* Section 3 and 5 grid styling */
            .stDataFrame {
                border: 2px solid green !important;
            }

            /* Style for image borders in Section 5 */
            .image-border {
                border: 2px solid red;
                padding: 10px;
            }
            </style>
        """, unsafe_allow_html=True)

        # Expander widget with five sections (all open by default)

        # Section 1 - Paragraph Text
        with st.expander(":dart: **Game Title**", expanded=True):
        #with st.expander("📄 **Section 1: Game Title**", expanded=True):
            st.markdown(prompt.gameTitle)

        # New Section 2 - Game Story
        if st.session_state['storiesoption']:

            with st.expander(":palm_tree: **Core Story**", expanded=True):
                # Subsection 1
                with st.expander("**Summary**", expanded=True):
                    st.markdown(prompt.story.summary)
        
                # Subsection 2
                with st.expander("**Game Play**", expanded=True):
                    st.markdown(prompt.story.gameplay)
        
                # Subsection 3
                with st.expander("**Location**", expanded=True):
                    st.markdown(prompt.story.setting.location)

                # Subsection 4
                with st.expander("**WorldStyle**", expanded=True):
                    st.markdown(prompt.story.setting.worldStyle)

        # Section 3 - Visual Style
        if st.session_state['visualstyleoption']: 
            with st.expander(":dart: **VisualStyle**", expanded=True):
                st.markdown(prompt.visualStyle.artStyle)  

        # New Section 4 - Bonus Features
        if st.session_state['bonusfeaturesoption']:

            with st.expander(":ferris_wheel: **Bonus Features**", expanded=True):
                # Subsection 1
                totalBonusFeatures = len(prompt.bonusFeatures)
                for i in range(totalBonusFeatures):
                    with st.expander(f":dancer: **{prompt.bonusFeatures[i].type}**", expanded=False):
                        st.markdown(f"**Name:** {prompt.bonusFeatures[i].name}")
                        st.markdown(f"**Description:** {prompt.bonusFeatures[i].description}")
                        st.markdown(f"**Triggered By:**  {prompt.bonusFeatures[i].trigger}")

                # Subsection 2
                #with st.expander(":ferris_wheel: **Bonus Wheel**", expanded=False):
                 #   st.markdown(f"**Name:** {prompt.bonusFeatures[1].name}")
                  #  st.markdown(f"**Description:** {prompt.bonusFeatures[1].description}")
                  #  st.markdown(f"**Triggered By:**  {prompt.bonusFeatures[1].trigger}")
        
                # Subsection 3
                #with st.expander(":dancer: **Respin features**", expanded=False):
                 #   st.markdown(f"**Name:** {prompt.bonusFeatures[2].name}")
                 #   st.markdown(f"**Description:** {prompt.bonusFeatures[2].description}")
                 #   st.markdown(f"**Triggered By:**  {prompt.bonusFeatures[2].trigger}")
                
        # New Section 4 - Characters Features
        if st.session_state['charactersoption']:
            with st.expander(":crown: **Characters:**", expanded=True):
            # Make sure you put your local image paths here
                with st.spinner("Loading Characters. Please wait.", show_time=True):
                    totalCharacters = len(prompt.characters)
                    characterImagesPath = []
                    characterPathDescDict = {}
                    for i in range(totalCharacters):
                        imageName = prompt.characters[i].name.replace(' ', '_') + ".png"
                        characterImagesPath.append(imageName)
                        characterPathDescDict[imageName] = prompt.characters[i].description
                        
                    index = 0
                    while (index < totalCharacters):
                        new_images = get_new_images(characterImagesPath)
                        if new_images:
                            for img_path in new_images:
                                img = Image.open(img_path)
                                st.image(img)
                                img = Image.open(img_path)
                                st.write(characterPathDescDict.get(img_path.name))
                                index = index + 1
                                break
                        time.sleep(1) 
                        break
                    
                    #for i in range(len(prompt.characters)):
                        #imagepath = "images/" + prompt.characters[i].name + ".png"
                        #if os.path.exists(imagepath):
                            #st.image(imagepath, caption=prompt.characters[i].name)
                            #st.write(prompt.characters[i].description)

            # New Section 5 - Symbols Features
        if st.session_state['symbolsoption']:

            with st.expander(":symbols: **Symbols**", expanded=True):

                with st.expander(":gear: **RegularSymbols**", expanded=False):
                    with st.spinner("Loading RegularSymbols. Please wait.", show_time=True):
                        totalRegularSymbols = len(prompt.symbols.regularSymbols)
                        regularSymbolsImagesPath = []
                        regularSymbolsPathDescDict = {}
                        for i in range(totalRegularSymbols):
                            imageName = prompt.symbols.regularSymbols[i].name.replace(' ', '_')  + ".png"
                            regularSymbolsImagesPath.append(imageName)
                            regularSymbolsPathDescDict[imageName] = prompt.symbols.regularSymbols[i].description
                        
                        index = 0
                        while (index < totalRegularSymbols):
                            new_images = get_new_images(regularSymbolsImagesPath)
                            if new_images:
                                for img_path in new_images:
                                    img = Image.open(img_path)
                                    st.image(img)
                                    img = Image.open(img_path)
                                    st.write(regularSymbolsPathDescDict.get(img_path.name))
                                    index = index + 1
                                    #break
                            time.sleep(1) 
                            #break

                with st.expander(":atom_symbol: **SpecialSymbols**", expanded=False):
                    with st.spinner("Loading SpecialSymbols. Please wait.", show_time=True):
                        totalSpecialSymbols = len(prompt.symbols.specialSymbols)
                        specialSymbolsImagesPath = []
                        specialSymbolsPathDescDict = {}
                        for i in range(totalSpecialSymbols):
                            imageName = prompt.symbols.specialSymbols[i].name.replace(' ', '_')  + ".png"
                            specialSymbolsImagesPath.append(imageName)
                            specialSymbolsPathDescDict[imageName] = prompt.symbols.specialSymbols[i].description
                        
                        index = 0
                        while (index < totalSpecialSymbols):
                            new_images = get_new_images(specialSymbolsImagesPath)
                            if new_images:
                                for img_path in new_images:
                                    img = Image.open(img_path)
                                    st.image(img)
                                    img = Image.open(img_path)
                                    st.write(specialSymbolsPathDescDict.get(img_path.name))
                                    index = index + 1
                                   # break
                            time.sleep(1)
                            #break 