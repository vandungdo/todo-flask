from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import os
import datetime

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)

class Things(db.Model):
    __tablename__ = 'data'
    id = db.Column(db.Integer,primary_key=True)
    thing = db.Column(db.String(200))
    complete = db.Column(db.Boolean)

    # def __init__(self,thing,complete):
    #     self.thing = thing
    #     self.complete = complete

    # def __repr__(self):
    #     return f"{self.thing}, {self.complete}"

@app.route('/')
def show():
    time = str(datetime.datetime.now())
    thingToDo = Things.query.filter_by(complete=False).all()
    thingCompleted = Things.query.filter_by(complete=True).all()
    return render_template('index.html',thingToDo=thingToDo,thingCompleted=thingCompleted,time=time)

@app.route('/add', methods=['POST'])
def add():
    data = Things(thing=request.form['thing'],complete=False)
    db.session.add(data)
    db.session.commit()

    return redirect(url_for('show'))

@app.route('/complete/<id>')
def complete(id):
    data = Things.query.filter_by(id=int(id)).first()
    data.complete = True
    db.session.commit()
    return redirect(url_for('show'))

@app.route('/resetComplete')
def resetComplete():
    data = Things.query.filter_by(complete=True).first()
    db.session.delete(data)
    db.session.commit()
    return redirect(url_for('show'))

@app.route('/resetTodo')
def resetTodo():
    data = Things.query.filter_by(complete=False).first()
    db.session.delete(data)
    db.session.commit()
    return redirect(url_for('show'))

if __name__ == "__main__":
    app.run(debug=True)
