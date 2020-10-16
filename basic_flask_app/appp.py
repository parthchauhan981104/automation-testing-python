from flask import Flask, jsonify


app = Flask(__name__)  #__name__ contains relative path of current module, it is always unique


@app.route('/')
def home():
    return jsonify({'message': 'Hello, world!'})


if __name__ == '__main__': #when this file appp.py is run directly
    app.run()
# if another file imports appp, __name__ value will not be __main__
# so app.run() will not run by itself and that file can control when they want to run it
