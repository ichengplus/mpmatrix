from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def reset_database():
    from model.blogs import Post, Category  # noqa
    from model.todos import Todo
    db.drop_all()
    db.create_all()
