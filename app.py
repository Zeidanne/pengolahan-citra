from flask import Flask, render_template, request, send_from_directory, session
import os
from image_processing import process_image

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.secret_key = 'HAL9900'
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
    original_image_filename = session.get('original_image_tugas1_filename')
    return render_template('tugas1.html',
                            original_image_filename_from_session=original_image_filename,
                            original_url=session.get('original_url_tugas1'),
                            processed_url=session.get('processed_url_tugas1'),
                            method=session.get('method_tugas1'),
                            method_display=method_display)

@app.route('/tugas2')
def tugas2():
    original_image_filename = session.get('original_image_tugas2_filename')
    return render_template('tugas2.html',
                            original_image_filename_from_session=original_image_filename,
                            original_url=session.get('original_url_tugas2'),
                            processed_url=session.get('processed_url_tugas2'),
                            method=session.get('method_tugas2'),
                            method_display=method_display)


@app.route('/tugas3')
def tugas3():
    original_image_filename = session.get('original_image_tugas3_filename')
    return render_template('tugas3.html',
                            original_image_filename_from_session=original_image_filename,
                            original_url=session.get('original_url_tugas3'),
                            processed_url=session.get('processed_url_tugas3'),
                            method=session.get('method_tugas3'),
                            se_type=session.get('se_type_tugas3'),
                            se_size=session.get('se_size_tugas3'),
                            method_display=method_display)

@app.route('/tugas4')
def tugas4():
    original_image_filename = session.get('original_image_tugas4_filename')
    return render_template('tugas4.html',
                            original_image_filename_from_session=original_image_filename,
                            original_url=session.get('original_url_tugas4'),
                            processed_url=session.get('processed_url_tugas4'),
                            method=session.get('method_tugas4'),
                            se_type=session.get('se_type_tugas4'),
                            se_size=session.get('se_size_tugas4'),
                            method_display=method_display)

@app.route('/upload_tugas1', methods=['POST'])
def upload_tugas1():
    original_filename_to_process = None

    if 'image' in request.files and request.files['image'].filename != '':
        f = request.files['image']
        original_filename = f"original_tugas1_{f.filename}"
        original_path = os.path.join(app.config['UPLOAD_FOLDER'], original_filename)
        f.save(original_path)
        session['original_image_tugas1_filename'] = original_filename
        original_filename_to_process = original_filename
    elif session.get('original_image_tugas1_filename'):
        original_filename_to_process = session['original_image_tugas1_filename']
        original_path = os.path.join(app.config['UPLOAD_FOLDER'], original_filename_to_process)
        if not os.path.exists(original_path):
            session.pop('original_image_tugas1_filename', None)
            session.pop('original_url_tugas1', None)
            session.pop('processed_url_tugas1', None)
            session.pop('method_tugas1', None)
            return "Error: Gambar sebelumnya tidak ditemukan. Silakan unggah lagi.", 400
    else:
        return "Tidak ada gambar yang dipilih. Silakan unggah gambar.", 400

    method_key = 'threshold'
    final_original_path = os.path.join(app.config['UPLOAD_FOLDER'], original_filename_to_process)

    base_filename_for_output = original_filename_to_process.replace("original_tugas1_", "")
    output_filename = f"{method_key}_{base_filename_for_output}"
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
    process_image(final_original_path, output_path, method_key)

    session['original_url_tugas1'] = original_filename_to_process
    session['processed_url_tugas1'] = output_filename
    session['method_tugas1'] = method_key

    return render_template('tugas1.html',
                            original_url=original_filename_to_process,
                            processed_url=output_filename,
                            method=method_key,
                            original_image_filename_from_session=original_filename_to_process,
                            method_display=method_display)


@app.route('/upload_tugas2', methods=['POST'])
def upload_tugas2():
    original_filename_to_process = None

    if 'image' in request.files and request.files['image'].filename != '':
        f = request.files['image']
        original_filename = f"original_tugas2_{f.filename}"
        original_path = os.path.join(app.config['UPLOAD_FOLDER'], original_filename)
        f.save(original_path)
        session['original_image_tugas2_filename'] = original_filename
        original_filename_to_process = original_filename
    elif session.get('original_image_tugas2_filename'):
        original_filename_to_process = session['original_image_tugas2_filename']
        original_path = os.path.join(app.config['UPLOAD_FOLDER'], original_filename_to_process)
        if not os.path.exists(original_path):
            session.pop('original_image_tugas2_filename', None)
            session.pop('processed_url_tugas2', None)
            session.pop('original_url_tugas2', None)
            session.pop('method_tugas2', None)
            return "Error: Gambar sebelumnya tidak ditemukan. Silakan unggah lagi.", 400
    else:
        return "Tidak ada gambar yang dipilih. Silakan unggah gambar.", 400

    method_key = request.form['method']
    final_original_path = os.path.join(app.config['UPLOAD_FOLDER'], original_filename_to_process)

    base_filename_for_output = original_filename_to_process.replace("original_tugas2_", "")
    output_filename = f"{method_key}_{base_filename_for_output}"
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)

    process_image(final_original_path, output_path, method_key)

    session['original_url_tugas2'] = original_filename_to_process
    session['processed_url_tugas2'] = output_filename
    session['method_tugas2'] = method_key

    return render_template('tugas2.html',
                            original_url=original_filename_to_process,
                            processed_url=output_filename,
                            method=method_key,
                            original_image_filename_from_session=original_filename_to_process,
                            method_display=method_display)


@app.route('/upload_tugas3', methods=['POST'])
def upload_tugas3():
    original_filename_to_process = None

    if 'image' in request.files and request.files['image'].filename != '':
        f = request.files['image']
        original_filename = f"original_tugas3_{f.filename}"
        original_path = os.path.join(app.config['UPLOAD_FOLDER'], original_filename)
        f.save(original_path)
        session['original_image_tugas3_filename'] = original_filename
        original_filename_to_process = original_filename
    elif session.get('original_image_tugas3_filename'):
        original_filename_to_process = session['original_image_tugas3_filename']
        original_path = os.path.join(app.config['UPLOAD_FOLDER'], original_filename_to_process)
        if not os.path.exists(original_path):
            session.pop('original_image_tugas3_filename', None)
            session.pop('original_url_tugas3', None)
            session.pop('processed_url_tugas3', None)
            session.pop('method_tugas3', None)
            session.pop('se_type_tugas3', None)
            session.pop('se_size_tugas3', None)
            return "Error: Gambar sebelumnya tidak ditemukan. Silakan unggah lagi.", 400
    else:
        return "Tidak ada gambar yang dipilih. Silakan unggah gambar.", 400

    method_key = request.form['method']
    se_type = request.form['se_type']
    se_size_str = request.form['se_size']

    final_original_path = os.path.join(app.config['UPLOAD_FOLDER'], original_filename_to_process)
    base_filename_for_output = original_filename_to_process.replace("original_tugas3_", "")
    output_filename = f"{method_key}_{se_type}_{base_filename_for_output}"
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)

    try:
        se_size_parsed = eval(se_size_str)
    except:
        se_size_parsed = 3 if se_type in ['disk', 'diamond', 'square', 'octagon', 'sphere'] else [5,5]

    process_image(final_original_path, output_path, method_key, se_type, se_size_parsed)

    session['original_url_tugas3'] = original_filename_to_process
    session['processed_url_tugas3'] = output_filename
    session['method_tugas3'] = method_key
    session['se_type_tugas3'] = se_type
    session['se_size_tugas3'] = se_size_parsed

    return render_template('tugas3.html',
                            original_url=original_filename_to_process,
                            processed_url=output_filename,
                            method=method_key,
                            se_type=se_type,
                            se_size=se_size_parsed,
                            original_image_filename_from_session=original_filename_to_process,
                            method_display=method_display)

@app.route('/upload_tugas4', methods=['POST'])
def upload_tugas4():
    original_filename_to_process = None

    if 'image' in request.files and request.files['image'].filename != '':
        f = request.files['image']
        original_filename = f"original_tugas4_{f.filename}"
        original_path = os.path.join(app.config['UPLOAD_FOLDER'], original_filename)
        f.save(original_path)
        session['original_image_tugas4_filename'] = original_filename
        original_filename_to_process = original_filename
    elif session.get('original_image_tugas4_filename'):
        original_filename_to_process = session['original_image_tugas4_filename']
        original_path = os.path.join(app.config['UPLOAD_FOLDER'], original_filename_to_process)
        if not os.path.exists(original_path):
            session.pop('original_image_tugas4_filename', None)
            session.pop('original_url_tugas4', None)
            session.pop('processed_url_tugas4', None)
            session.pop('method_tugas4', None)
            session.pop('se_type_tugas4', None)
            session.pop('se_size_tugas4', None)
            return "Error: Gambar sebelumnya tidak ditemukan. Silakan unggah lagi.", 400
    else:
        return "Tidak ada gambar yang dipilih. Silakan unggah gambar.", 400

    method_key = request.form['method']
    se_type   = request.form.get('se_type')
    se_size_str = request.form.get('se_size')

    final_original_path = os.path.join(app.config['UPLOAD_FOLDER'], original_filename_to_process)
    base_filename_for_output = original_filename_to_process.replace("original_tugas4_", "")
    if se_type:
        output_filename = f"{method_key}_{se_type}_{base_filename_for_output}"
    else:
        output_filename = f"{method_key}_{base_filename_for_output}"
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)

    se_size_parsed = None
    if se_type and se_size_str:
        try:
            se_size_parsed = eval(se_size_str)
        except:
            se_size_parsed = 3 if se_type in ['disk', 'diamond', 'square', 'octagon', 'sphere'] else [5, 5]

    process_image(final_original_path, output_path, method_key, se_type, se_size_parsed)

    # Simpan session dan render kembali halaman
    session['original_url_tugas4'] = original_filename_to_process
    session['processed_url_tugas4'] = output_filename
    session['method_tugas4'] = method_key
    session['se_type_tugas4'] = se_type
    session['se_size_tugas4'] = se_size_parsed

    return render_template('tugas4.html',
                            original_url=original_filename_to_process,
                            processed_url=output_filename,
                            method=method_key,
                            se_type=se_type,
                            se_size=se_size_parsed,
                            original_image_filename_from_session=original_filename_to_process,
                            method_display=method_display)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)