from flask import Flask, request, jsonify, render_template, send_from_directory
from werkzeug.utils import secure_filename
import os
import json
from hashtag_utils import generate_hashtag, is_valid_hashtag, save_hashtags, load_hashtags

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
IMAGE_METADATA_FILE = 'image_metadata.json'

def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def load_image_metadata():
    """Load image metadata from the JSON file."""
    try:
        with open(IMAGE_METADATA_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return[]

def save_image_metadata(metadata):
    """Save image metadata to the JSON file."""
    with open(IMAGE_METADATA_FILE, 'w') as file:
        json.dump(metadata, file)

@app.route('/')
def upload_form():
    """Render the upload form."""
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_images():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        hashtags = request.form.get('hashtags', '')
        hashtags_list = hashtags.split(',')
        valid_hashtags = [hashtag.strip() for hashtag in hashtags_list if is_valid_hashtag(hashtag.strip)]
        save_hashtags(valid_hashtags)

        # Save image metadata
        metadata = load_image_metadata()
        metadata.append({'filename': filename, 'hashtag': valid_hashtags})
        save_image_metadata(metadata)
        return jsonify({'message': 'File successfully uploaded', 'hashtag': valid_hashtags}), 200
    else:
        return jsonify({'error': 'Invalid file type'}), 400

@app.route('/search', methods=['GET'])
def search_form():
    return render_template('search.html')

@app.route('/search_images', methods=['POST'])
def search_images():
    search_hashtag = request.form.get('hashtag', '').split(',')
    search_hashtag = [hashtag.strip() for hashtag in search_hashtag if is_valid_hashtag(hashtag.strip())]

    metadata = load_image_metadata()
    result = [item for item in metadata if any(hashtag in item['hashtag'] for hashtag in search_hashtag)]

    return jsonify({'result': result})

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    text = data.get('text', '')
    hashtag = generate_hashtag(text)
    return jsonify({'hashtag': hashtag})

@app.route('/validate', methods=['POST'])
def validate():
    data = request.json
    hashtag = data.get('hashtag', '')
    valid = is_valid_hashtag(hashtag)
    return jsonify({'valid': valid})

@app.route('/add', methods=['POST'])
def add():
    data = request.json
    new_hashtag = data.get('hashtag', [])
    existing_hashtag = load_hashtags()

    valid_hashtag = [hashtag for hashtag in new_hashtag if is_valid_hashtag(hashtag)]
    save_hashtags(valid_hashtag)

    update_hashtag = load_hashtags()
    return jsonify({'update_hashtag': update_hashtag})

@app.route('/gallery')
def gallery():
    """Render the gallery view with all images."""
    metadata = load_image_metadata()
    return render_template('gallery.html', images=metadata)

@app.route('/search', methods=['GET', 'POST'])
def search():
    """Handle search queries and display results."""
    if request.method =='POST':
        search_hashtags = request.form.get('hashtags', '').split(',')
        search_hashtags = [hashtag.strip() for hashtag in search_hashtags if hashtag.strip()]

        metadata = load_image_metadata()
        results = [item for item in metadata if any(hashtag in item['hashtags'] for hashtag in search_hashtags)]

        return render_template('search_results.html', images=results)
    return render_template('search.html')

if __name__ == '__main__':
    app.run(debug=True)