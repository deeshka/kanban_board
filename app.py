from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

#setting up the app and database 
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#creating the Task table that would store all tasks and relevant attributes
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)
    inprogress = db.Column(db.Boolean)
    notstarted = db.Column(db.Boolean)

#setting up the home page for page updates
@app.route("/")
def home():
    #creating the lists for the tasks depending on their completion status
    #this helps us display tasks on the kanban in the relevant columns (Todod, Inprogress, Completed)
    task_list = Task.query.all()
    notstarted_list = Task.query.filter_by(notstarted=True).all()
    inprogress_list = Task.query.filter_by(inprogress=True).all()
    complete_list = Task.query.filter_by(complete=True).all()
    return render_template("kanban.html", task_list=task_list, notstarted_list=notstarted_list, inprogress_list=inprogress_list, complete_list=complete_list)

#defining the route to add a new task
@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    new_task = Task(title=title, complete=False, inprogress=False, notstarted=True)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for("home"))

#updating the status of the task to transport it to the relevant column
@app.route("/update/<int:task_id>")
def update(task_id):
    #choosing the task with the relevant ID
    task = Task.query.filter_by(id=task_id).first()

    #1st if statement checks if the task is not started and if it is, it moves it to in progress
    if task.complete == False and task.inprogress == False and task.notstarted == True :
        task.complete = False 
        task.inprogress = True 
        task.notstarted = False 

    #2nd if statement checks if the task is in progress and if it is, it moves it to complete
    elif task.complete == False and task.inprogress == True and task.notstarted == False:
        task.complete = True 
        task.inprogress = False 
        task.notstarted = False

    #3rd if statement checks if the task is complete and if it is, it moves it to not started
    #this makes it possible to move the task to the beginning of the board and the to the middle and then to the end
    else: 
        task.complete = False 
        task.inprogress = False 
        task.notstarted = True

    db.session.commit()
    return redirect(url_for("home"))

#deleting the task from the database by ID which deletes it from the frontend as well
@app.route("/delete/<int:task_id>")
def delete(task_id):
    task = Task.query.filter_by(id=task_id).first()
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("home"))

#running the app and creating the database
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)