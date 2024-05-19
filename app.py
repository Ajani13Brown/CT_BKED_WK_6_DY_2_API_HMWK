from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from marshmallow import fields, ValidationError
from db_connection import connect_db, Error

app = Flask(__name__)
ma = Marshmallow(app)



class BooksSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    title = fields.String(required=True)
    isbn = fields.String(required=True)
    publication_date = fields.Date(required=True)

    class Meta:
        fields = ('id','title','isbn','publication_date')

book_schema = BooksSchema()
books_schema = BooksSchema(many=True)


@app.route("/")
def hello_world():
    return "Hi Mom!"

@app.route("/books", methods =['GET'])
def get_books():
    conn = connect_db()
    if conn is not None:
        try:
            cursor = conn.cursor(dictionary=True)

            query = "SELECT * FROM books"

            cursor.execute(query)

            book = cursor.fetchall()
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
                return books_schema.jsonify(book)
            

@app.route('/books', methods=['POST'])
def add_book():
    try:
        book_data = book_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    conn = connect_db()
    if conn is not None:
        try:
            cursor = conn.cursor()

            new_book = (book_data['title'], book_data['isbn'], book_data['publication_date'])

            query = "INSERT INTO books (title, isbn, publication_date) VALUES (%s, %s, %s)"

            cursor.execute(query, new_book)
            conn.commit()

            return jsonify({'Message': "New book Added Successfully!"}), 201
        except Error as e:
            return jsonify(e.messages), 500
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({"Error": "Database Connection failed"}), 500


if __name__ == '__main__':
    app.run(debug=True)


