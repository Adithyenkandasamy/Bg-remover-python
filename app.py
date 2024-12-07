from rembg import remove
from PIL import Image
import io

# Input and Output Image Paths
input_image = "input1.png"  # Original AVIF file
intermediate_image = "converted_input1.png"  # Temporary PNG file
output_image = "output1.png"  # Final file after background removal

try:
    # Step 1: Convert AVIF to PNG
    with Image.open(input_image) as img:
        img = img.convert("RGBA")  # Convert to PNG-friendly format
        img.save(intermediate_image, format="PNG")  # Save as PNG
        print(f"Converted {input_image} to {intermediate_image}")

    with open(intermediate_image, "rb") as input_file:
        in_image = input_file.read()

    out_image = remove(in_image)

    # Step 4: Save the Final Image
    with open(output_image, "wb") as output_file:
        output_file.write(out_image)

    print("Background removed successfully!")
except Exception as e:
    print("Error:", e)
