from flask import Flask, render_template, request, redirect, url_for
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///description.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'jpeg', 'png', 'jpg', 'gif'}

class Description(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    explain = db.Column(db.String(255), nullable=False)
    filename = db.Column(db.String(255), nullable=False)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def get_uploaded_data():
    uploaded_data = []
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        if allowed_file(filename):
            uploaded_data.append({'filename': filename})
    return uploaded_data

@app.route('/upload-form')
def form():
    return render_template('form.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    text = request.form['text']
    explain = request.form['explain']

    if file:
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        data = Description(text=text, filename=filename, explain=explain)
        db.session.add(data)
        db.session.commit()
        displayData = Description.query.all()
        return redirect(url_for('index', displayData=displayData))
    else:
        return 'Invalid file extension.'

@app.route('/')
def index():
    displayData = Description.query.all()
    uploaded_data = get_uploaded_data()
    return render_template('index.html', displayData=displayData, uploaded_data=uploaded_data)

@app.route('/delete/<int:id>')
def delete(id):
    data = Description.query.get(id)
    if data:
        db.session.delete(data)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/blog')
def blog():
    displayData = Description.query.all()
    uploaded_data = get_uploaded_data()
    return render_template('blog.html', displayData=displayData, uploaded_data=uploaded_data)

if __name__ == '__main__':
    app.run(debug=True)
