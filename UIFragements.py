import streamlit as st
import pandas as pd
import os
from PageHelper import initialize_session_state
from schemas import GameDesignSchema
from schemas import Symbol
from pathlib import Path
import base64
import time
from PIL import Image
import GameUtils as gameUtils
from typing import List, Dict




initialize_session_state()



MAIN_IMAGES_FOLDER_NAME = "images\\"
# Folder to watch
# IMAGE_DIR = Path("images")
# if not IMAGE_DIR.exists():
#     IMAGE_DIR.mkdir()

FOLDER_WATCH_RETRY_MAX_COUNT = 20

def get_gameprogression_section(prompt):
    gameprogression={}
    try:
        if(prompt.story.islandMapProgression):
            gameprogression["Island Map Progression"]=prompt.story.islandMapProgression
        if(prompt.story.souvenirCollection):
            gameprogression["Souvenir Collection"]=prompt.story.souvenirCollection
        if(prompt.story.seasonalEvents):
            gameprogression["Seasonal Events"]=prompt.story.seasonalEvents
        if(prompt.story.achievementBadgesTrophies):
            gameprogression["Achievement Badges & Trophies"]=prompt.story.achievementBadgesTrophies
        if(prompt.story.progressiveJackpot):
            gameprogression["Progressive Jackpot"]=prompt.story.progressiveJackpot
        return "\n".join([f"- **{key}:** {value}" for key, value in gameprogression.items()])
    except Exception as e:
        print(f'Something went wrong: method: get_gameprogression_section : {e}')
        return ""

def get_new_images(imagesToRender,gameTitle: str):
    
    IMAGE_DIR = Path(gameUtils.create_directory_name(gameTitle,"images"))
    if not IMAGE_DIR.exists():
        IMAGE_DIR.mkdir()


    image_files = sorted(IMAGE_DIR.glob("*.png"))  # Can filter for jpg/png if needed
    new_images = []
    for img in image_files:
        if ((img.name in imagesToRender) and (img.name not in st.session_state.shown_images)):
            new_images.append(img)
            st.session_state.shown_images.add(img.name)

    return new_images

# # Main loop to check for new images
# def display_images(image_count):
#     index = 0
#     while (index < image_count):
#         new_images = get_new_images()
#         if new_images:
#             for img_path in new_images:
#                 img = Image.open(img_path)
#                 st.image(img, caption=img_path)
#                 index = index + 1
#         time.sleep(1)  # Check every second

# Function to convert a local image to a Base64 string
def get_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def process_symbols(symbolsList: List[Symbol] ,gameTitle: str ):
    totalSymbols = len(symbolsList)
    SymbolsImagesPath = []
    SymbolsPathDescDict = {}
    for i in range(totalSymbols):
        imageName = symbolsList[i].name.replace(' ', '_') + ".png"
        SymbolsImagesPath.append(imageName)
        SymbolsPathDescDict[imageName] = symbolsList[i].description
        
    index = 0
    maxRetryCount = (FOLDER_WATCH_RETRY_MAX_COUNT * totalSymbols)
    retryCount = 0
    while ((index < totalSymbols) and (retryCount < maxRetryCount)):
        new_images = get_new_images(SymbolsImagesPath,gameTitle)
        if new_images:
            for img_path in new_images:
                img = Image.open(img_path)
                imgName = img_path.name.replace('_', ' ')
                imgName = imgName.replace('.png','')


                # Custom CSS to apply flexbox for equal height and border to col1
                st.markdown(
                    """
                    <style>
                    .stContainer > div > div {
                        display: flex;
                        align-items: stretch; /* Ensures columns stretch to equal height */
                    }
                    .stContainer .col1-bordered {
                        border: 2px solid #ccc;
                        border-radius: 10px;
                        padding: 10px; /* Add some padding inside the border */
                        display: flex; /* Use flex to vertically center image if needed */
                        align-items: center; /* Center image vertically within its bordered column */
                        justify-content: center; /* Center image horizontally within its bordered column */
                    }
                    </style>
                    """,
                    unsafe_allow_html=True
                )

                # inside your loop after getting each img_path
                with st.container():                                   
                    col1, col2 = st.columns([1, 3])

                    with col1:
                        # Apply a custom class to this column to add the border via CSS
                        encoded_image = get_image_base64(img_path)
                        image_data_url = f"data:image/png;base64,{encoded_image}" # Assuming PNG, adjust if needed
                        
                        st.markdown(
                            f"""
                            <div class="col1-bordered" style="padding: 10px; border: 2px solid #ccc; border-radius: 10px; height: 160px;">
                                <img src="{image_data_url}" style="width: auto; height: auto; display: block;">
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    with col2:
                        st.markdown(
                            f"""
                            <div style="padding: 10px; border: 2px solid #ccc; border-radius: 10px; height: 160px;">
                                <p style="margin: 0;"><strong>{imgName}</strong></p>
                                <p style="margin: 0;">{SymbolsPathDescDict.get(img_path.name)}</p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                index = index + 1
                #break
        time.sleep(1)
        retryCount += 1
        #break
    
    st.session_state.shown_images = set()                 



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
            
            .stMarkdownColoredText {
                font-size: xx-large !important;
                font-style: italic !important;
                color: #4a4949 !important; 
            }
        
             /* Style for internal expander headers (Subsection titles) */
            details[open] > summary {
                font-weight: bold;
                color: grey;
            }
            
            details[open] > summary > span > div {
                font-size: x-large !important;
            }
            .internal-expander-header {
                font-weight: bold;
                color: brown;
            }

            /* Section 3 and 5 grid styling */
            .stDataFrame {
                border: 2px solid green !important;
            }
            
            .stCheckbox > label > div > div > div {
                font-size: 0.9rem !important;
            }
            
            .stCheckbox {
                font-size: 0.9rem !important;
            }

            /* Style for image borders in Section 5 */
            .image-border {
                border: 5px solid red !important;
                padding: 10px;
            }
                    
            .custom-table {
                border-collapse: collapse;
                width: 100%;
                border: 2px solid black;
            }
            
            .custom-table th, .custom-table td {
                border: 2px solid black;
                text-align: left;
                padding: 8px;
                vertical-align: top;
            }
            
            .custom-table th {
                background-color: brown; /* Light brown */
            }
            
            </style>
        """, unsafe_allow_html=True)

        # Section 1 - tittle
        st.write(f":grey[{prompt.gameTitle}]")

        # New Section 2 - Game Story
        if st.session_state['storiesoption']:

            with st.expander("**Core Story**", expanded=True):
                # Subsection 1
                if prompt.story and prompt.story.summary:
                 with st.expander("**Summary**", expanded=True):
                    st.markdown(prompt.story.summary)
        
                # Subsection 2
                if prompt.story and prompt.story.gameplay:
                 with st.expander("**Game Play**", expanded=True):
                    st.markdown(prompt.story.gameplay)
                    st.markdown(get_gameprogression_section(prompt))
                    if prompt.story and prompt.story.monetizationStrategy:
                        st.markdown("**Monetization Strategy**")
                        st.markdown(prompt.story.monetizationStrategy)

                # Subsection 3
                if prompt.story.setting and prompt.story.setting.location:
                    with st.expander("**Location**", expanded=True):
                        st.markdown(prompt.story.setting.location)

                # Subsection 4
                if prompt.story.setting and prompt.story.setting.worldStyle:
                 with st.expander("**WorldStyle**", expanded=True):
                    st.markdown(prompt.story.setting.worldStyle)

        # Section 3 - Visual Style
        if st.session_state['visualstyleoption']: 
            if prompt.visualStyle and prompt.visualStyle.artStyle:
                with st.expander("**VisualStyle**", expanded=True):
                    st.markdown(prompt.visualStyle.artStyle)  

        # New Section 4 - Bonus Features
        if st.session_state['bonusfeaturesoption']:

            with st.expander("**Bonus Features**", expanded=True):
                def section(title, kv_data: dict, color="#f5f5f5"):
                    st.markdown(
                        f"""
                        <div style="border: 1px solid #ccc; background-color: {color}; border-radius: 8px; padding: 16px; margin-bottom: 20px;">
                        <h6 style="color:grey;">{title}</h6>
                        <ul>
                            {''.join([f"<li><b>{k}:</b> {v}</li>" for k, v in kv_data.items()])}
                        </ul>
                        </div>
                        """, unsafe_allow_html=True
                    )

                # Subsection 1
                totalBonusFeatures = len(prompt.bonusFeatures)
                for i in range(totalBonusFeatures):
                        section(f"{prompt.bonusFeatures[i].type}", {
                                "Name": f" {prompt.bonusFeatures[i].name}",
                                "Description": f" {prompt.bonusFeatures[i].description}",
                                "Triggered By": f" {prompt.bonusFeatures[i].trigger}"
                                })
                        
        # New Section 4 - Characters Features
        if st.session_state['charactersoption']:
            with st.expander("**Characters**", expanded=True):
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
                    maxRetryCount = (FOLDER_WATCH_RETRY_MAX_COUNT * totalCharacters)
                    retryCount = 0
                    while ((index < totalCharacters) and (retryCount < maxRetryCount)):
                        new_images = get_new_images(characterImagesPath,prompt.gameTitle)
                        if new_images:
                            for img_path in new_images:
                                img = Image.open(img_path)
                                imgName = img_path.name.replace('_', ' ')
                                imgName = imgName.replace('.png','')


                                # Custom CSS to apply flexbox for equal height and border to col1
                                st.markdown(
                                    """
                                    <style>
                                    .stContainer > div > div {
                                        display: flex;
                                        align-items: stretch; /* Ensures columns stretch to equal height */
                                    }
                                    .stContainer .col1-bordered {
                                        border: 2px solid #ccc;
                                        border-radius: 10px;
                                        padding: 10px; /* Add some padding inside the border */
                                        display: flex; /* Use flex to vertically center image if needed */
                                        align-items: center; /* Center image vertically within its bordered column */
                                        justify-content: center; /* Center image horizontally within its bordered column */
                                    }
                                    </style>
                                    """,
                                    unsafe_allow_html=True
                                )

                                # inside your loop after getting each img_path
                                with st.container():                                   
                                    col1, col2 = st.columns([1, 3])

                                    with col1:
                                        # Apply a custom class to this column to add the border via CSS
                                        encoded_image = get_image_base64(img_path)
                                        image_data_url = f"data:image/png;base64,{encoded_image}" # Assuming PNG, adjust if needed
                                        
                                        st.markdown(
                                            f"""
                                            <div class="col1-bordered" style="padding: 10px; border: 2px solid #ccc; border-radius: 10px; height: 160px;">
                                                <img src="{image_data_url}" style="width: auto; height: auto; display: block;">
                                            </div>
                                            """,
                                            unsafe_allow_html=True
                                        )

                                    with col2:
                                        st.markdown(
                                            f"""
                                            <div style="padding: 10px; border: 2px solid #ccc; border-radius: 10px; height: 160px;">
                                                <p style="margin: 0;"><strong>{imgName}</strong></p>
                                                <p style="margin: 0;">{characterPathDescDict.get(img_path.name)}</p>
                                            </div>
                                            """,
                                            unsafe_allow_html=True
                                        )
                                index = index + 1
                                #break
                        time.sleep(1)
                        retryCount += 1
                        #break
                    
                    st.session_state.shown_images = set()

            # New Section 5 - Symbols Features
        if st.session_state['symbolsoption']:

            with st.expander("**Symbols**", expanded=True):
 
                with st.expander("**HighPay Symbols**", expanded=True):
                    with st.spinner("Loading HighPay Symbols. Please wait.", show_time=True):
                         process_symbols(prompt.symbols.highPaySymbols,prompt.gameTitle)
                         
                with st.expander("**LowPay Symbols**", expanded=True):
                    with st.spinner("Loading LowPay Symbols. Please wait.", show_time=True):
                        process_symbols(prompt.symbols.lowPaySymbols,prompt.gameTitle)
 
                with st.expander("**Royal Symbols**", expanded=True):
                    with st.spinner("Loading Royal Symbols. Please wait.", show_time=True):
                        process_symbols(prompt.symbols.royalSymbols,prompt.gameTitle)
 
                
                with st.expander("**Wild Symbols**", expanded=True):
                    with st.spinner("Loading Wild Symbols. Please wait.", show_time=True):
                        process_symbols(prompt.symbols.wildSymbols,prompt.gameTitle)
 
                with st.expander("**Scatter Symbols**", expanded=True):
                    with st.spinner("Loading Scatter Symbols. Please wait.", show_time=True):
                        process_symbols(prompt.symbols.scatterSymbols,prompt.gameTitle)




                