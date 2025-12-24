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
        <title>Upload File</title>
    </head>
    <body>
        <h1>Upload a File to S3</h1>
        <form action="/upload" method="post" enctype="multipart/form-data">
            <input type="file" name="file" required>
            <button type="submit">Upload</button>
        </form>
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
