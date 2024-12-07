# Background Remover API

A FastAPI-based web application that removes backgrounds from images of any format.

## Features
- Web interface for easy image upload
- API endpoint for programmatic access
- Supports various image formats (PNG, JPEG, AVIF, etc.)
- Automatically converts images to PNG format
- Removes background using the rembg library
- Preserves transparency in output images

## Requirements
Install the required packages:
```bash
pip install fastapi uvicorn python-multipart rembg Pillow pillow-avif-plugin
```

## Usage

### Starting the Server
```bash
python app.py
```
This will start the server at http://localhost:8000

### Using the Web Interface
1. Open your browser and go to http://localhost:8000
2. Upload an image using the web interface
3. Click "Remove Background"
4. The processed image will be downloaded automatically

### Using the API
You can also use the API endpoint directly:

```bash
curl -X POST -F "file=@your_image.jpg" http://localhost:8000/remove-bg/ --output output.png
```

## API Documentation
- API documentation is available at http://localhost:8000/docs
- Alternative documentation at http://localhost:8000/redoc

## Supported Image Formats
- PNG
- JPEG/JPG
- WEBP
- BMP
- TIFF
- And many more!
