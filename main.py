# app.py
from flask import Flask, request, send_from_directory, render_template, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains

# Define the directory where files will be stored
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)  # Create the directory if it doesn't exist

# Configure Flask to allow file uploads
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # Limit file size to 50MB (optional)

# Allowed file extensions (you can customize this)
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'zip', 'tar', 'mp4', 'mp3'}


# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Serve the frontend HTML page
@app.route('/')
def index():
    return render_template('index.html')  # Flask will look for index.html in the templates folder


# Route to upload files
@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if the file is part of the request
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    # If no file is selected
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # If file is allowed, save it
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # Print for debugging to confirm file path
        print(f"Saving file to: {file_path}")

        try:
            file.save(file_path)
            file_url = f'http://127.0.0.1:5000/download/{filename}'
            return jsonify({'message': 'File uploaded successfully', 'file_url': file_url}), 200
        except Exception as e:
            print(f"Error saving file: {e}")
            return jsonify({'error': 'Error saving the file'}), 500
    else:
        return jsonify({'error': 'File type not allowed'}), 400


# Route to download files
@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    try:
        # Ensure Flask is serving files from the correct directory
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404


if __name__ == '__main__':
    app.run(debug=True, port=5000)
