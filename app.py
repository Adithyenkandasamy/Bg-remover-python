from PIL import Image
from rembg import remove
import os

# Paths
input_image = "/home/yellowflash/Adithyenrepose/Bg-remover-python/input1.avif"
converted_image = "/home/yellowflash/Adithyenrepose/Bg-remover-python/converted_input1.png"
output_image = "/home/yellowflash/Adithyenrepose/Bg-remover-python/output1.png"

# Step 1: Convert AVIF to PNG
try:
    with Image.open(input_image) as img:
        img = img.convert("RGBA")
        img.save(converted_image, format="PNG")
        print(f"Converted {input_image} to {converted_image}")
except Exception as e:
    print(f"Error converting {input_image}: {e}")
    print("Ensure 'pillow-avif-plugin' is installed or use FFmpeg for conversion.")
    exit()

# Step 2: Remove Background
try:
    with open(converted_image, "rb") as input_file:
        in_image = input_file.read()
    out_image = remove(in_image)
    with open(output_image, "wb") as output_file:
        output_file.write(out_image)
    print(f"Background removed successfully! Output saved at {output_image}")
except Exception as e:
    print(f"Error during background removal: {e}")
