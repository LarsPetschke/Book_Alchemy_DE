from flask import Flask, render_template, request
import os
from data_models import db, Author, Book

app = Flask(__name__)

# Absoluten Pfad bestimmen
basedir = os.path.abspath(os.path.dirname(__file__))

# Database-URI setzen (absoluter Pfad)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# SQLAlchemy mit Flask verbinden
db.init_app(app)


# ---------------------------
# ROUTE: Autor hinzufügen
# ---------------------------
@app.route("/add_author", methods=["GET", "POST"])
def add_author():
    message = None

    if request.method == "POST":
        name = request.form["name"]
        birthdate = request.form["birthdate"]
        date_of_death = request.form["date_of_death"]

        author = Author(
            name=name,
            birth_date=birthdate,
            date_of_death=date_of_death if date_of_death else None
        )

        db.session.add(author)
        db.session.commit()

        message = "Author successfully added!"

    return render_template("add_author.html", message=message)


# ---------------------------
# ROUTE: Buch hinzufügen
# ---------------------------
@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    message = None
    authors = Author.query.all()

    if request.method == "POST":
        title = request.form["title"]
        isbn = request.form["isbn"]
        publication_year = request.form["publication_year"]
        author_id = request.form["author_id"]

        book = Book(
            title=title,
            isbn=isbn,
            publication_year=publication_year,
            author_id=author_id
        )

        db.session.add(book)
        db.session.commit()

        message = "Book successfully added!"

    return render_template("add_book.html", authors=authors, message=message)


# ---------------------------
# ROUTE: Startseite + Stichwortsuche
# ---------------------------
@app.route("/")
def home():
    search = request.args.get("search", None)

    query = Book.query

    # Stichwortsuche aktivieren
    if search:
        query = query.filter(Book.title.ilike(f"%{search}%"))

    books = query.all()

    # Meldung bei keinen Treffern
    if search and len(books) == 0:
        message = f"No books found for '{search}'."
    else:
        message = None

    return render_template("home.html", books=books, message=message)


# ---------------------------
# Tabellen erzeugen (einmalig)
# ---------------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
