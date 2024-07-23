from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def init_db():
    try:
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS stress_levels (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question1 INTEGER,
                    question2 INTEGER,
                    question3 INTEGER,
                    question4 INTEGER,
                    question5 INTEGER,
                    question6 INTEGER,
                    question7 INTEGER,
                    question8 INTEGER,
                    question9 INTEGER,
                    question10 INTEGER,
                    question11 INTEGER,
                    question12 INTEGER,
                    question13 INTEGER,
                    question14 INTEGER,
                    question15 INTEGER,
                    question16 INTEGER,
                    question17 INTEGER,
                    question18 INTEGER,
                    question19 INTEGER,
                    question20 INTEGER,
                    question21 INTEGER,
                    question22 INTEGER,
                    question23 INTEGER,
                    question24 INTEGER,
                    question25 INTEGER,
                    question26 INTEGER,
                    question27 INTEGER,
                    question28 INTEGER,
                    question29 INTEGER,
                    question30 INTEGER
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS moods (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT,
                    mood INTEGER
                )
            ''')
            conn.commit()
        print("Database initialized successfully.")
    except Exception as e:
        print(f"Error initializing database: {e}")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/quiz')
def quiz():
    return render_template('quiz.html')

@app.route('/submit_quiz', methods=['POST'])
def submit_quiz():
    responses = []
    for i in range(1, 31):
        try:
            responses.append(int(request.form[f'q{i}']))
        except (KeyError, ValueError):
            responses.append(0)  # Default value for missing or invalid data

    try:
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO stress_levels (
                    question1, question2, question3, question4, question5, 
                    question6, question7, question8, question9, question10, 
                    question11, question12, question13, question14, question15, 
                    question16, question17, question18, question19, question20, 
                    question21, question22, question23, question24, question25, 
                    question26, question27, question28, question29, question30
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', responses)
            conn.commit()
        print("Quiz responses inserted successfully.")
    except Exception as e:
        print(f"Error inserting quiz responses: {e}")

    total_score = sum(responses)
    return render_template('results.html', stress_level=total_score, causes="Your detailed causes will be listed here.")

@app.route('/mood_tracker')
def mood_tracker():
    moods = []
    try:
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT date, mood FROM moods')
            moods = cursor.fetchall()
        print("Moods fetched successfully.")
    except Exception as e:
        print(f"Error fetching moods: {e}")
    return render_template('mood_tracker.html', moods=moods)

@app.route('/submit_mood', methods=['POST'])
def submit_mood():
    mood = int(request.form['mood'])
    date = request.form['date']
    try:
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO moods (date, mood) VALUES (?, ?)', (date, mood))
            conn.commit()
        print("Mood submitted successfully.")
    except Exception as e:
        print(f"Error submitting mood: {e}")

    moods = []
    try:
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT date, mood FROM moods')
            moods = cursor.fetchall()
        print("Moods fetched successfully.")
    except Exception as e:
        print(f"Error fetching moods: {e}")

    return render_template('mood_calendar.html', moods=moods)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)  # Changed port to 5000
