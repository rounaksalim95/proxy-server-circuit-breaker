import time

from flask import Flask

app = Flask(__name__)


@app.route("/test/failure/timeout")
def index():
    time.sleep(7)
    return {"message": "Timeout failure"}, 400


@app.route("/test/failure/")
def test2():
    return {"message": "Failure"}, 400


if __name__ == "__main__":
    app.run(debug=True)
