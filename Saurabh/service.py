from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
import os

load_dotenv()
print(os.environ.get("GOOGLE_API_KEY"))

llm_model = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-001",
    temperature=0.0
    
)

game_prompt = PromptTemplate(
    input_variables=["user_input"],
    template= """Instruction:Create a story driven themed slot game concept based on Input Data.
Give Preference to the Input Data.
 
Context:As a game designer , I want to develop a storyline-based slot game concept 
for [casual players].The players love narrative led slot game experience.
The slot game should include an engaging backstory that explains the setting, 
the core story , and how the main role fits into the narrative world.
he tone should be cartoon based adventure. 
The game is aimed for both mobile and desktop. 
The symbols in the reel include thematic items. 
The game includes [bonus feature types, e.g., bonus rounds, special symbols, etc.] 
to enhance engagement.The visual tone should be 
[art style or theme tone, e.g., cartoon-based beach adventure].
The game is designed for [platforms, e.g., both mobile and desktop] 
with [reel layout, e.g., 4x4 reels].Symbols on the reels should include 
[symbol theme, e.g., thematic items and essentials relevant to the main theme].
Infer the main theme from Input Data.
 
**Input Data:** {user_input}
 
**Output Indicator**: Output in JSON format following given JSON schema
 
"""
)

# while(True):
#     inp = input("please provide input: ")

#     if inp.lower() not in  ['q', 'quit', 'bye']:
    
#         print(llm_model.invoke(inp).content)
#     else:
#         break

def invokeGem(user_input):
    formatted_prompt=game_prompt.format(user_input=user_input)
    print(formatted_prompt)
    #return llm_model.invoke(formatted_prompt).content
    

    return llm_model.invoke(formatted_prompt).content
    #return llm_model.invoke("needs output as json format including field back-story for As a game designer, I want you to develop a [Time Travel online slot game] for [casual and fun-loving gamers].The theme of the game is [Prehistoric era].The players enjoy [the experience of million years ego time of Prehistoric era].Story Setup: The player [initial scenario, e.g., A futuristic Time Lab with glowing gears, holograms, and a time machine interface.] and [core plot event, e.g., he player is sucked into the portal and dropped from the sky into a prehistoric jungle].As the game progresses through [main mechanic, e.g., collecting coins,Bones,Spear, Egg,caves  via spins], the player [progression mechanic, e.g., explores new old animals, characters of that era/time].The game includes [bonus feature types, e.g., Stampede Spins,Volcano Bonus,Chrono Totem Free Spins,Chrono Jackpot etc.] to enhance engagement.The visual tone should be [art style or theme tone, e.g.,  Warped time sounds, alarms, heavy pulses,ungle ambiance, loud dinosaur roar, crashing sound,Tribal drums].The game is designed for [platforms, e.g., both mobile and desktop] with [reel layout, e.g., 4x4 reels].Symbols on the reels should include [symbol theme, coins,Bones,Spear, Egg,caves, thematic items and essentials relevant to the main theme].The narrative and game elements should serve as a guide for slot game development").content