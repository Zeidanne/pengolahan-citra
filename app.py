from flask import Flask, render_template, request, send_from_directory
import os
from image_processing import process_image

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

method_display = {
    'threshold': 'Threshold',
    'sobel':     'Sobel',
    'prewitt':   'Prewitt',
    'roberts':   'Roberts',
    'canny':     'Canny',
    'erosi':     'Erosi',
    'dilasi':    'Dilasi'
}


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tugas1')
def tugas1():
    return render_template('tugas1.html')

@app.route('/tugas2')
def tugas2():
    return render_template('tugas2.html')

@app.route('/tugas3')
def tugas3():
    return render_template('tugas3.html')

# route tugas 1
@app.route('/upload_tugas1', methods=['POST'])
def upload_tugas1():
    f = request.files['image']
    method = 'threshold'

    original_filename = f"original_{f.filename}" 
    original_path = os.path.join(app.config['UPLOAD_FOLDER'], original_filename)
    f.save(original_path)

    output_filename = f"{method}_{f.filename}"
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
    process_image(original_path, output_path, method)

    return render_template('tugas1.html', 
                            original_url=original_filename, 
                            processed_url=output_filename,
                            method=method_display.get(method, method))

# route tugas 2
@app.route('/upload_tugas2', methods=['POST'])
def upload_tugas2():
    f = request.files['image']
    method = request.form['method']
    
    original_filename = f"original_{f.filename}" 
    original_path = os.path.join(app.config['UPLOAD_FOLDER'], original_filename)
    f.save(original_path)
    
    # Proses gambar
    output_filename = f"{method}_{f.filename}"
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
    process_image(original_path, output_path, method)
    
    return render_template('tugas2.html', 
                        original_url=original_filename, 
                        processed_url=output_filename,
                        method=method_display.get(method, method))

# route tugas 3
@app.route('/upload_tugas3', methods=['POST'])
def upload_tugas3():
    f = request.files['image']
    method  = request.form['method']
    se_type = request.form['se_type']
    se_size = request.form['se_size']

    original_filename = f"original_{f.filename}"
    original_path     = os.path.join(app.config['UPLOAD_FOLDER'], original_filename)
    f.save(original_path)

    output_filename = f"{method}_{se_type}_{f.filename}"
    output_path     = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)

    try:
        se_size_parsed = eval(se_size)
    except:
        se_size_parsed = 3

    process_image(original_path, output_path,method, se_type, se_size_parsed)

    return render_template('tugas3.html',
                            original_url=original_filename,
                            processed_url=output_filename,
                            method=method_display.get(method, method),
                            se_type=se_type,
                            se_size=se_size_parsed)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)