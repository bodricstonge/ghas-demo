from flask import Flask, render_template_string, redirect, url_for
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


conn = sqlite3.connect('example.db')
cursor = conn.cursor()

# 1. Simulate a request handler for a vulnerable endpoint
def user_search_endpoint():
    # 2. Get untrusted input (this is the 'tainted' data source)
    user_id = request.args.get('id')

    # 3. VULNERABLE SINK: Directly concatenating the untrusted input 
    # into the SQL query string.
    # CodeQL will identify the flow of data from 'request.args.get' (source)
    # to the string concatenation inside the 'query' variable (sink).
    query = "SELECT username, email FROM users WHERE id = " + user_id + ";"
    
    # 4. Execute the query
    cursor.execute(query)
    
    return "Query executed."