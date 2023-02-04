# У вас есть приложение с использованием REST X, 
# где все views, а также модель находятся в одном файле. 
# 
# Необходимо сделать рефакторинг архитектуры приложения.
# Структура приложения должна быть следующего вида:
#
# constants-division
# ├── ./app.py       - Основной фаил, здесь инициализируется приложение
# ├── ./constants.py - В этот файл переместите константы
# ├── ./models.py    - В этот фаил переместите модели
# ├── ./setup_db.    - в этом файле инициализируйте базу данных для Flask
# ├── ./test.py      - Это наши тесты, запустите после самостоятельной проверки
# └── ./views
#     ├── ./views/files.py        - В эти фаилы переместите необходимые
#     └── ./views/smartphones.py    для работы class based views.
# 
# Требования к выполнению задания:
# - Приложение должно соответствовать структуре выше.
# - В файле app.py не должно быть лишних переменных.
# - Приложение должно запускаться.
# - Запрос на эндпоинт должен возвращать корректный код.
#
# Менять значения, возвращаемые view-функциями, 
# а также url-адреаса в данном задании не требуется.
# Также задание содержит упрощенный вариант сериализации/десериализации
# которым мы пользуемся только в учебных целях для сокращения объема кода.


from flask import Flask
from flask_restx import Api
from config import Config
from models import File, SmartPhone
from setup_db import db
from views.files import file_ns
from views.smartphones import sm_ns


def create_app(config: Config) -> Flask:
    application = Flask(__name__)
    application.config.from_object(config)
    application.app_context().push()
    return application


def configure_app(application: Flask):
    db.init_app(application)
    api = Api(application)
    api.add_namespace(sm_ns) #smartphones
    api.add_namespace(file_ns) #files


def load_data():
    db.create_all()

    f1 = File(id=1, name='config.cfg', path='/var/', size=500)
    f2 = File(id=2, name='run.exe', path='/var/lib/', size=500)
    sp1 = SmartPhone(id=1, name="iphone", price=100000)
    sp2 = SmartPhone(id=2, name="android", price=110000)

    with db.session.begin():
        db.session.add_all([f1, f2])
        db.session.add_all([sp1, sp2])


if __name__ == '__main__':
    app_config = Config()
    app = create_app(app_config)
    app.url_map.strict_slashes = False
    configure_app(app)
    load_data()
    app.run(host="localhost", port=10001, debug=True)

