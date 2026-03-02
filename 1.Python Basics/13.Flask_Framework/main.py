from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "<html><body><h1>Hello, Flask!</h1><p>Testing Flask application. Added more text to test the application.</p></body></html>"

@app.route('/about')
def about():
    return render_template('index.html', name="Bensly")

@app.route('/contact')
def contact():
    return render_template('contact.html', name="Bensly")

@app.route('/dspage')
def dspage():
    return render_template('dspage.html', name="Bensly")

@app.route('/csspage')
def csspage():
    return render_template('csspage.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        return f"Welcome {user}"
    return '''
        <form method="post">
            <input name="username">
            <input type="submit">
        </form>
    '''
@app.route("/index",methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/form',methods=['GET','POST'])
def form():
    if request.method=='POST':
        name=request.form['name']
        return f'Hello {name}!'
    return render_template('form.html')

@app.route('/submit',methods=['GET','POST'])
def submit():
    if request.method=='POST':
        name=request.form['name']
        return f'Hello {name}!'
    return render_template('form.html')

@app.route('/user/<name>')
def user(name):
    return f"Hello {name} We are in User Page"

#Rest API with Flask    

@app.route('/api/data')
def get_data():
    return jsonify({"name": "Bensly", "role": "Data Scientist"})

#Flask for Data Science

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    result = model.predict([data["input"]])
    return jsonify({"prediction": result.tolist()})

if __name__ == '__main__':
    app.run(debug=True)