from flask import Flask
from flask_backend.models import db
from flask_backend.routes import routes


# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

# # initialize database
# db.init_app(app)

# # register blueprint for routes
# app.register_blueprint(routes)

# if __name__ == '__main__':
#     with app.app_context():
#         db.create_all()
#     app.run(port=5000)

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_data.db'

    # initialize database
    db.init_app(app)

    # register blueprint for routes
    app.register_blueprint(routes)

    # create tables
    with app.app_context():
        db.create_all()

    return app