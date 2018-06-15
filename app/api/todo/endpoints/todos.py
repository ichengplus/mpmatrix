# coding=utf8

import logging

from flask import request
from flask_restplus import Api, Resource, fields

from api.restplus import api
from api.todo.serializers import todo
from model.todos import Todo
from api.todo.business import create_todo, update_todo, delete_todo

log = logging.getLogger(__name__)

ns = api.namespace('todos', description='TODO operations')


@ns.route('/')
class TodoListApi(Resource):
    '''Shows a list of all todos, and lets you POST to add new tasks'''
    @ns.doc('list_todos')
    @ns.marshal_list_with(todo)
    def get(self):
        '''List all tasks'''
        todos = Todo.query.all()
        return todos

    @ns.doc('create_todo')
    @ns.expect(todo)
    @ns.marshal_with(todo, code=201)
    def post(self):
        '''Create a new task'''
        data = request.json
        create_todo(data)
        return None, 201


@ns.route('/<int:id>')
@ns.response(404, 'Todo not found')
@ns.param('id', 'The task identifier')
class TodoApi(Resource):
    '''Show a single todo item and lets you delete them'''
    @ns.doc('get_todo')
    @ns.marshal_with(todo)
    def get(self, id):
        '''Fetch a given resource'''
        return Todo.query.filter(Todo.id == id).one()

    @ns.doc('delete_todo')
    @ns.response(204, 'Todo deleted')
    def delete(self, id):
        '''Delete a task given its identifier'''
        delete_todo(id)
        return '', 204

    @ns.expect(todo)
    @ns.marshal_with(todo)
    def put(self, id):
        '''Update a task given its identifier'''
        data = request.json
        update_todo(id, data)
        return None, 204