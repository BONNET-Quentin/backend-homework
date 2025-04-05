
VERSION = "06"
import json
from flask import Flask
import requests
from flask import redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from flask import request
from flask import render_template

## usual Flask initilization
app = Flask(__name__)


## DB declaration

# filename where to store stuff (sqlite is file-based)
db_name = 'chat.db'
# how do we connect to the database ?
# here we say it's by looking in a file named chat.db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
# this variable, db, will be used for all SQLAlchemy commands
db = SQLAlchemy(app)

class Note(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    content = db.Column(db.String)
    done = db.Column(db.Boolean)


# actually create the database (i.e. tables etc)
with app.app_context():
    db.create_all()

@app.route('/')
def hello_world():
    # redirect to /front/notes
    # actually this is just a rsponse with a 301 HTTP code
    return redirect('/front/notes')

@app.route('/db/alive')
def db_alive():
    # A UTILISER AVEC http -I :5000/db/alive ou httpx http://127.0.0.1:5000/db/alive
    try:
        result = db.session.execute(text('SELECT 1'))
        print(result)
        return dict(status="healthy", message="Database connection is alive")
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text
    
@app.route('/api/notes', methods=['POST'])
def create_note():
    # we expect the user to send a JSON object with the 3 fields title, content and done
    # A UTILISER AVEC http -I :5000/api/notes title="MMC" content="reviser la fiche" done="ok" par exemple
    # OU http -I post :5000/api/notes title="MMC" content="reviser la fiche" done="ok"
    try:
        parameters = json.loads(request.data)
        title = parameters['title']
        content = parameters['content']
        done = parameters['done']
        print("note created successfully")
        # temporary
        new_note = Note(title=title, content=content, done=done)
        db.session.add(new_note)
        db.session.commit()
        return "note created successfully"
    except Exception as exc:
        return dict(error=f"{type(exc)}: {exc}"), 422

@app.route('/api/notes', methods=['GET'])
def list_notes():
    # A UTILISER AVEC http -I get :5000/api/notes ou http -I :5000/api/notes 
    notes = Note.query.all()
    return [dict(
            id=note.id, title=note.title, content=note.content, done=note.done)
        for note in notes]

@app.route('/api/notes/<int:id>/done', methods=['POST'])
def update_note_done_status(id):
    try:
        # Parse the request body to get the 'done' status
        parameters = json.loads(request.data)
        done = parameters['done']

        # Find the note by its ID
        note = Note.query.get(id)
        if not note:
            return dict(error="Note not found"), 404

        # Update the 'done' status of the note
        note.done = done
        db.session.commit()

        return dict(ok="ok")
    except Exception as exc:
        return dict(error=f"{type(exc)}: {exc}"), 422

@app.route('/api/notes/<int:id>', methods=['DELETE'])
def delete_note(id):
    # A UTILISER AVEC http -I delete :5000/api/notes/2
    try:
        # Find the note by its ID
        note = Note.query.get(id)
        if not note:
            return dict(error="Note not found"), 404

        # Delete the note from the database
        db.session.delete(note)
        db.session.commit()

        return dict(ok="ok")
    except Exception as exc:
        return dict(error=f"{type(exc)}: {exc}"), 422

## Frontend
# for clarity we define our routes in the /front namespace
# however in practice /front/users would probably be just /users

@app.route('/front/notes')
def front_notes():
    # first option of course, is to get all users from DB
    # users = User.query.all()
    # but in a more fragmented architecture we would need to
    # get that info at another endpoint
    # here we ask ourselves on the /api/users route
    url = request.url_root + '/api/notes'
    req = requests.get(url)
    if not (200 <= req.status_code < 300):
        # return render_template('errors.html', error='...')
        return dict(error=f"could not request notes list", url=url,
                    status=req.status_code, text=req.text)
    notes = req.json()
    return render_template('notes.html.j2', notes=notes, version=VERSION)


if __name__ == '__main__':
    app.run()