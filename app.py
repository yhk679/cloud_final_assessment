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
                font-family: Arial, Helvetica, sans-serif;
                background: linear-gradient(135deg, #4facfe, #00f2fe);
                height: 100vh;
                margin: 0;
                display: flex;
                align-items: center;
                justify-content: center;
            }

            .container {
                background: white;
                padding: 30px 40px;
                border-radius: 12px;
                box-shadow: 0 10px 25px rgba(0,0,0,0.2);
                width: 350px;
                text-align: center;
            }

            h1 {
                margin-bottom: 20px;
                color: #333;
            }

            input[type="file"] {
                margin: 15px 0;
                width: 100%;
            }

            button {
                background-color: #4facfe;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-size: 16px;
                cursor: pointer;
                width: 100%;
            }

            button:hover {
                background-color: #00c6ff;
            }

            footer {
                margin-top: 15px;
                font-size: 12px;
                color: #777;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Upload File to S3</h1>
            <form action="/upload" method="post" enctype="multipart/form-data">
                <input type="file" name="file" required>
                <button type="submit">Upload</button>
            </form>
            <footer>
                Cloud File Upload System
            </footer>
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

