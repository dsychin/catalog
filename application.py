import random
import string
from flask import Flask, render_template, Markup, session as login_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Category, Item

engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/')
@app.route('/catalog')
def home():
    categories = session.query(Category).all()
    return render_template('home.html', categories=categories)


@app.route('/login')
def login():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    print(state)
    login_session['state'] = state
    return "The current session state is %s" % login_session['state']


@app.route('/catalog/category/<int:category_id>')
def category(category_id):
    items = session.query(Item).filter(Item.id == category_id).all()
    return render_template('category.html', items=items)


@app.route('/catalog/item/<int:item_id>')
def item(item_id):
    return 'Item page for ' + str(item_id)


@app.route('/catalog/item/add')
def item_add():
    return 'Adding items page'


@app.route('/catalog/item/<int:item_id>/edit')
def item_edit(item_id):
    return 'Edit item id number ' + str(item_id)


@app.route('/catalog/item/<int:item_id>/delete')
def item_delete(item_id):
    return 'Delete item id number ' + str(item_id)

# TODO Add json endpoints


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
