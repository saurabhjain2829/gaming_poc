import yaml
from pydantic.v1 import BaseSettings, Field
import threading
import asyncio
import time
from langchain_openai import AzureChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.output_parsers import PydanticOutputParser
from typing import List, Dict
from langchain_core.exceptions import OutputParserException

import ImageGeneratorService_nebius as image_service
from schemas import GameDesignSchema
from dotenv import load_dotenv

# === Environment Settings ===
class EnvironmentSettings(BaseSettings):
    AZURE_OPENAI_API_KEY: str = Field(..., description="Azure OpenAI key")
    AZURE_OPENAI_ENDPOINT: str = Field(..., description="Azure OpenAI endpoint")
    AZURE_OPENAI_API_VERSION: str = Field(..., description="Azure OpenAI API version")
    AZURE_OPENAI_DEPLOYMENT_NAME: str = Field(..., description="Azure OpenAI model name")

    class Config:
        env_file = ".env"

environment_settings = EnvironmentSettings()

# === Load Configuration ===
with open("game_service_config.yaml", "r") as f:
    config = yaml.safe_load(f)

# === Output Parser ===
parser = PydanticOutputParser(pydantic_object=GameDesignSchema)

# === Azure LLM Model === 
llm_model = AzureChatOpenAI(
    azure_endpoint=environment_settings.AZURE_OPENAI_ENDPOINT,
    azure_deployment=environment_settings.AZURE_OPENAI_DEPLOYMENT_NAME,
    api_version=environment_settings.AZURE_OPENAI_API_VERSION,
    api_key=environment_settings.AZURE_OPENAI_API_KEY,
    temperature=config["llm"]["temperature"]
)

# === Prompt Template ===
game_prompt = PromptTemplate(
    input_variables=["input_text", "exclude_sections"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
    template=config["prompt"]["template"]
)

def generate_game_details(user_input, exclude_sections):
    print(exclude_sections)
    chain = LLMChain(
        llm=llm_model,
        prompt=game_prompt,
        output_parser=parser,
        verbose=True
    )

    
    include_prompt, exclude_prompt = generate_dynamic_prompt_elements(exclude_sections)
    
    result = safe_run_chain(chain, {
    "input_text": user_input,
    "include_prompt": include_prompt,
    "exclude_prompt": exclude_prompt
    })
    #result=chain.run({"input_text": user_input, "include_prompt": include_prompt, "exclude_prompt" : exclude_prompt})
    if not result:
        print("[Failure] No game details generated.")
        return None

    run_image_generator(extract_symbols(result), extract_visual_style(result), extract_game_title(result))
    run_image_generator(extract_characters(result), extract_visual_style(result), extract_game_title(result))

    print(result)
    return result

def safe_run_chain(chain, inputs, retries=2):
    for attempt in range(1, retries + 1):
        try:
            return chain.run(inputs)
        except OutputParserException as e:
            print(f"[Attempt {attempt}] Parsing Error: {e}")
            time.sleep(1)  # slight delay before retry
        except Exception as e:
            print(f"[Attempt {attempt}] Unexpected Error: {e}")
            break
    return None

def run_image_generator(symbols: List[Dict[str, str]], art_style: str, gameTitle: str):
    if symbols:
        def async_task():
            try:
                asyncio.run(image_service.generate_all(symbols, art_style, gameTitle))
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

    return [{"name": char.name, "description": char.description} for char in schema.characters]

def extract_visual_style(schema: GameDesignSchema) -> str:
    return schema.visualStyle.artStyle if schema.visualStyle else ""

def extract_game_title(schema: GameDesignSchema) -> str:
    return schema.gameTitle if schema.gameTitle else ""

def generate_dynamic_prompt_elements(exclude_sections):
    dynamic_elements ={"""Symbols

Include 5 Low Pay Symbols, between 3 to 5 Royal Symbols (e.g., A, K, Q, J, 10, 9), 5 High Pay Symbols, 2 to 4 Wild Symbols, and 1 to 2 Scatter Symbols.

Each symbol should match the game’s theme and tone, with a detailed visual description suitable for generating theme-relevant images.

Descriptions should support both thematic consistency and visual design needs.
Map the details like visual description and symbol description etc to description field.                      

Characters

Describe the main characters featured in the game.

Ensure that each character is aligned with the theme and tone of the game.

Provide detailed visual and personality descriptions that can be used to generate relevant artwork.

Bonus Features

Include at least four bonus features such as Free Spins, Free Rounds, Mini Games, Multipliers, Bonus Wheels, and Jackpot Features.

Describe each bonus feature in detail and ensure it ties into both the overall gameplay mechanics and the game theme.

Bonus features should be engaging, thematic, and distinct from each other. """}
    # exclude_prompt = "Exclude " if len(exclude_sections)>0 else ""
    # include_prompt =""" """
    # for key, value in dynamic_elements.items():
    #     if(key in exclude_sections):
    #       exclude_prompt += " \n - " + key
    #     else:
    #         include_prompt +=   value +" \n "
    # return include_prompt, exclude_prompt
    return dynamic_elements, ""