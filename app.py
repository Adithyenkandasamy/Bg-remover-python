from PIL import Image
from rembg import remove
import os
import sys

def convert_and_remove_bg(input_path):
    try:
        # Get the filename and directory
        input_dir = os.path.dirname(input_path)
        filename = os.path.basename(input_path)
        name_without_ext = os.path.splitext(filename)[0]
        
        print(f"Processing image: {filename}")
        
        # Open and convert image to PNG format (best format for transparency)
        with Image.open(input_path) as img:
            # Convert to RGBA mode to ensure transparency support
            img = img.convert("RGBA")
            
            # Save temporary PNG file
            temp_png = os.path.join(input_dir, f"{name_without_ext}_temp.png")
            img.save(temp_png, format="PNG")
            print("Image converted to PNG format")
            
            # Remove background
            with Image.open(temp_png) as png_img:
                # Remove background
                output = remove(png_img)
                
                # Save the output
                output_path = os.path.join(input_dir, f"{name_without_ext}_nobg.png")
                output.save(output_path)
                print(f"Background removed! Output saved as: {output_path}")
            
            # Clean up temporary file
            os.remove(temp_png)
            print("Temporary files cleaned up")
            
            return True
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def main():
    # Check if input file is provided
    if len(sys.argv) < 2:
        print("Please provide the path to the image file.")
        print("Usage: python app.py <path_to_image>")
        return
    
    input_path = sys.argv[1]
    
    # Check if file exists
    if not os.path.exists(input_path):
        print(f"Error: File '{input_path}' does not exist.")
        return
    
    # Process the image
    if convert_and_remove_bg(input_path):
        print("Processing completed successfully!")
    else:
        print("Failed to process the image.")

if __name__ == "__main__":
    main()
