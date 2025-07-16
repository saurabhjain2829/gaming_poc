import os
import asyncio
from huggingface_hub import InferenceClient
from PIL import Image

# Set up the client
client = InferenceClient(
    provider="nebius",
    api_key=os.environ["HUGGINGFACE_HUB_TOKEN"]
)

# Async function to generate one image
async def generate_sketch(input_text: str):
    prompt = (
        f"""A detailed pencil sketch of symbol {input_text}, rendered in fine graphite pencil with crosshatching 
        and shading to show depth and metallic textures. 
        The drawing is hand-drawn on lightly textured parchment or sketchbook paper. 
        The design includes intricate gears, pipes, and vintage steampunk detailing. 
        The image style is consistent with 19th-century engineering blueprints, 
        with a subtle fantasy aesthetic. No color — only pencil grayscale tones. 
        Artistic focus on realism and technical intricacy, suitable for concept art or 
        collectible card designs."""
    )

    def sync_generate():
        image = client.text_to_image(
            prompt=prompt,
            model="black-forest-labs/FLUX.1-dev",
            height=128,
            width=128,
            
        )
        filename = f"{input_text.replace(' ', '_')}_128x128.png"
        image = image.resize((128, 128), Image.LANCZOS)
        image.save(filename)
        return f"Saved: {filename}"

    return await asyncio.to_thread(sync_generate)

# Main async runner
async def generate_all(inputs):
    tasks = [generate_sketch(c) for c in inputs]
    results = await asyncio.gather(*tasks)
    for result in results:
        print(result)

asyncio.run(generate_all(["skeleton"]))