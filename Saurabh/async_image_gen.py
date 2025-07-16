import os
import asyncio
from huggingface_hub import InferenceClient
from PIL import Image

client = InferenceClient(
    provider="nebius",
    api_key=os.environ["HUGGINGFACE_HUB_TOKEN"],
)

async def generate_image(input):
    def sync_generate():
        return client.text_to_image(
    prompt=f"A clean pencil sketch of {input}, centered on a transparent canvas, black and white minimalist style, 128x128 resolution, sharp outlines, no background, no shading, icon-like, line art.",
    model="black-forest-labs/FLUX.1-dev",
    negative_prompt="blurry, distorted",
    height=128,
    width=128,
    num_inference_steps=30,
    guidance_scale=12.5,
    seed=42,
    )
       

    image = await asyncio.to_thread(sync_generate)
    image.save(f"{input}.png")

#asyncio.run(generate_image("fire torch"))
asyncio.run(generate_image("skeleton"))