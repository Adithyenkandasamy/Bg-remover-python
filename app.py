from flask import Flask, request, render_template_string, jsonify, send_from_directory
import os
from PIL import Image
from rembg import remove
import io
from datetime import datetime

app = Flask(__name__)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.route('/')
def home():
    return render_template_string(HTML_FORM, uploaded_images=os.listdir(UPLOAD_DIR))

@app.route('/remove-bg/', methods=['POST'])
def remove_background():
    try:
        if 'files' not in request.files:
            return jsonify({"error": "No files provided"}), 400
        
        files = request.files.getlist('files')
        if not files:
            return jsonify({"error": "No selected files"}), 400

        processed_images = []

        for file in files:
            if file.filename == '':
                continue  

            contents = file.read()
            input_image = Image.open(io.BytesIO(contents))
            input_image = input_image.convert("RGBA")

            output_image = remove(input_image)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            original_filename = os.path.splitext(file.filename)[0]
            output_filename = f"{original_filename}_nobg_{timestamp}.png"
            output_path = os.path.join(UPLOAD_DIR, output_filename)
            output_image.save(output_path, format="PNG")

            processed_images.append(output_filename)

        return jsonify({"images": processed_images})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_DIR, filename)

HTML_FORM = """
<html>
<head>
    <title>Batch Background Remover</title>
    <style>
        .preview-container {
            margin-top: 20px;
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
            justify-content: center;
        }
        .preview-item {
            text-align: center;
        }
        .preview {
            max-width: 150px;
            height: auto;
            border: 2px solid #ddd;
            border-radius: 10px;
            padding: 5px;
            background: #f9f9f9;
        }
        .download-btn {
            margin-top: 5px;
            padding: 5px 10px;
            background-color: #28a745;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 12px;
        }
        .download-btn:hover {
            background-color: #218838;
        }
    </style>
    <script>
        function showLoading() {
            document.getElementById('loading').style.display = 'block';
            document.getElementById('result').innerHTML = '';
        }

        async function uploadFiles(event) {
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
                    let imagesHtml = '<div class="preview-container">';
                    data.images.forEach(img => {
                        imagesHtml += `
                            <div class="preview-item">
                                <img src="/uploads/${img}" class="preview" alt="Processed image">
                                <a href="/uploads/${img}" download="${img}">
                                    <button class="download-btn">Download</button>
                                </a>
                            </div>
                        `;
                    });
                    imagesHtml += '</div>';
                    document.getElementById('result').innerHTML = imagesHtml;
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
    <h1>Batch Background Remover</h1>
    <form onsubmit="uploadFiles(event)" enctype="multipart/form-data">
        <input type="file" name="files" accept="image/*" multiple required>
        <button type="submit">Remove Background</button>
    </form>
    <div id="loading" style="display: none;">Processing images... Please wait...</div>
    <div id="result"></div>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
