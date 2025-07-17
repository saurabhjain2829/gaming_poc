# main.py
import yaml
from dotenv import load_dotenv
import os

from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.output_parsers import PydanticOutputParser

from final_schemas import GameDesignSchema 

# === Load Configuration ===
with open("final_game_service_config.yaml", "r") as f:
    config = yaml.safe_load(f)

# === Load API Key ===
load_dotenv()

# === Output Parser ===
parser = PydanticOutputParser(pydantic_object=GameDesignSchema)

# === LLM Model ===
llm_model = ChatGoogleGenerativeAI(
    model=config["llm"]["model"],
    temperature=config["llm"]["temperature"]
)

# === Prompt Template ===
game_prompt = PromptTemplate(
    input_variables=["input_text"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
    template=config["prompt"]["template"]
)

# === Inference Function ===
def generate_game_details(user_input):
    chain = LLMChain(
        llm=llm_model,
        prompt=game_prompt,
        output_parser=parser,
        verbose=True
    )
    return chain.run({"input_text": user_input})


#print(generate_game_details("As a game designer I want a game on Time travel including storyline, symbols, characters, game mchenice "))
result = generate_game_details("As a game designer I want a game on Time travel including storyline, symbols, characters, game mchenice ")
print(result)