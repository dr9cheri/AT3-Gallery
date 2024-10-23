import os
from flask import Flask, render_template, jsonify, redirect, request, send_from_directory,url_for
from app import allowed_file, load_image_metadata, save_image_metadata
from hashtag_utils import generate_hashtag

app = Flask(__name__)

# Sample data for images and hashtag
images = [
  {"URL": "../static/images/babypanda.jpg", "hashtag": ["panda", "animal"]},
  {"URL": "../static/images/panda.jpg", "hashtag": ["panda", "animal"]},
  {"URL": "../static/images/pandaintree.jpg", "hashtag": ["panda", "animal"]},
  {"URL": "../static/images/sleeppanda.jpg", "hashtag": ["panda", "animal"]},
  {"URL": "../static/images/Cynstaring.png", "hashtag": ["cyn", "murderdrones"]},
  {"URL": "../static/images/CynJumpscare2.png", "hashtag": ["cyn", "murderdrones"]},
  {"URL": "../static/images/AminotwantedN.png", "hashtag": ["cyn", "murderdrones"]},
  #Add more images and hashtag here
]

@app.route('/')
def index():
  return render_template('layout.html', images=images)

@app.route('/search/<query>')
def search(query):
  filtered_images = [image for image in images if query.lower() in " ".join(image["hashtags"]).lower()]
  return jsonify(filtered_images)

@app.route('/upload_page')
def upload_page():
  
  return render_template('upload.html')

@app.route('/upload',methods=["POST"])
def upload():
  """Handle image upload and save metadata."""
  if 'file' not in request.files:
   return jsonify({'error': 'No file part'}), 400
  
  file = request.files['files']
  if file.filename == '':
    return jsonify({'error': 'No selected file'}), 400
  
  if file and allowed_file(file.filename):
    # Save the file to the "image" folder
    filename = secure_filename(file.filename) # type: ignore
    file_path = os.path.join(app.config['../static/images/<filename>'], filename)
    file.save(file.path)

    # Get list of hashtags from form
    hashtags = request.form.get('hashtags', '')
    hashtags_list = hashtags.split(',')
    valid_hashtags = [hashtag.strip() for hashtag in hashtags_list if hashtag.strip()]

    # Load existing image metadata
    metadata = load_image_metadata()

    #Append new image data
    metadata.append({'filename': filename, 'hashtags': valid_hashtags})

    #Save updated metadata
    save_image_metadata(metadata)

    return jsonify({'message': 'File successfully uploaded', 'hashtags': valid_hashtags}), 200
  else:
    return jsonify({'error': 'Invalid file type'}), 400
  
@app.route('../static/images/<filename>')
def uploaded_file(filename):
  """Serve the uploaded image files."""
  return send_from_directory(app.config['../static/images/<filename>'], filename)

if __name__ == '__main__':
  app.run(debug=True)
