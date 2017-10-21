from flask import Flask, render_template

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/')
@app.route('/catalog')
def home():
    return render_template('home.html')


@app.route('/login')
def login():
    return 'Login page'


@app.route('/catalog/category/<int:category_id>')
def category(category_id):
    return 'Category page for ' + str(category_id)


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
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
