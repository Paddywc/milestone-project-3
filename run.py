import os
import json
from flask import Flask

app = Flask(__name__)

app.secret_key = 'some_secret'


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)