from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

# Home
@app.route('/')
def home():
    return render_template('login.html')


# Register
@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Check if user already exists
    existing_user = cursor.execute(
        "SELECT * FROM users WHERE username=?",
        (username,)
    ).fetchone()

    if existing_user:
        conn.close()
        return "❌ Username already taken! Try another one."

    # Insert new user
    cursor.execute(
        "INSERT INTO users (username, password, score) VALUES (?, ?, 0)",
        (username, password)
    )
    conn.commit()
    conn.close()

    return redirect('/')

# Login
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    user = cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    ).fetchone()

    conn.close()

    if user:
        session['user'] = username
        session['q_index'] = 0
        session['score'] = 0
        return redirect('/quiz')
    else:
        return "Invalid credentials"


# Quiz Page
@app.route('/quiz')
def quiz():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Load questions only once
    if 'questions' not in session:
        questions = cursor.execute("SELECT * FROM questions ORDER BY RANDOM()").fetchall()
        session['questions'] = questions

    conn.close()

    q_index = session.get('q_index', 0)
    questions = session['questions']

    if q_index >= len(questions):
        return redirect('/result')

    question = questions[q_index]

    message = session.pop('message', '') 

    return render_template('quiz.html', q=question, msg=message)
# Submit Answer
@app.route('/submit', methods=['POST'])
def submit():
    selected = request.form['option']

    questions = session['questions']
    q_index = session['q_index']

    correct_answer = questions[q_index][6]

    if selected == correct_answer:
        session['score'] += 1
        session['message'] = "✅ Correct!"
    else:
        session['message'] = f"❌ Wrong! Correct answer: {correct_answer}"

    return redirect('/quiz')   # ❌ removed auto next

# NEXT BUTTON
@app.route('/next')
def next_question():
    if session['q_index'] < len(session['questions']) - 1:
        session['q_index'] += 1
    return redirect('/quiz')


# PREVIOUS BUTTON
@app.route('/prev')
def prev_question():
    if session['q_index'] > 0:
        session['q_index'] -= 1
    return redirect('/quiz')

# Result Page
@app.route('/result')
def result():
    return f"Your Score: {session['score']}"


if __name__ == '__main__':
    app.run(debug=True)