from flask import Flask

app = Flask(__name__)
@app.route('/')
def indexGET():
    return "GET"

@app.route('/', methods=["POST"])
def POST():
    print("post")
    return "POST"

@app.route('/', methods=["PUT"])
def PUT():
    return "PUT"

@app.route('/', methods=["DELETE"])
def DELETE():
    return "DELETE"

@app.route('/tests/:id')
def test():
    return "GET a new test"