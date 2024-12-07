# Background Remover

A Python script that can remove backgrounds from images of any format.

## Features
- Supports various image formats (PNG, JPEG, AVIF, etc.)
- Automatically converts images to PNG format
- Removes background using the rembg library
- Preserves transparency in output images

## Requirements
```bash
pip install rembg Pillow pillow-avif-plugin
```

## Usage
```bash
python app.py <path_to_image>
```

Example:
```bash
python app.py image.jpg
```

The output will be saved in the same directory as the input image with "_nobg" suffix.
For example, if your input is "image.jpg", the output will be "image_nobg.png".

## Supported Image Formats
- PNG
- JPEG/JPG
- WEBP
- BMP
- TIFF
- And many more!
