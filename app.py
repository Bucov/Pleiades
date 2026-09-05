from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///manga.db'
db = SQLAlchemy(app)



class Manga(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    native_title = db.Column(db.String(200), nullable=True)
    type = db.Column(db.String(50), nullable=True)
    status = db.Column(db.String(50), nullable=True)
    year = db.Column(db.Integer, nullable=True)
    rating = db.Column(db.Float, nullable=True)
    description = db.Column(db.Text, nullable=True)
    genres = db.Column(db.JSON, nullable=True)
    tags = db.Column(db.JSON, nullable=True)
    authors = db.Column(db.JSON, nullable=True)
    total_chapters = db.Column(db.Float, nullable=True)
    cover_url = db.Column(db.String(500), nullable=True)
    avg_rating = db.Column(db.Float, nullable=True)

    def __repr__(self):
            return '<Manga ID: %r>' % self.id


with app.app_context():
    db.create_all()


@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html',)


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        request_title = request.form['query']
        stmt = db.select(Manga).where(Manga.title.contains(request_title))
        result = db.session.execute(stmt).scalars().all()
        return render_template('search.html', result=result)

        pass
    
    else:
        return render_template('search.html')
            

@app.route('/manga/<int:id>')
def manga(id):
    stmt = db.select(Manga).where(Manga.id == id)
    manga = db.session.execute(stmt).scalars().first()


    return render_template('manga.html', manga=manga, id=id)


@app.route('/settings')
def settings():
    return render_template('settings.html')


@app.route('/about')
def about():
    return render_template('about.html')

    
    
if __name__ == "__main__": 
    app.run(debug=True)