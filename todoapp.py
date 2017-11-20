from flask import Flask, render_template, request, redirect
import re, pickle

app = Flask(__name__)
todo_list = []
status = ""
emailCheck = re.compile("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

class Task:
    def __init__(self, task, email, priority):
        self.task = task
        self.email = email
        self.priority = priority


@app.route('/')
def index():
    return render_template('index.html', todo_list=todo_list,
                           status=status)


@app.route('/submit', methods=['POST'])
def submit():
    global status
    task = request.form['task']
    email = request.form['email']
    priority = request.form['priority']

    if task == "":
        status = "Error: Task is required"
        return redirect("/")
    else:
        status = ""
    if not re.search(emailCheck, email):
        status = "Error: Please enter valid email address."
        return redirect("/")
    else:
        status = ""

    if priority != "High" and priority != "Medium" and priority != "Low":
        status = "Error: Please select the priority"
        return redirect("/")
    else:
        status = ""

    newtask = Task(task, email, priority)
    todo_list.append(newtask)

    return redirect("/")


@app.route('/clear', methods=['POST'])
def clear():
    del todo_list[:]
    return redirect("/")


@app.route('/delete', methods=['POST'])
def delete():
    delete_index = int(request.form['index'])
    del todo_list[delete_index]
    return redirect("/")

@app.route('/save', methods=['POST'])
def save():
    pickle.dump(todo_list, open('todoList_export.txt', 'wb'))
    return redirect("/")

if __name__ == '__main__':
    app.run()