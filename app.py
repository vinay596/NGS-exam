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
    coding_questions = fetch_questions('coding1')
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
def compare_code():
    data = request.json
    question_id = data['question_id']
    student_code = data['code']
    language = data['language']
    
    # Fetch the correct solution from the database based on the question ID
    db_connection = get_db_connection()
    cursor = db_connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM questions WHERE id = %s", (question_id,))
    question = cursor.fetchone()
    db_connection.close()
    
    # Determine the solution column based on the selected language
    solution_column = f"{language}_solution"
    correct_solution = question.get(solution_column)
    
    # Compare the student's code with the correct solution
    if student_code.strip() == correct_solution.strip():
        return jsonify({"message": "Executed successfully", "is_correct": True})
    else:
        return jsonify({"message": "Error in execution", "is_correct": False})

@app.route('/end')
def end_page():
    return render_template('Endpage.html')

if __name__ == '__main__':
    app.run(debug=True)
