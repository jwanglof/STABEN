import model

app = model.app
db = model.db

# Should check if the DB is created successfully or not!
def create_app():
    db.init_app(app)
    with app.test_request_context():
        db.create_all()
    return app
