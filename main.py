from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from bson import ObjectId
import os

app = Flask(__name__)

# Конфигурация приложения и базы данных MongoDB
app.config['MONGO_URI'] = os.getenv('MONGO_URI', 'mongodb://localhost:27017/tasktracker')
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'

mongo = PyMongo(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Регистрация пользователя
@app.route('/register', methods=['POST'])
def register():
    users = mongo.db.users
    data = request.get_json()
    existing_user = users.find_one({'username': data['username']})

    if existing_user:
        return jsonify({'message': 'Username already exists'}), 400

    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = {
        'username': data['username'],
        'password': hashed_password
    }
    users.insert_one(new_user)
    return jsonify({'message': 'User registered successfully'}), 201

# Аутентификация пользователя
@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    data = request.get_json()
    user = users.find_one({'username': data['username']})

    if user and bcrypt.check_password_hash(user['password'], data['password']):
        access_token = create_access_token(identity=str(user['_id']))
        return jsonify({'access_token': access_token}), 200

    return jsonify({'message': 'Invalid credentials'}), 401

# Управление проектами
@app.route('/projects', methods=['GET', 'POST'])
@jwt_required()
def manage_projects():
    users = mongo.db.users
    projects = mongo.db.projects
    current_user_id = ObjectId(get_jwt_identity())

    if request.method == 'POST':
        data = request.get_json()
        new_project = {
            'name': data['name'],
            'description': data.get('description', ''),
            'user_id': current_user_id
        }
        projects.insert_one(new_project)
        return jsonify({'message': 'Project created'}), 201

    user_projects = projects.find({'user_id': current_user_id})
    return jsonify([
        {'id': str(project['_id']), 'name': project['name'], 'description': project['description']}
        for project in user_projects
    ])

# Управление задачами
@app.route('/tasks', methods=['GET', 'POST'])
@jwt_required()
def manage_tasks():
    tasks = mongo.db.tasks
    projects = mongo.db.projects
    current_user_id = ObjectId(get_jwt_identity())

    if request.method == 'POST':
        data = request.get_json()
        new_task = {
            'title': data['title'],
            'description': data.get('description', ''),
            'status': data.get('status', 'To Do'),
            'project_id': ObjectId(data['project_id']),
            'assigned_to': data.get('assigned_to')
        }
        tasks.insert_one(new_task)
        return jsonify({'message': 'Task created'}), 201

    user_tasks = tasks.find({'project_id': {'$in': [project['_id'] for project in projects.find({'user_id': current_user_id})]}})
    return jsonify([
        {'id': str(task['_id']), 'title': task['title'], 'description': task['description'], 'status': task['status'], 'project_id': str(task['project_id']), 'assigned_to': task.get('assigned_to')}
        for task in user_tasks
    ])

# Обновление задачи
@app.route('/tasks/<string:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    tasks = mongo.db.tasks
    task = tasks.find_one({'_id': ObjectId(task_id)})
    if not task:
        return jsonify({'message': 'Task not found'}), 404

    data = request.get_json()
    task['title'] = data.get('title', task['title'])
    task['description'] = data.get('description', task['description'])
    task['status'] = data.get('status', task['status'])
    task['assigned_to'] = data.get('assigned_to', task.get('assigned_to'))
    tasks.update_one({'_id': ObjectId(task_id)}, {'$set': task})
    return jsonify({'message': 'Task updated'}), 200

# Добавление комментария к задаче
@app.route('/comments', methods=['POST'])
@jwt_required()
def add_comment():
    comments = mongo.db.comments
    data = request.get_json()
    new_comment = {
        'content': data['content'],
        'task_id': ObjectId(data['task_id']),
        'user_id': ObjectId(get_jwt_identity())
    }
    comments.insert_one(new_comment)
    return jsonify({'message': 'Comment added'}), 201

# Получение комментариев к задаче
@app.route('/comments/<string:task_id>', methods=['GET'])
@jwt_required()
def get_comments(task_id):
    comments = mongo.db.comments.find({'task_id': ObjectId(task_id)})
    return jsonify([
        {'id': str(comment['_id']), 'content': comment['content'], 'user_id': str(comment['user_id'])}
        for comment in comments
    ])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
