from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(100), unique=True, nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publisher = db.Column(db.String(100))

    def __repr__(self):
        return f"<Book {self.book_name} by {self.author}>"

@app.route('/')
def index():
    return 'Welcome to the Book API!'

@app.route("/books")
def get_books():
    books = Book.query.all()
    output = [{'id': book.id, 'book_name': book.book_name, 'author': book.author, 'publisher': book.publisher} for book in books]
    return {'books': output}

@app.route('/books/<int:id>')
def get_book(id):
    book = Book.query.get_or_404(id)
    return {'id': book.id, 'book_name': book.book_name, 'author': book.author, 'publisher': book.publisher}

@app.route('/books', methods=['POST'])
def add_book():
    data = request.json
    new_book = Book(book_name=data['book_name'], author=data['author'], publisher=data.get('publisher'))
    db.session.add(new_book)
    db.session.commit()
    return {'id': new_book.id}, 201

@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return {"message": "Book deleted"}



