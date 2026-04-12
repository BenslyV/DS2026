from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Flask! Testing Flask application.  Added more text to test the application."

@app.route('/about')
def about():
    return "we are in About Page"

@app.route('/user/<name>')
def user(name):
    return f"Hello {name} We are in User Page"

if __name__ == '__main__':
    app.run(debug=True)