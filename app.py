from flask import Flask, request, render_template, flash, redirect, url_for
import PyPDF2
import os

app = Flask(__name__)
app.secret_key = 'AIzaSyDlBNc98LOQFujLs_8TAc3MXaxQmDpy1dk'

def extract_text_from_pdf(file_path):
    text = ''
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text

def generate_answer(document_text, question):
    # Placeholder for language model integration
    # For demonstration, we'll return a dummy answer
    return f"Answer to '{question}' based on the document."

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'pdf_file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['pdf_file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            file_path = os.path.join('uploads', file.filename)
            file.save(file_path)
            document_text = extract_text_from_pdf(file_path)
            question = request.form['question']
            answer = generate_answer(document_text, question)
            return render_template('result.html', question=question, answer=answer)
    return render_template('index.html')
