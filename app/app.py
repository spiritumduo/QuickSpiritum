
# import flask module
from flask import Flask
 
# instance of flask application
app = Flask(__name__)
 
# home route that returns below text
# when root url is accessed
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/me")
def hello_world2():
    return "<p>Hello, World!2</p>"
 
if __name__ == '__main__':
    app.run(debug=True, port=1111, host="0.0.0.0")