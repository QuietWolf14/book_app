from app import app, db
from flask import render_template, request, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Book, List
from werkzeug.urls import url_parse
from app.forms import LoginForm, RegistrationForm, AddBook, CreateList


@app.route('/')
@app.route('/index')
@login_required
def index():
    book = Book.query.filter_by(isbn=9781534445420).first()

    if book is None:
        book = {'title':"None", 'author':'None'}
    
    return render_template('index.html', title='Home', book=book)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash ('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        user = User.query.filter_by(username=form.username.data).first()
        want_to_read = List(name="Want To Read", user_id=user.id)
        currently_reading = List(name="Currently Reading", user_id=user.id)
        read = List(name="Read", user_id=user.id)

        db.session.add(want_to_read)
        db.session.add(currently_reading)
        db.session.add(read)
        db.session.commit()

        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)


@app.route('/book-details')
def book_details():
    book = Book.query.filter_by(isbn=9781534445420).first()
    return render_template('book_details.html', title='Book Details', book=book)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    books = [
        {'title':'Slay', 'author':'Brittney Morris'},
        {'title':'MagnifiqueNoir: Book2', 'author':'Briana Lawrence'}
    ]

    return render_template('user.html', user=user, books=books)


@app.route('/add-book', methods=['GET', 'POST'])
def add_book():
    form = AddBook()
    if form.validate_on_submit():
        isbn = form.isbn.data
        title = form.title.data
        author = form.author.data
        summary = form.summary.data
        book = Book(isbn=isbn, title=title, author=author, summary=summary)
        db.session.add(book)
        db.session.commit()
        flash("Book added successfully.")
        return redirect(url_for('index'))

    return render_template('add_book.html', title="Add Book", form=form)


@app.route('/create-list', methods=['GET', 'POST'])
@login_required
def create_list():
    form = CreateList()
    lists = List.query.filter_by(user_id=current_user.id).all()
    if form.validate_on_submit():
        new_list = List(name=form.name.data, user_id=current_user.id)
        db.session.add(new_list)
        db.session.commit()
        flash("List successfully created.")
        return redirect(url_for('create_list'))
    
    return render_template('create_list.html', title='Create List', form=form, lists=lists)

@app.route('/browse-books')
def browse_books():
    books = Book.query.all()

    return render_template('browse_books.html', title='Browse Books', books=books)
