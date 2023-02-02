from flask import request
from flask_restx import Resource, Namespace
from models import Book
from setup_db import db

book_ns = Namespace('books')


@book_ns.route('/')
class BooksView(Resource):
    def get(self):
        bs = Book.query.all()
        res = []
        for b in bs:
            sm_d = b.__dict__
            del sm_d['_sa_instance_state']
            res.append(sm_d)
        return res, 200

    def post(self):
        req_json = request.json
        ent = Book(**req_json)
        db.session.add(ent)
        db.session.commit()
        return "", 201

@book_ns.route('/<int:bid>')
class BookView(Resource):
    def get(self, bid):
        r = Book.query.get(bid)
        sm_d = r.__dict__
        del sm_d['_sa_instance_state']
        return sm_d, 200

    def put(self, bid):
        book = Book.query.get(bid)
        req_json = request.json
        book.name = req_json.get('name')
        book.author = req_json.get("author")
        book.year = req_json.get("year")
        book.pages = req_json.get("pages")
        db.session.add(book)
        db.session.commit()
        return "", 204

    def delete(self, bid):
        review = Book.query.get(bid)
        
        db.session.delete(review)
        db.session.commit()
        return "", 204