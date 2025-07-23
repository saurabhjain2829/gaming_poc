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
import shutil

# Load config from YAML
with open("image_config.yaml", "r") as file:
    config = yaml.safe_load(file)

# Extract config values
folder_name = config["image"]["directory_name"]
model = config["nebius"]["model"]
base_url = config["nebius"]["base_url"]
response_extension = config["nebius"]["response_extension"]
response_format = config["nebius"]["response_format"]
image_generation_enable= config["image_generation_enable"]
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

def handle_no_image_found(target_path: str):
    fallback_image_path = "image_not_found.png"

    target_dir = os.path.dirname(target_path)
    os.makedirs(target_dir, exist_ok=True)

    try:
        shutil.copy2(fallback_image_path, target_path)
        print(f"Fallback image copied to: {target_path}")
        return f"Fallback used: {target_path}"
    except Exception as e:
        print(f"Failed to copy fallback image: {e}")
        return f"Failed to provide fallback image for: {target_path}"

def sync_generate(prompt: str, filepath: str, directory_name: str) -> str:
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

    image_b64 = result.data[0].b64_json
    image_data = base64.b64decode(image_b64)
    image = Image.open(BytesIO(image_data))

    if resize_enabled:
        image = image.resize((resize_width, resize_height), Image.LANCZOS)

    os.makedirs(directory_name, exist_ok=True)
    image.save(filepath)
    return f"Saved: {filepath}"

async def generate_sketch(image_input: Dict[str, str], art_style: str, gameTitle: str):
    print(image_input)
    image_name = image_input["name"]
    image_description = image_input["description"]
    filename = f"{image_name.replace(' ', '_')}{extension}"
    directory_name = gameUtils.create_directory_name(gameTitle, folder_name)
    os.makedirs(directory_name, exist_ok=True)

    filepath = os.path.join(directory_name, filename)

    if os.path.exists(filepath):
        print(f"Already exists: {filepath}")
        return f"Skipped (already exists): {filepath}"
    if image_generation_enable:
            prompt = style_prompt_template.format(name=image_name, description=image_description, art_style=art_style)
            print(prompt)

            max_attempts = 3
            for attempt in range(1, max_attempts + 1):
                try:
                    result = await asyncio.to_thread(sync_generate, prompt, filepath, directory_name)
                    return result
                except Exception as e:
                    print(f"[Attempt {attempt}/{max_attempts}] Error during image generation: {e}")
                    if attempt < max_attempts:
                        await asyncio.sleep(1)
                    else:
                        print(f"Final failure for input: {image_input} with prompt: {prompt}")
                        return handle_no_image_found(filepath)
    else:
        return handle_no_image_found(filepath)

async def generate_all(symbols: List[Dict[str, str]], art_style: str, gameTitle: str):
    tasks = [generate_sketch(symbol, art_style, gameTitle) for symbol in symbols]
    results = await asyncio.gather(*tasks)
    for result in results:
        print(result)
    print("All images generated successfully by nebius")