import os
from huggingface_hub import InferenceClient

client = InferenceClient(
    provider="nebius",
    api_key=os.environ["HUGGINGFACE_HUB_TOKEN"],
)

# output is a PIL.Image object
image = client.text_to_image(
    "create a pencil sketch style with resolution 128x128 as thumnail for symbol Seashell",
     model="black-forest-labs/FLUX.1-dev",
)
image.save("Sea_1111.png")