import app
import sys
import unittest
from pathlib import Path
from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy
import setup_db
from sqlalchemy import Integer, String
import os

project_name = Path(os.path.abspath(__file__)).parent.parent.parent.name
cwd = Path.cwd()
parts = cwd.parts
basefolder_index = parts.index(project_name)
basepath = Path(*parts[:basefolder_index + 1])
sys.path.append(str(basepath))
from ttools.skyprotests.tests import SkyproTestCase  # noqa: E402
from ttools.skyprotests.tests_mixins import (
    ResponseTestsMixin, DataBaseTestsMixin)  # noqa: E402


class StructureTestCase(SkyproTestCase):

    def test_views_files_has_namespace_vars(self):
        from views import books
        from views import reviews
        namespaces_vars = ['book_ns', 'review_ns', 'app', 'db']
        for var, module in zip (namespaces_vars, [books, reviews, app, setup_db]):   
            self.assertTrue(
                hasattr(module, var), 
                f'%@ Проверте что модуль {module} содержит переменную {var}.'
                'Также обратите внимание на список переменных требуемых '
                'для корректной работы тестов.'
            )

    def test_book_ns_has_correct_resources(self):
        from views import books
        ns_var = books.book_ns
        namespace = ns_var.name
        resources_list = [res.urls[0] for res in ns_var.resources]
        expected_resources = ['/', '/<int:bid>']
        for expected in expected_resources:
            self.assertIn(expected, resources_list,
            '%@ Проверьте что фаил books содержит view-функцию для '
            f' адреса /"{namespace}{expected}"')

    def test_book_ns_has_correct_resources(self):
        from views import reviews
        ns_var = reviews.review_ns
        namespace = ns_var.name
        resources_list = [res.urls[0] for res in ns_var.resources]
        expected_resources = ['/', '/<int:rid>']
        for expected in expected_resources:
            self.assertIn(expected, resources_list,
            '%@ Проверьте что фаил books содержит view-функцию для '
            f' адреса /"{namespace}{expected}"')


class DataBaseTestCase(SkyproTestCase):
    def setUp(self):
        self.app = app.app
        self.db = app.db
    
    def test_tables_exists(self):
        tablenames = ['books', 'reviews']
        current_tables = self.db.metadata.tables.keys()
        for table in tablenames:
            self.assertIn(
                table, current_tables,
                f"%@Проверьте, что создали таблицу {table}")


class ViewsTestCase(SkyproTestCase,
                    ResponseTestsMixin):
    CREATE_BOOKS = ("CREATE TABLE books ("
                    "id integer PRIMARY KEY, "
                    "name varchar(300), "
                    "author varchar(300), "
                    "year integer, "
                    "pages ingeger)")
    INSERT_BOOKS = ("INSERT INTO books"
                    "('name', 'author', 'year', 'pages') VALUES "
                    "('newbook1', 'newauthor1', 1950, 1024),"
                    "('newbook2', 'newauthor2', 1990, 512)")

    CREATE_REVIEW = ("CREATE TABLE reviews ("
                     "id integer PRIMARY KEY, "
                     "user varchar(300), "
                     "rating integer, "
                     "book_id ingeger)")
    INSERT_REVIEWS = ("INSERT INTO reviews"
                      "('user', 'rating', 'book_id') VALUES "
                      "('user1', 5, 1),"
                      "('user2', 3, 2)")
    
    BOOK_INSTANCE = {
        "name": "test_book",
        "author": "test_author",
        "year": 1500,
        "pages": 1100
    }

    REVIEW_INSTANCE = {
        "user": "test_user",
        "rating": 5,
        "book_id": 1
    }
    
    def setUp(self):
        self.review1 = {'id': 1, 'book_id': 1, 'user': 'user1', 'rating': 5}
        self.review2 = {'id': 2, 'book_id': 2, 'user': 'user2', 'rating': 3}
        self.book1 = {'id': 1, 'author': 'newauthor1', 'year': 1950, 
                      'pages': 1024, 'name': 'newbook1'}
        self.book2 = {'id': 2, 'author': 'newauthor2', 'year': 1990, 
                      'pages': 512, 'name': 'newbook2'}
        self.expected_review_instance = {**self.REVIEW_INSTANCE}
        self.expected_review_instance['id'] = 1
        self.app = app.app
        self.db = app.db
        self.app.app_context().push()
        self.student_app = self.app.test_client()
        self.db.drop_all()
        with self.app.app_context():
            with self.db.session.begin():
                self.db.session.execute(text(self.CREATE_BOOKS))
                self.db.session.execute(text(self.INSERT_BOOKS))
                self.db.session.execute(text(self.CREATE_REVIEW))
                self.db.session.execute(text(self.INSERT_REVIEWS))


    def test_view_books_get_is_available_and_works_correct(self):
        url = '/books/'
        test_options = {
            "url": url,
            "method": 'GET',
            "code": [200],
            "student_response": self.student_app.get(
                url, json=""),
            "expected": list,
            "answer": [self.book1, self.book2]
        }
        self.check_status_code_jsonify_and_expected(**test_options)

    def test_view_books_post_is_available_and_works_correct(self):
        url = '/books/'
        method = 'POST'
        test_options = {
            "url": url,
            "method": method,
            "code": [200, 201, 204],
            "student_response": self.student_app.post(
                url, json=self.BOOK_INSTANCE),
        }
        self.check_status_code_jsonify_and_expected(**test_options)
        # options for code below:
        new_id = 3
        tablename = 'books'
        example_instance = self.BOOK_INSTANCE
        ### code below can be reused
        instance = self.db.session.execute(
            f"SELECT * FROM {tablename} where `id` = {new_id}").fetchall()
        self.assertGreater(
            len(instance), 0,
            f'%@Проверьте что при {method} запросе в таблице {tablename} создаётся запись')
        example_instance['id'] = new_id
        for key in example_instance.keys():
            self.assertIn(example_instance[key], *instance,
            f"%@Проверьте что корректно присваивается значение поля {key} в "
            f"таблице {tablename} при {method}-запросе на адрес {url}")

    def test_view_books_id_get_is_available_and_works_correct(self):
        url = '/books/1'
        test_options = {
            "url": url,
            "method": 'GET',
            "code": [200],
            "student_response": self.student_app.get(
                url, json=""),
            "expected": dict
        }
        self.check_status_code_jsonify_and_expected(**test_options)

    def test_view_books_id_put_is_available_and_works_correct(self):
        url = '/books/1'
        method = 'PUT'
        test_options = {
            "url": url,
            "method": 'PUT',
            "code": [200, 204],
            "student_response": self.student_app.put(
                url, json=self.BOOK_INSTANCE),
        }
        self.check_status_code_jsonify_and_expected(**test_options)
        # options:
        new_id = 1
        tablename = 'books'
        example_instance = {**self.BOOK_INSTANCE}
        ### code below can be reused
        instance = self.db.session.execute(
            f"SELECT * FROM {tablename} where `id` = {new_id}").fetchall()
        self.assertGreater(
            len(instance), 0,
            f'%@Проверьте что при {method} запросе в таблице {tablename} создаётся запись')
        example_instance['id'] = new_id
        for key in example_instance.keys():
            self.assertIn(example_instance[key], *instance,
            f"%@Проверьте что корректно присваивается значение поля {key} в "
            f"таблице {tablename} при {method}-запросе на адрес {url}")

    def test_view_books_id_delete_is_available_and_works_correct(self):
        url = '/books/1'
        method = 'DELETE'
        test_options = {
            "url": url,
            "method": method,
            "code": [200, 204],
            "student_response": self.student_app.delete(
                url, json=""),
        }
        self.check_status_code_jsonify_and_expected(**test_options)
        # options:
        new_id = 1
        tablename = 'books'
        ### code below can be reused
        instance = self.db.session.execute(
            f"SELECT * FROM {tablename} where `id` = {new_id}").fetchall()
        self.assertEqual(
            len(instance), 0,
            f'%@Проверьте что при {method} запросе в таблице {tablename} удаляется запись')

    def test_view_review_get_is_available_and_works_correct(self):
        url = '/reviews/'
        test_options = {
            "url": url,
            "method": 'GET',
            "code": [200],
            "student_response": self.student_app.get(
                url, json=""),
            "expected": list,
            "answer": [self.review1, self.review2]
        }
        self.check_status_code_jsonify_and_expected(**test_options)

    def test_view_review_post_is_available_and_works_correct(self):
        url = '/reviews/'
        method = 'POST'
        test_options = {
            "url": url,
            "method": method,
            "code": [200, 201, 204],
            "student_response": self.student_app.post(
                url, json=self.REVIEW_INSTANCE),
        }
        self.check_status_code_jsonify_and_expected(**test_options)
        # options:
        new_id = 3
        tablename = 'reviews'
        example_instance = {**self.REVIEW_INSTANCE}
        ###
        instance = self.db.session.execute(
            f"SELECT * FROM {tablename} where `id` = {new_id}").fetchall()
        self.assertGreater(
            len(instance), 0,
            f'%@Проверьте что при {method} запросе в таблице {tablename} создаётся запись')
        example_instance['id'] = new_id
        for key in example_instance.keys():
            self.assertIn(example_instance[key], *instance,
            f"%@Проверьте что корректно присваивается значение поля {key} в "
            f"таблице {tablename} при {method}-запросе на адрес {url}")

    def test_view_review_id_get_is_available_and_works_correct(self):
        url = '/reviews/1'
        test_options = {
            "url": url,
            "method": 'GET',
            "code": [200],
            "student_response": self.student_app.get(
                url, json=""),
            "expected": dict
        }
        self.check_status_code_jsonify_and_expected(**test_options)

    def test_view_review_id_put_is_available_and_works_correct(self):
        url = '/reviews/1'
        method = 'PUT'
        test_options = {
            "url": url,
            "method": method,
            "code": [200, 204],
            "student_response": self.student_app.put(
                url, json=self.REVIEW_INSTANCE)
        }
        self.check_status_code_jsonify_and_expected(**test_options)
        # options for code below:
        new_id = 1
        tablename = 'reviews'
        example_instance = {**self.REVIEW_INSTANCE}
        ### code below can be reused
        instance = self.db.session.execute(
            f"SELECT * FROM {tablename} where `id` = {new_id}").fetchall()
        self.assertGreater(
            len(instance), 0,
            f'%@Проверьте что при {method} запросе в таблице {tablename} создаётся запись')
        example_instance['id'] = new_id
        for key in example_instance.keys():
            self.assertIn(example_instance[key], *instance,
            f"%@Проверьте что корректно присваивается значение поля {key} в "
            f"таблице {tablename} при {method}-запросе на адрес {url}")
    
    def test_view_review_id_delete_is_available_and_works_correct(self):
        url = '/reviews/1'
        method = 'DELETE'
        test_options = {
            "url": url,
            "method": method,
            "code": [200, 204],
            "student_response": self.student_app.delete(
                url, json="")
        }
        self.check_status_code_jsonify_and_expected(**test_options)
        # options:
        new_id = 1
        tablename = 'reviews'
        ### code below can be reused
        instance = self.db.session.execute(
            f"SELECT * FROM {tablename} where `id` = {new_id}").fetchall()
        self.assertEqual(
            len(instance), 0,
            f'%@Проверьте что при {method} запросе в таблице {tablename} удаляется запись')

    def tearDown(self):
        self.db.drop_all()
        self.db.session.close()

if __name__ == "__main__":
    unittest.main()