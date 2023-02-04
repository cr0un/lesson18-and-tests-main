
from flask import Flask
from flask_restx import Api

from models import SmartPhone, File
from setup_db import db
from views.smartphones import sm_ns
from views.files import file_ns


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    register_extensions(app)
    return app


def register_extensions(app):
    db.init_app(app)
    api = Api(app)
    api.add_namespace(sm_ns)
    api.add_namespace(file_ns)
    create_data(app, db)

def create_data(app, db):
    with app.app_context():
        db.create_all()
        sp1 = SmartPhone(id=1, name="iphone", price=100000)
        sp2 = SmartPhone(id=2, name="android", price=110000)
        f1 = File(id=1, name='config.cfg', path='/var/', size=500)
        f2 = File(id=2, name='run.exe', path='/var/lib/', size=500)
        with db.session.begin():
            db.session.add_all([f1, f2])
            db.session.add_all([sp1, sp2])

app = create_app()
app.debug = True

if __name__ == '__main__':
    app.run(host="localhost", port=10001, debug=True)




