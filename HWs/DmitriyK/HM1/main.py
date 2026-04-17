from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return "Hello world!"


@app.route("/user_name/<name>")
def hello_user(name):
    print(name, type(name))
    return f"{name}"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
