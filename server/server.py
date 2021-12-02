from flask import Flask
import time


app = Flask(__name__)

@app.route('/')
def index():
    time.sleep(15)
    return {"message": "Hello World!"}

@app.route('/test/')
def test2():
    return {"message": "Hello World 2!"}

if(__name__ == "__main__"):
    app.run(debug=True)