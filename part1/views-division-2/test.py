import app
import sys
import unittest
from pathlib import Path
import os


project_name = Path(os.path.abspath('/Users/valeriy/lesson18-and-tests-main/part1/views-division-2')).parent.parent.parent.name
cwd = Path.cwd()
parts = cwd.parts
basefolder_index = parts.index(project_name)
basepath = Path(*parts[:basefolder_index + 1])
sys.path.append(str(basepath))
from ttools.skyprotests.tests import SkyproTestCase  # noqa: E402
from ttools.skyprotests.tests_mixins import ResponseTestsMixin  # noqa: E402


class ArchitectureTestCase(SkyproTestCase):
    def setUp(self):
        self.checkpath = basepath.joinpath('part1', 'views-division-2')

    def test_folder_views_is_created(self):
        folder = 'views'
        self.assertTrue(os.path.exists(self.checkpath.joinpath(folder)),
        f"%@ Проверьте что создали папку {folder}")

    def test_file_views_is_created(self):
        files = ['models.py', 'setup_db.py']
        for file in files:
            self.assertTrue(os.path.exists(self.checkpath.joinpath(file)),
            f"%@ Проверьте что создали файл {file} в корне папки приложения")

    def test_file_views_is_created(self):
        folder = 'views'
        file = 'views/books.py'
        self.assertTrue(os.path.exists(self.checkpath.joinpath(folder, file)),
        f"%@ Проверьте что создали файл {file} в папке views")
    
    def test_books_file_has_book_ns(self):
        from views import books
        self.assertTrue(
            hasattr(books, 'book_ns'), 
            '%@ Проверте что модуль books содержит переменную book_ns'
        )

    def test_books_file_has_book_ns(self):
        import models
        self.assertTrue(
            hasattr(models, 'Book'), 
            '%@ Проверте что модуль models.py содержит модель Book'
        )

    def test_book_ns_has_correct_resources(self):
        from views import books
        namespace = books.book_ns.name
        resources_list = [res.urls[0] for res in books.book_ns.resources]
        expected_resources = ['/', '/<int:bid>']
        for expected in expected_resources:
            self.assertIn(expected, expected_resources,
            '%@ Проверьте что фаил books содержит classbased view для '
            f' адреса /"{namespace}{expected}"')

    def test_author_ns_has_correct_resources(self):
        from views import books
        namespace = books.book_ns.name
        resources_list = [res.urls[0] for res in books.book_ns.resources]
        expected_resources = ['/', '/<int:bid>']
        for expected in expected_resources:
            self.assertIn(expected, expected_resources,
            '%@ Проверьте что фаил books содержит class based view для '
            f' адреса /"{namespace}{expected}"')

class ApplicationTestCase(SkyproTestCase,
                          ResponseTestsMixin):
    def setUp(self):
        self.student_app = app.app.test_client()

    def test_view_books_get_is_available_and_works_correct(self):
        url = '/books/'
        test_options = {
            "url": url,
            "method": 'GET',
            "code": [200],
            "student_response": self.student_app.get(
                url, json=""),
            "expected": list
        }
        self.check_status_code_jsonify_and_expected(**test_options)

    def test_view_books_post_is_available_and_works_correct(self):
        url = '/books/'
        test_options = {
            "url": url,
            "method": 'POST',
            "code": [201],
            "student_response": self.student_app.post(
                url, json={}),
        }
        self.check_status_code_jsonify_and_expected(**test_options)

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

if __name__ == "__main__":
    unittest.main()