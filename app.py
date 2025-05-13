from flask import Flask, render_template, request, send_from_directory
import os
from image_processing import process_image

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    f = request.files['image']
    method = request.form['method']
    
    # Simpan gambar original dengan nama unik
    original_filename = f"original_{f.filename}" 
    original_path = os.path.join(app.config['UPLOAD_FOLDER'], original_filename)
    f.save(original_path)  # Simpan file original ke folder uploads
    
    # Proses gambar
    output_filename = f"{method}_{f.filename}"  # Contoh: sobel_cat.jpg
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
    process_image(original_path, output_path, method)
    
    return render_template('index.html', 
                        original_url=original_filename, 
                        processed_url=output_filename)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)