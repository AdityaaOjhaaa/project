import os
import uuid
from flask import Flask, request, render_template, send_from_directory
import easyocr
from PIL import Image

# Initialize Flask app
app = Flask(__name__)

# Set upload folder
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

# Initialize EasyOCR Reader (load only when needed to save memory)
reader = None

def get_reader():
    global reader
    if reader is None:
        reader = easyocr.Reader(['en'], gpu=False)
    return reader

# Function to perform OCR using EasyOCR
def extract_text(image_path):
    # Use EasyOCR to extract text from the image
    result = get_reader().readtext(image_path, detail=0)  # detail=0 returns only text
    return " ".join(result)

# Clean the extracted text for readability
def clean_text(text):
    # Remove extra whitespaces and ensure proper formatting
    return "\n".join(line.strip() for line in text.splitlines() if line.strip())

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# File upload route
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return render_template('index.html', error='No file uploaded!')
    file = request.files['file']
    if file.filename == '':
        return render_template('index.html', error='No selected file!')
    
    # Generate a unique filename to prevent overwriting
    unique_filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
    file.save(file_path)
    
    try:
        # Perform OCR
        raw_text = extract_text(file_path)
        cleaned_text = clean_text(raw_text)
        success = True
    except Exception as e:
        cleaned_text = f"Error processing image: {str(e)}"
        success = False
    
    return render_template('result.html', text=cleaned_text, success=success)

# Error handling
@app.errorhandler(413)
def request_entity_too_large(error):
    return render_template('index.html', error='The image you tried to upload is too large.')

# Add a simple health check endpoint
@app.route('/health')
def health_check():
    return "OK", 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
