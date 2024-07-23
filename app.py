from flask import Flask, request, render_template, redirect, url_for
import sqlite3
import datetime

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('rose.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS moods (date TEXT, mood INTEGER)''')
    conn.commit()
    conn.close()

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Quiz route
@app.route('/quiz')
def quiz():
    return render_template('quiz.html')

# Quiz submission route
@app.route('/submit_quiz', methods=['POST'])
def submit_quiz():
    answers = request.form.to_dict()
    stress_level, causes = assess_stress(answers)
    return render_template('results.html', stress_level=stress_level, causes=causes)

def assess_stress(answers):
    # Dummy logic to assess stress levels and identify causes
    stress_level = sum(int(value) for value in answers.values()) // len(answers)
    causes = "Sample cause based on answers"
    return stress_level, causes

# Mood tracker route
@app.route('/mood_tracker')
def mood_tracker():
    conn = sqlite3.connect('rose.db')
    c = conn.cursor()
    c.execute('SELECT * FROM moods')
    moods = c.fetchall()
    conn.close()
    return render_template('mood_tracker.html', moods=moods)

# Mood submission route
@app.route('/submit_mood', methods=['POST'])
def submit_mood():
    mood = request.form.get('mood')
    date = datetime.date.today().strftime('%Y-%m-%d')
    conn = sqlite3.connect('rose.db')
    c = conn.cursor()
    c.execute('INSERT INTO moods (date, mood) VALUES (?, ?)', (date, mood))
    conn.commit()
    conn.close()
    return redirect(url_for('mood_tracker'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
