from flask import Flask
from flask_restx import Api

from setup_db import db
from views.books import book_ns
from models import Book

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    register_extensions(app)
    return app


def register_extensions(app):
    db.init_app(app)
    api = Api(app)
    api.add_namespace(book_ns)
    create_data(app, db)


def create_data(app, db):
    with app.app_context():
        db.create_all()
        b1 = Book(id=1, name="Гарри Поттер и Тайная Комната",   # Формируем тестовую БД   
                  author="Джоан Роулинг", year=1990)            # чтобы можно было
        b2 = Book(id=2, name="Граф Монте-Кристо",               # самостоятельно проверить 
                  author="Александр Дюма", year=1844)           # работу эндпоинтов
        with db.session.begin():
            db.session.add_all([b1, b2])


app = create_app()
app.debug = True

if __name__ == '__main__':
    app.run(host="localhost", port=10001, debug=True)

