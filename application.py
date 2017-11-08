import random
import string
import httplib2
import json
import requests

from flask import Flask, render_template, Markup, session as login_session, \
    make_response, request, flash, redirect, url_for, jsonify

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Category, Item

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)
app.url_map.strict_slashes = False

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item Catalog"


@app.route('/')
@app.route('/catalog')
def home():
    categories = session.query(Category).all()
    items = session.query(Item).order_by(Item.id.desc()).limit(10)
    return render_template('home.html', categories=categories, items=items,
                           login_session=login_session)


@app.route('/catalog/category/<int:category_id>')
def category(category_id):
    items = session.query(Item).filter(Item.category_id == category_id).all()
    return render_template('category.html', items=items,
                           login_session=login_session)


@app.route('/catalog/item/<int:item_id>')
def item(item_id):
    item = session.query(Item).filter(Item.id == item_id).first()
    return render_template('item.html', item=item, login_session=login_session)


@app.route('/catalog/item/add', methods=['GET', 'POST'])
def item_add():
    if 'username' not in login_session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        item = Item(name=request.form['name'],
                    description=request.form['description'],
                    category_id=request.form['category_id'])
        session.add(item)
        session.commit()
        return redirect(url_for('home'))
    else:
        categories = session.query(Category).all()
        return render_template('add_item.html', categories=categories)


@app.route('/catalog/item/<int:item_id>/edit', methods=['GET', 'POST'])
def item_edit(item_id):
    if 'username' not in login_session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        # Get a copy of the item from the database, update it with the new
        # values and commit it to the database.
        item = session.query(Item).filter(Item.id == item_id).first()
        item.name = request.form['name']
        item.description = request.form['description']
        item.category_id = request.form['category_id']
        session.add(item)
        session.commit()
        return redirect(url_for('item', item_id=item_id))
    else:
        item = session.query(Item).filter(Item.id == item_id).first()
        categories = session.query(Category).all()
        return render_template('edit_item.html', categories=categories,
                               item=item)


@app.route('/catalog/item/<int:item_id>/delete', methods=['GET', 'POST'])
def item_delete(item_id):
    if 'username' not in login_session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        itemToDelete = session.query(Item).filter(Item.id == item_id).first()
        session.delete(itemToDelete)
        session.commit()
        return redirect(url_for('home'))
    else:
        item = session.query(Item).filter(Item.id == item_id).first()
        return render_template('delete_item.html', item=item)


@app.route('/login')
def login():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
            'Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # Check database if user exists
    user = session.query(User) \
                  .filter(User.email == login_session['email']).first()
    if not user:
        new_user = User(name=login_session['username'],
                        email=login_session['email'])
        session.add(new_user)
        session.commit()

    # TODO: use templates
    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    return output


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print('Access Token is None')
        response = make_response(json.dumps(
            'Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print('In gdisconnect access token is %s', access_token)
    print('User name is: ')
    print(login_session['username'])
    url = 'https://accounts.google.com/o/oauth2/revoke?token={}'.format(
        login_session['access_token'])
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print('result is ')
    print(result)
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps(
            'Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

# START JSON ENDPOINTS


# Get list of categories
@app.route('/catalog/categories/json')
def categories_json():
    categories = session.query(Category).all()
    return jsonify(Categories=[i.serialize for i in categories])


# Get list of items in a category
@app.route('/catalog/category/<int:category_id>/json')
def category_items_json(category_id):
    items = session.query(Item).filter(Item.category_id == category_id).all()
    return jsonify(Items=[i.serialize for i in items])


# Get list of all items
@app.route('/catalog/items/json')
def all_items_json():
    items = session.query(Item).all()
    return jsonify(Items=[i.serialize for i in items])


# Get single item by item id
@app.route('/catalog/item/<int:item_id>/json')
def item_json(item_id):
    item = session.query(Item).filter(Item.id == item_id).first()
    return jsonify(Item=item.serialize)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
