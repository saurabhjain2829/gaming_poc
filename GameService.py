# main.py
import yaml
from dotenv import load_dotenv
import os
import threading
import asyncio

from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.output_parsers import PydanticOutputParser
from typing import List, Dict
import ImageGeneratorService_nebius as image_service

from schemas import GameDesignSchema 

# === Load Configuration ===
with open("game_service_config.yaml", "r") as f:
    config = yaml.safe_load(f)

# === Load API Key ===
load_dotenv()

# === Output Parser ===
parser = PydanticOutputParser(pydantic_object=GameDesignSchema)

# GOOGLE_API_KEY should be in enviornments
# === LLM Model === 
llm_model = ChatGoogleGenerativeAI(
    model=config["llm"]["model"],
    temperature=config["llm"]["temperature"]
)

# === Prompt Template ===
game_prompt = PromptTemplate(
    input_variables=["input_text", "exclude_sections"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
    template=config["prompt"]["template"]
)


def generate_game_details(user_input,exclude_sections):
    print(exclude_sections)
    chain = LLMChain(
        llm=llm_model,
        prompt=game_prompt,
        output_parser=parser,
        verbose=True
        
    )
    

    exclude_sections_text=[]
    for section in exclude_sections:
     exclude_sections_text.append(f'User does not want {section} in the output.')
 
    result=chain.run({"input_text": user_input, "exclude_sections": "\n".join(exclude_sections_text)})
 
    run_image_generator(extract_symbols(result),extract_visual_style(result),extract_game_title(result))
    run_image_generator(extract_characters(result),extract_visual_style(result),extract_game_title(result))
    print(result)
    return result

def run_image_generator(symbols: List[Dict[str, str]],art_style: str,gameTitle: str):
     if symbols:
        def async_task():
            try:
                asyncio.run(image_service.generate_all(symbols,art_style,gameTitle))
            except Exception as e:
                print(f"[Image Generation Error] {e}")

        thread = threading.Thread(target=async_task)
        thread.start()  


def extract_symbols(schema: GameDesignSchema) -> List[Dict[str, str]]:
    if not schema.symbols:
        return []

    all_symbols = []
    for symbol in (schema.symbols.lowPaySymbols or []):
        all_symbols.append({"name": symbol.name, "description": symbol.description})

    for symbol in (schema.symbols.royalSymbols or []):
        all_symbols.append({"name": symbol.name, "description": symbol.description})
    for symbol in (schema.symbols.highPaySymbols or []):
        all_symbols.append({"name": symbol.name, "description": symbol.description})
    for symbol in (schema.symbols.wildSymbols or []):
        all_symbols.append({"name": symbol.name, "description": symbol.description})
    for symbol in (schema.symbols.scatterSymbols or []):
        all_symbols.append({"name": symbol.name, "description": symbol.description})

    return all_symbols

def extract_characters(schema: GameDesignSchema) -> List[Dict[str, str]]:
    if not schema.characters:
        return []

    all_characters = []
    for characters in (schema.characters or []):
        all_characters.append({"name": characters.name, "description": characters.description})

   
    return all_characters

def extract_visual_style(schema: GameDesignSchema) -> str:
    return schema.visualStyle.artStyle if schema.visualStyle else ""

def extract_game_title(schema: GameDesignSchema) -> str:
    return schema.gameTitle if schema.gameTitle else ""