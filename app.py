from flask import Flask, request, render_template_string, jsonify, send_from_directory
import os
from PIL import Image
from rembg import remove
import io
from datetime import datetime

app = Flask(__name__)

# Create uploads directory if it doesn't exist
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.route('/')
def home():
    return render_template_string(HTML_FORM)

@app.route('/remove-bg/', methods=['POST'])
def remove_background():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        # Read image
        contents = file.read()
        input_image = Image.open(io.BytesIO(contents))
        input_image = input_image.convert("RGBA")
        
        # Remove background
        output_image = remove(input_image)
        
        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        original_filename = os.path.splitext(file.filename)[0]
        output_filename = f"{original_filename}_nobg_{timestamp}.png"
        output_path = os.path.join(UPLOAD_DIR, output_filename)
        output_image.save(output_path, format="PNG")
        
        return jsonify({
            "image_url": f"/uploads/{output_filename}",
            "filename": output_filename
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_DIR, filename)

HTML_FORM = """
<html>
<head>
    <title>Background Remover</title>
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
                const data = await response.json();
                if (response.ok) {
                    document.getElementById('result').innerHTML = `
                        <img src="${data.image_url}" class="preview" alt="Processed image">
                        <br>
                        <a href="${data.image_url}" download="${data.filename}">
                            <button class="download-btn">Download Image</button>
                        </a>
                    `;
                } else {
                    throw new Error(data.error);
                }
            } catch (error) {
                document.getElementById('result').innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
            } finally {
                document.getElementById('loading').style.display = 'none';
            }
        }
    </script>
</head>
<body>
    <h1>Background Remover</h1>
    <form onsubmit="uploadFile(event)" enctype="multipart/form-data">
        <input type="file" name="file" accept="image/*" required>
        <button type="submit">Remove Background</button>
    </form>
    <div id="loading" style="display: none;">Processing image... Please wait...</div>
    <div id="result"></div>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
