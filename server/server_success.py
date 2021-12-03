from flask import Flask
import time


app = Flask(__name__)

@app.route('/test/success')
def index():
    return {"message": "success"}

@app.route('/test/')
def test2():
    return {"message": "Hello World 2!"}

if(__name__ == "__main__"):
    app.run(debug=True, port=4000)