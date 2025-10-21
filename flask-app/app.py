from flask import Flask, render_template_string, redirect, url_for
import os

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


def vulnerable_login_query(username, password):
    # This is the VULNERABLE part: direct string concatenation of user input
    # into the SQL query string.
    query = "SELECT * FROM users WHERE username = '" + username + \
            "' AND password = '" + password + "';"
    return query