
from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('students.db')
    conn.row_factory = sqlite3.Row
    return conn

# Initialize DB
with get_db() as conn:
    conn.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            department TEXT
        )
    ''')

@app.route('/')
def index():
    conn = get_db()
    try:
        students = conn.execute('SELECT * FROM students').fetchall()
        return render_template('index.html', students=students)
    finally:
        conn.close()

@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    age = int(request.form['age'])
    dept = request.form['department']
    conn = get_db()
    try:
        conn.execute('INSERT INTO students (name, age, department) VALUES (?, ?, ?)', (name, age, dept))
        conn.commit()
    finally:
        conn.close()
    return redirect('/')

@app.route('/edit/<int:id>')
def edit(id):
    conn = get_db()
    try:
        student = conn.execute('SELECT * FROM students WHERE id=?', (id,)).fetchone()
        return render_template('edit.html', student=student)
    finally:
        conn.close()

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    name = request.form['name']
    age = int(request.form['age'])
    dept = request.form['department']
    conn = get_db()
    try:
        conn.execute('UPDATE students SET name=?, age=?, department=? WHERE id=?', (name, age, dept, id))
        conn.commit()
    finally:
        conn.close()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db()
    try:
        conn.execute('DELETE FROM students WHERE id=?', (id,))
        conn.commit()
    finally:
        conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
