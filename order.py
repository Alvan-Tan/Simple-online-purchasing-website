from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/book'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)

# CORS(app)

@app.route("/")
def index():
    # if 'username' in session:
    #     username = session['username']
    #     return "Logged in as" + username + "<br>" + "<b><a href = '/logout'>click here to log out</a></b>"
    # return "You are not logged in <br><a href= '/login'>click here to log in </a>"
    return render_template("index.html")

@app.route("/login", methods = ["GET", "POST"])
def login_verification():
    # if request.method == 'POST':
    #   session['username'] = request.form['username']
    #   return redirect(url_for('index'))
    return render_template("login.html")

@app.route('/logout')
def logout():
#    session.pop('username', None)
#    return redirect(url_for('index'))
    return render_template("index.html")


# @app.route("/book")
# def get_all():
#     booklist = Book.query.all()
#     if len(booklist):
#         return jsonify(
#             {
#                 "code": 200,
#                 "data": {
#                     "books": [book.json() for book in booklist]
#                 }
#             }
#         )
#     return jsonify(
#         {
#             "code": 404,
#             "message": "There are no books."
#         }
#     ), 404


# @app.route("/book/<string:isbn13>")
# def find_by_isbn13(isbn13):
#     book = Book.query.filter_by(isbn13=isbn13).first()
#     if book:
#         return jsonify(
#             {
#                 "code": 200,
#                 "data": book.json()
#             }
#         )
#     return jsonify(
#         {
#             "code": 404,
#             "message": "Book not found."
#         }
#     ), 404


# @app.route("/book/<string:isbn13>", methods=['POST'])
# def create_book(isbn13):
#     if (Book.query.filter_by(isbn13=isbn13).first()):
#         return jsonify(
#             {
#                 "code": 400,
#                 "data": {
#                     "isbn13": isbn13
#                 },
#                 "message": "Book already exists."
#             }
#         ), 400

#     data = request.get_json()
#     book = Book(isbn13, **data)

#     try:
#         db.session.add(book)
#         db.session.commit()
#     except:
#         return jsonify(
#             {
#                 "code": 500,
#                 "data": {
#                     "isbn13": isbn13
#                 },
#                 "message": "An error occurred creating the book."
#             }
#         ), 500

#     return jsonify(
#         {
#             "code": 201,
#             "data": book.json()
#         }
#     ), 201


# @app.route("/book/<string:isbn13>", methods=['PUT'])
# def update_book(isbn13):
#     book = Book.query.filter_by(isbn13=isbn13).first()
#     if book:
#         data = request.get_json()
#         if data['title']:
#             book.title = data['title']
#         if data['price']:
#             book.price = data['price']
#         if data['availability']:
#             book.availability = data['availability'] 
#         db.session.commit()
#         return jsonify(
#             {
#                 "code": 200,
#                 "data": book.json()
#             }
#         )
#     return jsonify(
#         {
#             "code": 404,
#             "data": {
#                 "isbn13": isbn13
#             },
#             "message": "Book not found."
#         }
#     ), 404


# @app.route("/book/<string:isbn13>", methods=['DELETE'])
# def delete_book(isbn13):
#     book = Book.query.filter_by(isbn13=isbn13).first()
#     if book:
#         db.session.delete(book)
#         db.session.commit()
#         return jsonify(
#             {
#                 "code": 200,
#                 "data": {
#                     "isbn13": isbn13
#                 }
#             }
#         )
#     return jsonify(
#         {
#             "code": 404,
#             "data": {
#                 "isbn13": isbn13
#             },
#             "message": "Book not found."
#         }
#     ), 404


if __name__ == "__main__":
    app.run(port="5000", debug=True)