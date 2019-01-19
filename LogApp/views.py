from .app import app

@app.route('/admin')
def index_view():
    return 'hello'
