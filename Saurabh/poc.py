import streamlit as st
import service as myservice
from service1 import SlotMachineGame

# Title
st.title("")

# Input boxes
role = st.text_input("role")
game_theme = st.text_input("game theme")
sub_theme = st.text_input("sub theme")


# Submit button
if st.button("Submit"):
    # Output logic: concatenate inputs (customize as needed)
    result = myservice.invokeGem(role, game_theme,sub_theme)
    
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