import streamlit as st
import game_service as myservice
from service1 import SlotMachineGame
import json
# Title
st.title("")

# Input boxes
userInput = st.text_input("User Input")


# Submit button
if st.button("Submit"):
    # Output logic: concatenate inputs (customize as needed)
    result = myservice.invokeGem(userInput)
    
    #data_dict = json.loads(result)

    
    # st.markdown("### Rendered Output:")
    # st.markdown(f"Game Titile: {result.slotMachineTitle}")
    # st.markdown(f"Storyline: {result.storyline.backstory}")
    # st.markdown("## High Value Symbols:")
    # for symbol in result.gameplay.symbols.highValue:
    #     st.markdown(symbol)
    
    # for symbol in result.gameplay.symbols.midValue:
    #     st.markdown(symbol)
    
    # for symbol in result.gameplay.symbols.lowValue:
    #     st.markdown(symbol)
    st.markdown(result, unsafe_allow_html=True)