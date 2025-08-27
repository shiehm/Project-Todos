from uuid import uuid4
from flask import (
    flash,
    Flask,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from todos.utils import error_for_list_title
from werkzeug.exceptions import NotFound

app = Flask(__name__)
app.secret_key = 'secret1'

def find_list_by_id(list_id, lists):
    return next((lst for lst in lists if lst['id'] == list_id), None)

@app.before_request
def initialize_session():
    if 'lists' not in session:
        session['lists'] = []

@app.route("/")
def index():
    return redirect(url_for('get_lists'))

@app.route("/lists/new")
def add_todo_list():
    return render_template('new_list.html')

# Render the list of todo lists
@app.route("/lists")
def get_lists():
    return render_template('lists.html', lists=session['lists'])

# Create a new todo list
@app.route("/lists", methods=["POST"])
def create_list():
    title = request.form["list_title"].strip()
    
    error = error_for_list_title(title, session['lists'])
    if error:
        flash(error, "error")
        return render_template('new_list.html', title=title)

    session['lists'].append({
        'id': str(uuid4()),
        'title': title,
        'todos': [],
    })
    flash("The list has been created.", "success")
    session.modified = True
    return redirect(url_for('get_lists'))

@app.route('/lists/<list_id>')
def show_list(list_id):
    lst = find_list_by_id(list_id, session['lists'])
    if not lst:
        raise NotFound(description="List not found.")
    
    return render_template('list.html', lst=lst)

if __name__ == "__main__":
    app.run(debug=True, port=5003)