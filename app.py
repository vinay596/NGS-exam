from flask import Flask, render_template, redirect, url_for
from database import fetch_questions

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('Loginpage.html')

@app.route('/Termspage')
def terms():
    return render_template('Termspage.html')

@app.route('/test_start')
def test_start():
    return render_template('AptitudeTest.html')

@app.route('/aptitude_test')
def aptitude_test():
    questions = fetch_questions()
    if questions:
        first_question = {
            'id': questions[0][0],
            'question_text': questions[0][1],
            'option_a': questions[0][2],
            'option_b': questions[0][3],
            'option_c': questions[0][4],
            'option_d': questions[0][5],
            'correct_answer': questions[0][6]
        }
    else:
        first_question = None
    return render_template('AtestPage.html', question=first_question)

if __name__ == '__main__':
    app.run(debug=True)
