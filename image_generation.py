from diffusers import StableDiffusionPipeline
import torch
import os
import common_func as cf
# Load the model (run this once at the start of the script)
device = "cuda" if torch.cuda.is_available() else "cpu"
image_pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5", 
    torch_dtype=torch.float16 if device == "cuda" else torch.float32
).to(device)

def generate_image(prompt, filename="generated_image.png"):
    image = image_pipe(prompt).images[0]
    image.save(filename)
    cf.speak("Image generated successfully.")
    os.startfile(filename)  # Opens the image
