import config

from flask import Flask, jsonify, request
from model import db, app

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run()