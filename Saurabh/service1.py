from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
import os
from langchain.chains import LLMChain
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel
from typing import List, Optional


# -------- SYMBOLS & BONUS --------

class Symbol(BaseModel):
    name: str
    description: str
    payoutMultiplier: int


class Symbols(BaseModel):
    highValue: List[Symbol]
    midValue: List[Symbol]
    lowValue: List[Symbol]


class WildSymbol(BaseModel):
    name: str
    effect: str


class ScatterSymbol(BaseModel):
    name: str
    effect: str


class BonusTriggerSymbol(BaseModel):
    name: str
    effect: str


class BonusFeature(BaseModel):
    name: str
    trigger: str
    description: str
    mechanics: str
    storyIntegration: Optional[str] = None


# -------- GAMEPLAY --------

class Gameplay(BaseModel):
    reels: int
    rows: int
    paylines: int
    symbols: Symbols
    wildSymbol: WildSymbol
    scatterSymbol: ScatterSymbol
    bonusTriggerSymbol: BonusTriggerSymbol
    bonusFeatures: List[BonusFeature]


# -------- CHARACTERS & STORYLINE --------

class Character(BaseModel):
    name: str
    trait: str
    role: str
    symbolType: Optional[str] = None


class Progression(BaseModel):
    unlockableChapters: List[str]
    characterEvolution: str
    shiftingEnvironments: str


class Storyline(BaseModel):
    backstory: str
    mainRole: str
    characters: List[Character]
    conflict: str
    progression: Progression


# -------- VISUALS & AUDIO --------

class VisualStyle(BaseModel):
    backgroundArt: str
    animationIdeas: List[str]
    symbolDesign: str
    uiElements: str


class AudioStyle(BaseModel):
    soundtrack: str
    soundEffects: List[str]
    musicSuggestions: List[str]


# -------- ROOT MODEL --------

class SlotMachineGame(BaseModel):
    slotMachineTitle: str
    storyline: Storyline
    gameplay: Gameplay
    visualStyle: VisualStyle
    audioStyle: AudioStyle



parser = PydanticOutputParser(pydantic_object=SlotMachineGame)
load_dotenv()
print(os.environ.get("GOOGLE_API_KEY"))

llm_model = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-001",
    temperature=0.5
    
)

game_prompt = PromptTemplate(
    input_variables=["input_text"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
    template="""Extract the following information and output it in the specified JSON format:

{format_instructions}
Input:
{input_text}
"""
)


# while(True):
#     inp = input("please provide input: ")

#     if inp.lower() not in  ['q', 'quit', 'bye']:
    
#         print(llm_model.invoke(inp).content)
#     else:
#         break

def invokeGem(role, game_theme,sub_theme):
    
    chain = LLMChain(
    llm=llm_model,
    prompt=game_prompt,
    output_parser=parser,
    verbose=True
)
    formatted_prompt = f"Create a detailed json output storyline-based slot machine concept based on a given {role}, {game_theme}, and {sub_theme}. The slot machine should include an engaging backstory that explains the setting, the central conflict or mission, and how the main role fits into the narrative world. Introduce 2 to 4 main characters, providing their names, traits, and roles within the story—clearly indicating which of them (or what symbols) act as the Wild, Scatter, and Bonus Trigger symbols. Define 10 to 12 reel symbols, broken down into high-value, mid-value, and low-value categories, and ensure they are thematically consistent with the story. Include descriptions of bonus features such as free spins, interactive story choices, or mini-games that tie into the narrative arc or character development. Also describe the visual and audio style, including background art, animation ideas, and soundtrack suggestions that enhance immersion. Optionally, add progression mechanics such as unlockable chapters, evolving characters, or shifting environments that reward continued play and tie back into the unfolding story?"
    return chain.run({"input_text": formatted_prompt})
    #return llm_model.invoke("needs output as json format including field back-story for As a game designer, I want you to develop a [Time Travel online slot game] for [casual and fun-loving gamers].The theme of the game is [Prehistoric era].The players enjoy [the experience of million years ego time of Prehistoric era].Story Setup: The player [initial scenario, e.g., A futuristic Time Lab with glowing gears, holograms, and a time machine interface.] and [core plot event, e.g., he player is sucked into the portal and dropped from the sky into a prehistoric jungle].As the game progresses through [main mechanic, e.g., collecting coins,Bones,Spear, Egg,caves  via spins], the player [progression mechanic, e.g., explores new old animals, characters of that era/time].The game includes [bonus feature types, e.g., Stampede Spins,Volcano Bonus,Chrono Totem Free Spins,Chrono Jackpot etc.] to enhance engagement.The visual tone should be [art style or theme tone, e.g.,  Warped time sounds, alarms, heavy pulses,ungle ambiance, loud dinosaur roar, crashing sound,Tribal drums].The game is designed for [platforms, e.g., both mobile and desktop] with [reel layout, e.g., 4x4 reels].Symbols on the reels should include [symbol theme, coins,Bones,Spear, Egg,caves, thematic items and essentials relevant to the main theme].The narrative and game elements should serve as a guide for slot game development").content


#print(invokeGem("","",""))