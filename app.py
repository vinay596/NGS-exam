import requests
from flask import Flask, request, jsonify, render_template, redirect, url_for
from database import fetch_questions, submit_response, calculate_marks

app = Flask(__name__)

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # TODO: Add actual user credential validation here.
        return redirect(url_for('terms_conditions'))
    return render_template('Loginpage.html')

@app.route('/terms-conditions')
def terms_conditions():
    return render_template('Termspage.html')

@app.route('/aptitude-test-start')
def aptitude_test_start():
    return render_template('AptitudeTest.html')

@app.route('/aptitude-test')
def show_aptitude_test():
    aptitude_questions = fetch_questions('aptitude')
    return render_template('AtestPage.html', questions=aptitude_questions)

@app.route('/verbal-test-start')
def verbal_test_start():
    return render_template('Verbaltest.html')

@app.route('/verbal-test')
def verbal_test():
    verbal_questions = fetch_questions('verbal')
    return render_template('Etestpage.html', questions=verbal_questions)

@app.route('/coding-test-start')
def coding_test_start():
    return render_template('codestart.html')

@app.route('/coding-test')
def coding_test():
    coding_questions = fetch_questions('coding')
    return render_template('Codetest.html', questions=coding_questions)

@app.route('/submit-answer', methods=['POST'])
def submit_answer():
    data = request.json
    student_id = data['student_id']
    question_id = data['question_id']
    selected_option = data['selected_option']
    is_correct = submit_response(student_id, question_id, selected_option)
    total_marks = calculate_marks(student_id)
    return jsonify({"is_correct": is_correct, "total_marks": total_marks})

@app.route('/execute', methods=['POST'])
def execute_code():
    data = request.json
    source_code = data['code']
    language = data['language']
    language_id = {'python': 71, 'java': 62, 'c': 50, 'c++': 54}.get(language, 71)
    payload = {
        "source_code": source_code,
        "language_id": language_id,
        "stdin": "",
        "redirect_stderr_to_stdout": True,
    }
    response = requests.post("https://api.judge0.com/submissions?base64_encoded=false&wait=true", json=payload)
    return jsonify(response.json())

@app.route('/end')
def end_page():
    return render_template('Endpage.html')

if __name__ == '__main__':
    app.run(debug=True)
