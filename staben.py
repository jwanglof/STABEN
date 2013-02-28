import config
import model
from dev import db_commands

app = config.app

# DEV OPTIONS
# NEED TO BE REMOVED IN PRODUCTION MODE
@app.route('/db_create')
def db_create():
    db_commands.create_app()

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run()
