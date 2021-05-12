from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# Initialize DB
db = SQLAlchemy(app)

# class ToDo(db.Model):
#     # Set up column
#     id = db.Column(db.Integer, primary_key=True)
#     content = db.

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
