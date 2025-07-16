from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
import os
from langchain.chains import LLMChain
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel
from typing import List, Optional


from typing import List
from pydantic import BaseModel


class SymbolEffect(BaseModel):
    name: str
    effect: str


class SpecialSymbols(BaseModel):
    WildSymbol: SymbolEffect
    ScatterSymbol: SymbolEffect
    BonusSymbol: SymbolEffect


class ReelSymbols(BaseModel):
    regularSymbols: List[str]
    specialSymbols: SpecialSymbols


class Setting(BaseModel):
    location: str
    worldStyle: str


class Backstory(BaseModel):
    summary: str
    mainCharacter: str
    supportingCharacters: List[str]


class BonusFeature(BaseModel):
    name: str
    trigger: str
    description: str


class VisualStyle(BaseModel):
    artStyle: str
    animation: str
    audio: str


class GameLoop(BaseModel):
    baseGame: str
    metaProgression: str


class UserExperience(BaseModel):
    UXFocus: str
    Accessibility: str


class GameDesignSchema(BaseModel):
    gameTitle: str
    theme: str
    platforms: List[str]
    reelLayout: str
    targetAudience: str
    tone: str
    setting: Setting
    backstory: Backstory
    reelSymbols: ReelSymbols
    bonusFeatures: List[BonusFeature]
    visualStyle: VisualStyle
    gameLoop: GameLoop
    userExperience: UserExperience



parser = PydanticOutputParser(pydantic_object=GameDesignSchema)
load_dotenv()
print(os.environ.get("GOOGLE_API_KEY"))

llm_model = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-001",
    temperature=0.0
    
)

game_prompt = PromptTemplate(
    input_variables=["input_text"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
    template="""**Instruction:**
    Create a story driven themed slot game concept based on Input Data.
    Give Preference to the Input Data.
    Consider players nature from Input Data if available
    Consider core story from Input Data if available
    Context:As a game designer , I want to develop a storyline-based slot game concept for players [players type  e.g casual , aggressive].The players love narrative led slot game experience.
    The slot game should include an engaging backstory that explains the setting, the [core story] , and how the main role fits into the narrative world.The [tone] should be cartoon based adventure.
     The game is aimed for [platforms e.g mobile]. The symbols in the reel include thematic items. The game includes [bonus feature types, e.g., bonus rounds, special symbols, etc.] to enhance engagement.The visual tone should be [art style or theme tone, e.g., cartoon-based beach adventure].The game is designed for [platforms, e.g., both mobile and desktop] with [reel layout, e.g., 4x4 reels].Symbols on the reels should include [symbol theme, e.g., thematic items and essentials relevant to the main theme].
    
 

    {format_instructions}
    **Input:**
    {input_text}
    """
)


# while(True):
#     inp = input("please provide input: ")

#     if inp.lower() not in  ['q', 'quit', 'bye']:
    
#         print(llm_model.invoke(inp).content)
#     else:
#         break

def invokeGem(user_input):
    
    chain = LLMChain(
    llm=llm_model,
    prompt=game_prompt,
    output_parser=parser,
    verbose=True
)
    #formatted_prompt = f"Create a detailed json output storyline-based slot machine concept based on a given {role}, {game_theme}, and {sub_theme}. The slot machine should include an engaging backstory that explains the setting, the central conflict or mission, and how the main role fits into the narrative world. Introduce 2 to 4 main characters, providing their names, traits, and roles within the story—clearly indicating which of them (or what symbols) act as the Wild, Scatter, and Bonus Trigger symbols. Define 10 to 12 reel symbols, broken down into high-value, mid-value, and low-value categories, and ensure they are thematically consistent with the story. Include descriptions of bonus features such as free spins, interactive story choices, or mini-games that tie into the narrative arc or character development. Also describe the visual and audio style, including background art, animation ideas, and soundtrack suggestions that enhance immersion. Optionally, add progression mechanics such as unlockable chapters, evolving characters, or shifting environments that reward continued play and tie back into the unfolding story?"
    return chain.run({"input_text": user_input})
    #return llm_model.invoke("needs output as json format including field back-story for As a game designer, I want you to develop a [Time Travel online slot game] for [casual and fun-loving gamers].The theme of the game is [Prehistoric era].The players enjoy [the experience of million years ego time of Prehistoric era].Story Setup: The player [initial scenario, e.g., A futuristic Time Lab with glowing gears, holograms, and a time machine interface.] and [core plot event, e.g., he player is sucked into the portal and dropped from the sky into a prehistoric jungle].As the game progresses through [main mechanic, e.g., collecting coins,Bones,Spear, Egg,caves  via spins], the player [progression mechanic, e.g., explores new old animals, characters of that era/time].The game includes [bonus feature types, e.g., Stampede Spins,Volcano Bonus,Chrono Totem Free Spins,Chrono Jackpot etc.] to enhance engagement.The visual tone should be [art style or theme tone, e.g.,  Warped time sounds, alarms, heavy pulses,ungle ambiance, loud dinosaur roar, crashing sound,Tribal drums].The game is designed for [platforms, e.g., both mobile and desktop] with [reel layout, e.g., 4x4 reels].Symbols on the reels should include [symbol theme, coins,Bones,Spear, Egg,caves, thematic items and essentials relevant to the main theme].The narrative and game elements should serve as a guide for slot game development").content


#print(invokeGem("","",""))