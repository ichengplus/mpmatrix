# coding=utf8
from model import db
from model.todos import Todo

def create_todo(data):
    task = data.get('task')
    todo_id = data.get('id')

    todo = Todo(task)
    if todo_id:
        todo.id = todo_id

    db.session.add(todo)
    db.session.commit()


def update_todo(todo_id, data):
    todo = Todo.query.filter(Todo.id == todo_id).one()
    todo.task = data.get('task')
    db.session.add(todo)
    db.session.commit()


def delete_todo(todo_id):
    todo = Todo.query.filter(Todo.id == todo_id).one()
    db.session.delete(todo)
    db.session.commit()