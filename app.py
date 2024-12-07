from PIL import Image
import os
from rembg import remove

# Input and Output Paths
input_image = "input1.avif"  # Replace with your input image path
intermediate_image = "converted_input1.png"  # Intermediate PNG file
output_image = "output1.png"  # Final output with background removed

try:
    # Step 1: Convert Input Image to PNG (if needed)
    with Image.open(input_image) as img:
        img = img.convert("RGBA")  # Convert to RGBA for transparency support
        img.save(intermediate_image, format="PNG")  # Save as PNG
        print(f"Converted {input_image} to {intermediate_image}")

    # Step 2: Read the Converted PNG File
    with open(intermediate_image, "rb") as input_file:
        in_image = input_file.read()

    # Step 3: Remove Background
    out_image = remove(in_image)

    # Step 4: Save the Final Image
    with open(output_image, "wb") as output_file:
        output_file.write(out_image)

    print(f"Background removed successfully! Output saved at {output_image}")

except Exception as e:
    print("Error:", e)
