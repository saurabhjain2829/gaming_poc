import os
import yaml
import asyncio
from huggingface_hub import InferenceClient
from PIL import Image
from typing import List, Dict
from dotenv import load_dotenv

# Load config from YAML
with open("image_config.yaml", "r") as file:
    config = yaml.safe_load(file)

# Extract config values
provider = config["huggingface"]["provider"]
model = config["huggingface"]["model"]

width = config["image"]["width"]
height = config["image"]["height"]
extension = config["image"]["extension"]
resize_enabled = config["image"].get("resize", False)
resize_width = config["image"].get("resize_width", width)
resize_height = config["image"].get("resize_height", height)
folder_name=  config["image"]["directory_name"]

style_prompt_template = config["image"]["style_prompt"]


# Set up the client
client = InferenceClient(provider=provider) # HUGGINGFACE_HUB_TOKEN should be in enviornments

# Async function to generate one image
async def generate_sketch(image_input: Dict[str, str], art_style: str):
    print(image_input)
    image_name = image_input["name"]
    image_description = image_input["description"]
    filename = f"{image_name.replace(' ', '_')}{extension}"
    filepath = os.path.join(folder_name, filename)

    # Check if image already exists
    if os.path.exists(filepath):
        print(f"Already exists: {filepath}")
        return f"Skipped (already exists): {filepath}"

    prompt = style_prompt_template.format(name=image_name, description=image_description, art_style=art_style)
    print(prompt)

    def sync_generate():
        image = client.text_to_image(
            prompt=prompt,
            model=model,
            height=height,
            width=width,
        )
        if resize_enabled:
            image = image.resize((resize_width, resize_height), Image.LANCZOS)
        image.save(filepath)
        return f"Saved: {filepath}"

    return await asyncio.to_thread(sync_generate)


async def generate_all(symbols: List[Dict[str, str]], art_style:str):
    tasks = [
        generate_sketch(symbol,art_style)
        for symbol in symbols
    ]
    results = await asyncio.gather(*tasks)
    for result in results:
        print(result)
    print("All images generated successfully")

# Run the script
# asyncio.run(generate_all([
#     {"name": "skeleton", "description": "A spooky skeleton in a dark forest"},
#     {"name": "seashell", "description": "A shiny seashell on a beach"}
# ]))