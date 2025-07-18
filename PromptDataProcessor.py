import streamlit as st

def process_data(story_options, gameDescriptionPrompt):
        st.write(f"**Description:** {gameDescriptionPrompt}")
        st.write(f"VisualStyle: {story_options['visualstyleoption']}")
        st.write(f"Characters: {story_options['charactersoption']}")
        st.write(f"Stories: {story_options['storiesoption']}")
        st.write(f"Symbols: {story_options['symbolsoption']}")
        st.write(f"Symbols: {story_options['bonusfeaturesoption']}")