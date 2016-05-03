# coding=utf-8
from flask import Flask, jsonify, url_for
from flask import abort
from flask import request

app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

@app.route('/hoboom/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})


@app.route('/hoboom/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = filter(lambda t: t['id'] == task_id, tasks)
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})


@app.route('/hoboom/api/v1.0/tasks', methods=['POST'])
def create_task():
    return request.json
    print request.json[ur"id"]
    if not request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title':request.json.get('title'),
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201

@app.route('/hoboom/api/v1.0/query_api', methods=['GET'])
def queryAPI():
    return url_for('get_tasks')

if __name__ == '__main__':
    app.run(debug=True, port=9600)