import os
import yaml
import asyncio
from huggingface_hub import InferenceClient
from PIL import Image

# Load config from YAML
with open("final_image_config.yaml", "r") as file:
    config = yaml.safe_load(file)

# Extract config values
provider = config["huggingface"]["provider"]
api_key = os.environ[config["huggingface"]["api_key_env"]]
model = config["huggingface"]["model"]

width = config["image"]["width"]
height = config["image"]["height"]
extension = config["image"]["extension"]
resize_enabled = config["image"].get("resize", False)
resize_width = config["image"].get("resize_width", width)
resize_height = config["image"].get("resize_height", height)

style_prompt_template = config["image"]["style_prompt"]
inputs = config["inputs"]

# Set up the client
client = InferenceClient(provider=provider, api_key=api_key)

# Async function to generate one image
async def generate_sketch(input_text: str):
    prompt = style_prompt_template.format(input_text=input_text)

    def sync_generate():
        image = client.text_to_image(
            prompt=prompt,
            model=model,
            height=height,
            width=width,
        )
        filename = f"{input_text.replace(' ', '_')}_{width}x{height}{extension}"
        if resize_enabled:
            image = image.resize((resize_width, resize_height), Image.LANCZOS)
        image.save(filename)
        return f"Saved: {filename}"

    return await asyncio.to_thread(sync_generate)

# Main async runner
async def generate_all(inputs):
    tasks = [generate_sketch(text) for text in inputs]
    results = await asyncio.gather(*tasks)
    for result in results:
        print(result)

# Run the script
asyncio.run(generate_all(["skeleton","seashell"]))