__author__="mengu"
__date__ ="$Jun 27, 2010 5:16:14 PM$"

from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, Unicode, UnicodeText, DateTime, Boolean
from sqlalchemy.orm import relation, backref
from ideabox.model.meta import Base
from ideabox.model.user import User
from ideabox.lib.helpers import slugify
from datetime import datetime

class Project(Base):
    __tablename__ = "project"

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(100))
    slug = Column(Unicode(150))
    description = Column(Unicode(300))
    user_id = Column(Integer, ForeignKey("user.id"))
    author = relation(User, backref=backref('project', lazy='dynamic'), primaryjoin="Project.user_id == User.id")
    dateline = Column(DateTime)

    def __init__(self, name, description, user_id):
        self.name = name
        self.slug = slugify(name)
        self.description = description
        self.user_id = user_id
        self.dateline = datetime.now()

class Task(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True)
    task = Column(UnicodeText(300))
    project = Column(Integer, ForeignKey("project.id"))
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relation(User, backref=backref('task', lazy='dynamic'), primaryjoin="Task.user_id == User.id")
    assigned_to = Column(Integer, ForeignKey("user.id"))
    assigned_user = relation(User, backref=backref('task_assigned', lazy='dynamic'), primaryjoin="Task.assigned_to == User.id")
    completed = Column(Boolean)
    completed_at = Column(DateTime, nullable=True)
    deadline = Column(DateTime, nullable=True)
    dateline = Column(DateTime)

    def __init__(self, task, project, author, assigned_to, deadline):
        self.task = task
        self.project = project
        self.author = author
        self.assigned_to = assigned_to
        self.completed = False
        self.deadline = deadline
        self.dateline = datetime.now()

class Note(Base):
    __tablename__ = "note"

    id = Column(Integer, primary_key=True)
    project = Column(Integer, ForeignKey("project.id"))
    task = Column(Integer, ForeignKey("task.id"))
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relation(User, backref=backref('note', lazy='dynamic'), primaryjoin="Note.user_id == User.id")
    note = Column(Unicode(300))
    dateline = Column(DateTime)

    def __init__(self, project, task, author, note):
        self.project = project
        self.task = task
        self.author = author
        self.note = note
        self.dateline = datetime.now()
