# coding=utf8

from model import db

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(50))

    def __init__(self, task):
        self.task = task

    def __repr__(self):
        return '<Todo %r>' % self.task