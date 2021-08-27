from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)

MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD')

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:{MYSQL_PASSWORD}@localhost/flaskmysql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
marshmallow = Marshmallow(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70), unique=True)
    description = db.Column(db.String(100))

    def __init__(self, title, description):
        self.title = title
        self.description = description

db.create_all()

class TaskSchema(marshmallow.Schema):
    class Meta:
        fields = ('id', 'title', 'description')

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

@app.route('/tasks/', methods=['POST'])
def create_task():
    title = request.json['title']
    description = request.json['description']

    new_task = Task(title, description)
    db.session.add(new_task)
    db.session.commit()
    
    return task_schema.jsonify(new_task)

@app.route('/tasks/', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    result = tasks_schema.dump(tasks)
    
    return jsonify(result)

@app.route('/tasks/<id>/', methods=['GET'])
def get_task(id):
    task = Task.query.get(id)
    result = task_schema.dump(task)
    
    return jsonify(result)

@app.route('/tasks/<id>/', methods=['PUT'])
def update_task(id):
    task = Task.query.get(id)
    
    title = request.json['title'] 
    description = request.json['description']

    task.title = title
    task.desciption = description

    db.session.commit()
    result = task_schema.dump(task)

    return jsonify(result)

@app.route('/tasks/<id>/', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get(id)
    db.session.delete(task)
    db.session.commit()

    result = task_schema.dump(task)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)

