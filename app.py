from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
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

# Yt comment fix
with app.app_context():
    db.create_all()


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        request_content = request.form['content']
        if request_content == 'one':
                new_manga = Manga(title='Berserk', native_title='ベルセルク', type='Manga', status='Completed', year=1989, rating=9.5, description='A dark fantasy manga series written and illustrated by Kentaro Miura.', genres=['Action', 'Adventure', 'Dark Fantasy'], tags=['Guts', 'Griffith', 'Casca'], authors=['Kentaro Miura'], total_chapters=364, cover_url='https://comicbook.com/wp-content/uploads/sites/4/2024/04/9d93e8f2-9e48-408c-894f-9d7182489a57.jpg?resize=1024,576', avg_rating=9.5)
                new_manga2 = Manga(title='Naruto', native_title='ナルト', type='Manga', status='Completed', year=1999, rating=8.5, description='A manga series written and illustrated by Masashi Kishimoto.', genres=['Action', 'Adventure', 'Fantasy'], tags=['Naruto Uzumaki', 'Ninja', 'Shinobi'], authors=['Masashi Kishimoto'], total_chapters=700, cover_url='https://m.media-amazon.com/images/I/91RpwagB7uL._SL1500_.jpg', avg_rating=8.5)
                new_manga3 = Manga(title='Naruto 2', native_title='ナルト 2', type='Manga', status='Completed', year=2000, rating=8.0, description='A manga series written and illustrated by Masashi Kishimoto.', genres=['Action', 'Adventure', 'Fantasy'], tags=['Naruto Uzumaki', 'Ninja', 'Shinobi'], authors=['Masashi Kishimoto'], total_chapters=700, cover_url='https://example.com/naruto2.jpg', avg_rating=8.0)
        else:
                new_manga = Manga(title='One Piece', native_title='ワンピース', type='Manga', status='Ongoing', year=1997, rating=9.0, description='A manga series written and illustrated by Eiichiro Oda.', genres=['Action', 'Adventure', 'Fantasy'], tags=['Monkey D. Luffy', 'Pirates', 'Treasure'], authors=['Eiichiro Oda'], total_chapters=1000, cover_url='https://example.com/onepiece.jpg', avg_rating=9.0)
                new_manga2 = Manga(title='Dragon Ball', native_title='ドラゴンボール', type='Manga', status='Completed', year=1984, rating=9.0, description='A manga series written and illustrated by Akira Toriyama.', genres=['Action', 'Adventure', 'Fantasy'], tags=['Goku', 'Saiyan', 'Dragon Balls'], authors=['Akira Toriyama'], total_chapters=519, cover_url='https://example.com/dragonball.jpg', avg_rating=9.0)
                new_manga3 = Manga(title='Dragon Ball Z', native_title='ドラゴンボールZ', type='Manga', status='Completed', year=1989, rating=9.5, description='A manga series written and illustrated by Akira Toriyama.', genres=['Action', 'Adventure', 'Fantasy'], tags=['Goku', 'Saiyan', 'Dragon Balls'], authors=['Akira Toriyama'], total_chapters=325, cover_url='https://example.com/dragonballz.jpg', avg_rating=9.5)
        try:
            db.session.add_all([new_manga, new_manga2, new_manga3])
            db.session.commit()
            return redirect('/')
        except:
            return 'Error adding task'

    else:
        
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

    
    
if __name__ == "__main__": 
    app.run(debug=True)