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


# --- VULNERABLE FUNCTION ---
@app.route('/welcome')
def welcome_user():
    # 1. Get untrusted user input from the URL query parameters
    user_name = request.args.get('name', 'Guest')
    
    # 2. VULNERABLE: Direct insertion of untrusted input into HTML 
    # without proper sanitization or auto-escaping.
    # In some contexts (like using certain methods or disabling auto-escaping), 
    # the templating engine can be tricked or explicitly told to render raw content.
    
    # CodeQL often flags sinks like 'render_template_string' when they directly
    # process unsanitized user input (the 'user_name' variable).
    
    html_template = f"<h1>Welcome, {user_name}!</h1>"
    
    # If a malicious user passes the payload: ?name=<script>alert('XSS')</script>
    # The resulting page will execute the script.
    return render_template_string(html_template)

if __name__ == '__main__':
    # This snippet is for demonstration; do not run with debug=True in production.
    app.run(debug=True)