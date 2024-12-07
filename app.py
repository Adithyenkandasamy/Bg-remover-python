from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from PIL import Image
from rembg import remove
import io
import os
from datetime import datetime
import uvicorn

app = FastAPI(title="Background Remover API")

# Create uploads directory if it doesn't exist
UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

@app.get("/", response_class=HTMLResponse)
async def home():
    """Return a simple HTML form for file upload"""
    return """
    <html>
        <head>
            <title>Background Remover</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #f0f0f0;
                }
                .container {
                    background-color: white;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                }
                h1 {
                    color: #333;
                    text-align: center;
                }
                form {
                    display: flex;
                    flex-direction: column;
                    gap: 20px;
                    align-items: center;
                }
                input[type="file"] {
                    padding: 10px;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    width: 100%;
                    max-width: 400px;
                }
                button {
                    background-color: #4CAF50;
                    color: white;
                    padding: 10px 20px;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                    font-size: 16px;
                }
                button:hover {
                    background-color: #45a049;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Background Remover</h1>
                <form action="/remove-bg/" enctype="multipart/form-data" method="post">
                    <input type="file" name="file" accept="image/*" required>
                    <button type="submit">Remove Background</button>
                </form>
            </div>
        </body>
    </html>
    """

@app.post("/remove-bg/")
async def remove_background(file: UploadFile = File(...)):
    """Remove background from uploaded image"""
    try:
        # Read the uploaded file
        contents = await file.read()
        
        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        original_filename = os.path.splitext(file.filename)[0]
        
        # Convert image and remove background
        input_image = Image.open(io.BytesIO(contents))
        
        # Convert to RGBA mode
        input_image = input_image.convert("RGBA")
        
        # Remove background
        output_image = remove(input_image)
        
        # Save the output
        output_filename = f"{original_filename}_nobg_{timestamp}.png"
        output_path = os.path.join(UPLOAD_DIR, output_filename)
        output_image.save(output_path, format="PNG")
        
        # Return the processed image
        return FileResponse(
            output_path,
            media_type="image/png",
            filename=output_filename
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
