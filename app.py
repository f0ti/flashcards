import os
import json
import random

from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')  # external render database
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('LOCALHOST_DATABASE_URI')  # local database  
app.secret_key = 'gaye'

db = SQLAlchemy(app)
mirage = Migrate(app, db)


class Collection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    flashcards = db.relationship('Flashcard', backref='collection', lazy=True)


class Flashcard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    front = db.Column(db.String(1024), nullable=False)
    back = db.Column(db.String(1024), nullable=False)
    collection_id = db.Column(db.Integer, db.ForeignKey('collection.id'))


@app.route('/')
def index():
    collections = Collection.query.all()
    return render_template('index.html', collections=collections)


@app.route('/collection/add', methods=['GET', 'POST'])
def add_collection():
    if request.method == 'POST':
        name = request.form['name']
        flashcards_data = json.loads(request.form['flashcards'])

        collection = Collection(name=name)
        db.session.add(collection)
        db.session.commit()
        
        for flashcard_data in flashcards_data:
            front = flashcard_data['front']
            back = flashcard_data['back']
            flashcard = Flashcard(front=front, back=back, collection_id=collection.id)
            db.session.add(flashcard)
        
        db.session.commit()
        
        return redirect(url_for('index'))
    
    return render_template('add_collection.html')


@app.route('/collection/<int:collection_id>/edit', methods=['GET', 'POST'])
def edit_collection(collection_id):
    collection = Collection.query.get_or_404(collection_id)
    if request.method == 'POST':
        name = request.form['name']
        collection.name = name
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_collection.html', collection=collection)


@app.route('/collection/<int:collection_id>/delete', methods=['POST'])
def delete_collection(collection_id):
    collection = Collection.query.get_or_404(collection_id)
    db.session.delete(collection)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/collection/<int:collection_id>/flashcards', methods=['GET', 'POST'])
def flashcards(collection_id):
    collection = Collection.query.get_or_404(collection_id)
    if request.method == 'POST':
        front = request.form['front']
        back = request.form['back']
        flashcard = Flashcard(front=front, back=back, collection_id=collection_id)
        db.session.add(flashcard)
        db.session.commit()
        return redirect(url_for('flashcards', collection_id=collection_id))
    return render_template('flashcards.html', collection=collection)


@app.route('/collection/<int:collection_id>/flashcards/<int:flashcard_id>/delete', methods=['POST'])
def delete_flashcard(collection_id, flashcard_id):
    flashcard = Flashcard.query.get_or_404(flashcard_id)
    db.session.delete(flashcard)
    db.session.commit()
    return redirect(url_for('flashcards', collection_id=collection_id))


@app.route('/collection/<int:collection_id>/slideshow', methods=['GET'])
def slideshow(collection_id):
    collection = Collection.query.get_or_404(collection_id)

    return render_template('slideshow.html', collection=collection)


if __name__ == '__main__':
    app.run(debug=True)
