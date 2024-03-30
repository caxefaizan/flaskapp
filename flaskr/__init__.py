import os, json

from flask import Flask, request
from flask_socketio import SocketIO, emit, Namespace
from flaskr.db import get_db
from datetime import datetime

# class MySocketNamespace(Namespace):
#     def on_connect(self, arg):
#         print(request.event["args"]) 
#         print(f"Client {arg} connected!")

#     def on_disconnect(self, arg):
#         print(f"Client {arg} disconnected!")

#     def on_send_message(self):
#         emit('message_response', "message received")

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )
    # app.config.from_pyfile("config.py")
    
    socketio = SocketIO(app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    def writeMessageAndSendResponse(username, recipientId, message, size):
        recipient = (
            get_db()
            .execute(
                "SELECT u.*" f" FROM user u " f" WHERE u.id = '{recipientId}'",
            )
            .fetchone()
        )
        sender = (
            get_db()
            .execute(
                "SELECT u.*" f" FROM user u " f" WHERE u.username = '{username}'",
            )
            .fetchone()
        )
        db = get_db()
        db.execute(
            "INSERT INTO messages (senderId, recipientId, messageText, timeStamp)"
            " VALUES (?, ?, ?, ?)",
            (
                sender['id'],
                recipient['id'],
                message,
                datetime.now(),
            ),
        )
        db.commit()
        print("Message saved successfully")

        return blog.get_messages(sender['id'], recipientId, int(size))
    
    # socketio.on_namespace(MySocketNamespace('/test'))

    @socketio.on("clientConnect")
    def handle_my_custom_event(json):
        print('client: ' + str(json))

    @socketio.on("submitMessage")
    def handle_my_custom_event(username, rId, message, size):
        print("######",request.event["args"]) 
        messages = writeMessageAndSendResponse(username, rId, message, size)

        emit(
            "serverMessagesUpdate", 
            json.dumps(
                {
                    "action": "refresh"
                }
            ),
            namespace="kang/message",
            broadcast=True
        )

    from . import db

    db.init_app(app)

    from . import auth

    app.register_blueprint(auth.bp)

    from . import blog

    app.register_blueprint(blog.bp)
    app.add_url_rule("/", endpoint="index")

    return app
