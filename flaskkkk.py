# from flask import Flask, request, jsonify
# from flask_sqlalchemy import SQLAlchemy
# from flask_socketio import SocketIO, send
# from flask_cors import CORS

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# app.config['SECRET_KEY'] = 'your_secret_key'

# db = SQLAlchemy(app)
# socketio = SocketIO(app, cors_allowed_origins="*")  # Allow CORS
# CORS(app)  # Enable CORS for the Flask app

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(50), unique=True, nullable=False)
#     password = db.Column(db.String(80), nullable=False)

# @app.route('/register', methods=['POST'])
# def register():
#     data = request.get_json()
#     if not data or not 'username' in data or not 'password' in data:
#         return jsonify({'message': 'Invalid input'}), 400
    
#     hashed_password = generate_password_hash(data['password'], method='sha256')
#     new_user = User(username=data['username'], password=hashed_password)
    
#     try:
#         db.session.add(new_user)
#         db.session.commit()
#         return jsonify({'message': 'User registered successfully'}), 201
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'message': 'User registration failed', 'error': str(e)}), 500

# # Flask-SocketIO event handler for chat messages
# @socketio.on('message')
# def handle_message(msg):
#     print('Message:', msg)
#     send(msg, broadcast=True)  # Broadcast the message to all clients

# if __name__ == '__main__':
#     with app.app_context():
#         db.create_all()  # Ensure tables are created
#     socketio.run(app, debug=True, host='0.0.0.0', port=5000)


from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_socketio import SocketIO, emit
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'your_secret_key'

# Initialize CORS to allow requests from any origin
CORS(app)

db = SQLAlchemy(app)
socketio = SocketIO(app, cors_allowed_origins="*")

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(200), nullable=False)

# Flask-SocketIO event handler for chat messages
@socketio.on('message')
def handle_message(data):
    username = data.get('username')
    message_content = data.get('message')
    print(username)
    if username and message_content:
        # Save the message to the database
        new_message = Message(username=username, content=message_content)
        db.session.add(new_message)
        db.session.commit()
        
        # Broadcast the message to all connected clients
        emit('message', {'username': username, 'message': message_content}, broadcast=True)

@socketio.on('connect')
def handle_connect():
    # Load the previous messages from the database when a user connects
    messages = Message.query.all()
    message_list = [{'username': msg.username, 'message': msg.content} for msg in messages]
    
    # Send the previous messages to the newly connected client
    emit('previous_messages', message_list)

if __name__ == '__main__':
    # Create the database tables within an app context
    with app.app_context():
        db.create_all()
    
    # Run the Flask app with SocketIO and CORS enabled
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)


# from flask import Flask, request, jsonify, session
# from flask_sqlalchemy import SQLAlchemy
# from werkzeug.security import generate_password_hash, check_password_hash
# from flask_socketio import SocketIO, emit
# from flask_cors import CORS

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# app.config['SECRET_KEY'] = 'your_secret_key'
# app.config['SESSION_TYPE'] = 'filesystem'

# db = SQLAlchemy(app)
# socketio = SocketIO(app, cors_allowed_origins="*")
# CORS(app)

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(50), unique=True, nullable=False)
#     password = db.Column(db.String(80), nullable=False)

# class Message(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(50), nullable=False)
#     content = db.Column(db.String(200), nullable=False)

# @app.route('/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     if not data or not 'username' in data or not 'password' in data:
#         return jsonify({'message': 'Invalid input'}), 400
    
#     user = User.query.filter_by(username=data['username']).first()
    
#     if user and user.password == data['password']:
#         session['username'] = user.username
#         return jsonify({'message': 'Login successful', 'username': user.username}), 200
#     else:
#         return jsonify({'message': 'Login failed'}), 401

# @app.route('/logout', methods=['POST'])
# def logout():
#     session.pop('username', None)
#     return jsonify({'message': 'Logged out'}), 200

# @socketio.on('message')
# def handle_message(data):
#     username = session.get('username')
#     print(username)
    
#     if not username:
#         print("User not logged in")
#         emit('error', {'message': 'User not logged in'})
#         # return
    
#     message_content = data.get('message')
    
#     if message_content:
#         new_message = Message(username=username, content=message_content)
#         db.session.add(new_message)
#         db.session.commit()
        
#         emit('message', {'username': username, 'message': message_content}, broadcast=True)

# @app.route('/register', methods=['POST'])
# def register():
#     print(request.data, " hiihih")
#     data = request.get_json()
#     if not data or 'username' not in data or 'password' not in data:
#         return jsonify({'message': 'Invalid input'}), 400
    
#     new_user = User(username=data['username'], password=data['password'])
    
#     try:
#         db.session.add(new_user)
#         db.session.commit()
#         return jsonify({'message': 'User registered successfully'}), 201
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'message': 'User registration failed', 'error': str(e)}), 500


# @socketio.on('connect')
# def handle_connect():
#     messages = Message.query.all()
#     message_list = [{'username': msg.username, 'message': msg.content} for msg in messages]
#     emit('previous_messages', message_list)

# if __name__ == '__main__':
#     with app.app_context():
#         db.create_all()
#     socketio.run(app, debug=True)
