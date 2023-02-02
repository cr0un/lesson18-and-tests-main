from flask import request
from flask_restx import Resource, Namespace
from models import Book
from setup_db import db

book_ns = Namespace('books')


@book_ns.route('/')
class BooksView(Resource):
    def get(self):                            
        books = Book.query.all()
        res = []
        for book in books:                    
            sm_d = book.__dict__              
            del sm_d['_sa_instance_state']    
            res.append(book.__dict__)
        return res, 200

    def post(self):
        data = request.json
        new_book = Book(name=data.get('name'),
                        author=data.get('author'),
                        year=data.get('year'))
        with db.session.begin():
            db.session.add(new_book)
        return "", 201


@book_ns.route('/<int:bid>')
class BookView(Resource):
    def get(self, bid):
        book = Book.query.get(bid)
        result = book.__dict__
        del result['_sa_instance_state']
        return result, 200
