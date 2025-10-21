from flask import Flask, request, render_template_string, redirect, url_for
import os
import sqlite3

app = Flask(__name__)
COUNT_FILE = 'race_count.txt'

def get_count():
    if not os.path.exists(COUNT_FILE):
        return 0
    with open(COUNT_FILE, 'r') as f:
        return int(f.read() or 0)

def set_count(count):
    with open(COUNT_FILE, 'w') as f:
        f.write(str(count))

@app.route('/')
def index():
    count = get_count()
    return render_template_string('''
        <h1>Races Run: {{count}}</h1>
        <form action="/add" method="post">
            <button type="submit">Add Race</button>
        </form>
    ''', count=count)

@app.route('/add', methods=['POST'])
def add():
    count = get_count() + 1
    set_count(count)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

# CodeQL recognizes this as a database connection context.
conn = sqlite3.connect('example.db') 
cursor = conn.cursor()

def user_search_endpoint():
    user_id = request.args.get('id')
    # This is the VULNERABLE pattern CodeQL looks for
    query = "SELECT username, email FROM users WHERE id = " + user_id + ";"
    cursor.execute(query) # CodeQL recognizes this as the dangerous 'sink'.
    return "Query executed."