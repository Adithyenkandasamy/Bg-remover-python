from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
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

# Mount the uploads directory
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

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
                #result {
                    margin-top: 20px;
                    text-align: center;
                }
                .preview {
                    max-width: 300px;
                    margin: 20px auto;
                    border-radius: 4px;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                }
                .download-btn {
                    background-color: #2196F3;
                    margin-top: 10px;
                }
                .download-btn:hover {
                    background-color: #1976D2;
                }
                .loading {
                    display: none;
                    margin: 20px auto;
                    text-align: center;
                }
            </style>
            <script>
                function showLoading() {
                    document.getElementById('loading').style.display = 'block';
                    document.getElementById('result').innerHTML = '';
                }

                async function uploadFile(event) {
                    event.preventDefault();
                    showLoading();
                    
                    const formData = new FormData(event.target);
                    try {
                        const response = await fetch('/remove-bg/', {
                            method: 'POST',
                            body: formData
                        });
                        
                        if (response.ok) {
                            const data = await response.json();
                            const result = document.getElementById('result');
                            result.innerHTML = `
                                <img src="${data.image_url}" class="preview" alt="Processed image">
                                <br>
                                <a href="${data.image_url}" download="${data.filename}">
                                    <button class="download-btn">Download Image</button>
                                </a>
                            `;
                        } else {
                            throw new Error('Image processing failed');
                        }
                    } catch (error) {
                        document.getElementById('result').innerHTML = `
                            <p style="color: red;">Error: ${error.message}</p>
                        `;
                    } finally {
                        document.getElementById('loading').style.display = 'none';
                    }
                }
            </script>
        </head>
        <body>
            <div class="container">
                <h1>Background Remover</h1>
                <form onsubmit="uploadFile(event)">
                    <input type="file" name="file" accept="image/*" required>
                    <button type="submit">Remove Background</button>
                </form>
                <div id="loading" class="loading">
                    <p>Processing image... Please wait...</p>
                </div>
                <div id="result"></div>
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
        
        # Return JSON response with image URL
        return {
            "image_url": f"/uploads/{output_filename}",
            "filename": output_filename
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
