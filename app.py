from flask import Flask, request
import boto3
import os

app = Flask(__name__)

# S3 bucket name
BUCKET_NAME = "csc3074-file-upload"

# Home page - file upload form
@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>S3 File Upload</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg, #667eea, #764ba2);
                height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                margin: 0;
            }

            .card {
                background: white;
                padding: 30px 40px;
                border-radius: 12px;
                width: 350px;
                text-align: center;
                box-shadow: 0 10px 25px rgba(0,0,0,0.2);
            }

            h1 {
                margin-bottom: 20px;
                color: #333;
            }

            input[type="file"] {
                display: none;
            }

            .file-label {
                display: inline-block;
                padding: 12px 20px;
                background: #667eea;
                color: white;
                border-radius: 6px;
                cursor: pointer;
                font-size: 14px;
                transition: background 0.3s;
            }

            .file-label:hover {
                background: #5563d6;
            }

            #file-name {
                margin-top: 10px;
                font-size: 13px;
                color: #555;
            }

            button {
                margin-top: 20px;
                padding: 12px;
                width: 100%;
                background: #764ba2;
                border: none;
                color: white;
                font-size: 15px;
                border-radius: 6px;
                cursor: pointer;
                transition: background 0.3s;
            }

            button:hover {
                background: #5e3b8a;
            }
        </style>

        <script>
            function showFileName() {
                const input = document.getElementById("file");
                const fileName = document.getElementById("file-name");
                fileName.textContent = input.files.length > 0 
                    ? input.files[0].name 
                    : "No file selected";
            }
        </script>
    </head>

    <body>
        <div class="card">
            <h1>Upload File</h1>
            <form action="/upload" method="post" enctype="multipart/form-data">
                <label class="file-label" for="file">Choose File</label>
                <input id="file" type="file" name="file" onchange="showFileName()" required>
                <div id="file-name">No file selected</div>
                <button type="submit">Upload to S3</button>
            </form>
        </div>
    </body>
    </html>
    """



# File upload handler
@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return "No file part", 400

    file = request.files["file"]
    if file.filename == "":
        return "No selected file", 400

    try:
        s3 = boto3.client("s3")
        s3.upload_fileobj(file, BUCKET_NAME, file.filename)
        return f"Upload successful: {file.filename}"
    except Exception as e:
        return f"Upload failed: {str(e)}", 500

# Run Flask on all interfaces, port 80
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)


