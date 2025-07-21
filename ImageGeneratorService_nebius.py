import os
import yaml
import asyncio
from PIL import Image
from typing import List, Dict
from dotenv import load_dotenv
from openai import OpenAI
import base64
from io import BytesIO
import GameUtils as gameUtils
# Load config from YAML
with open("image_config.yaml", "r") as file:
    config = yaml.safe_load(file)

# Extract config values

model = config["nebius"]["model"]
base_url = config["nebius"]["base_url"]
response_extension= config["nebius"]["response_extension"]
response_format= config["nebius"]["response_format"]

width = config["image"]["width"]
height = config["image"]["height"]
extension = config["image"]["extension"]
resize_enabled = config["image"].get("resize", False)
resize_width = config["image"].get("resize_width", width)
resize_height = config["image"].get("resize_height", height)

style_prompt_template = config["image"]["style_prompt"]
load_dotenv()

client = OpenAI(
    base_url=base_url,
    api_key=os.environ.get("NEBIUS_API_KEY")
)

# Async function to generate one image
async def generate_sketch(image_input: Dict[str, str], art_style: str, gameTitle: str):
    print(image_input)
    image_name = image_input["name"]
    image_description = image_input["description"]
    filename = f"{image_name.replace(' ', '_')}{extension}"
    directory_name= gameUtils.create_directory_name(gameTitle)
    os.makedirs(directory_name, exist_ok=True)
    filepath = os.path.join(directory_name, filename)

    # Check if image already exists
    if os.path.exists(filepath):
        print(f"Already exists: {filepath}")
        return f"Skipped (already exists): {filepath}"

    prompt = style_prompt_template.format(name=image_name, description=image_description, art_style=art_style)
    print(prompt)

    def sync_generate():
        result = client.images.generate(
        model=model,
        response_format=response_format,
        prompt=prompt,
        extra_body={
            "response_extension": response_extension,
            "width": width,
            "height": height,
            "num_inference_steps": 28,
            "negative_prompt": "",
            "seed": -1,
            "loras": None
        }
    )

    # Extract and decode base64 image string
        image_b64 = result.data[0].b64_json
        image_data = base64.b64decode(image_b64)
        image = Image.open(BytesIO(image_data))

        # Resize if enabled
        if resize_enabled:
            image = image.resize((resize_width, resize_height), Image.LANCZOS)

        # Ensure the directory exists
        os.makedirs(directory_name, exist_ok=True)

    # Save the image
        image.save(filepath)
        return f"Saved: {filepath}"

    return await asyncio.to_thread(sync_generate)


async def generate_all(symbols: List[Dict[str, str]], art_style:str,gameTitle: str):
    tasks = [
        generate_sketch(symbol,art_style,gameTitle)
        for symbol in symbols
    ]
    results = await asyncio.gather(*tasks)
    for result in results:
        print(result)
    print("All images generated successfully by nebius")

