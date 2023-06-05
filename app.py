from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'jpeg', 'png', 'jpg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def get_uploaded_data():
    uploaded_data = []
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        if allowed_file(filename):
            uploaded_data.append({'filename': filename})
    return uploaded_data

# @app.route('/')
# def index():
#     return render_template('index.html')
@app.route('/upload-form')
def form():
    return render_template('form.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    text = request.form['text']

    if file and allowed_file(file.filename):
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('index'))
    else:
        return 'Invalid file extension.'

@app.route('/')
def index():
    uploaded_data = get_uploaded_data()
    return render_template('index.html', uploaded_data=uploaded_data)

if __name__ == '__main__':
    app.run()
