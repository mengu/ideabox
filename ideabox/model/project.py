__author__="mengu"
__date__ ="$Jun 27, 2010 5:16:14 PM$"

from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, Unicode, UnicodeText, DateTime, Boolean
from ideabox.model.meta import Base
from ideabox.lib.helpers import slugify
from datetime import datetime

class Project(Base):
    __tablename__ = "project"

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(100))
    slug = Column(Unicode(150))
    description = Column(Unicode(300))
    author = Column(Integer, ForeignKey("user.id"))
    dateline = Column(DateTime)

    def __init__(self, name, description, author):
        self.name = name
        self.slug = slugify(name)
        self.description = description
        self.author = author
        self.dateline = datetime.now()

class Task(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True)
    task = Column(UnicodeText(300))
    project = Column(Integer, ForeignKey("project.id"))
    author = Column(Integer, ForeignKey("user.id"))
    assigned_to = Column(Integer, ForeignKey("user.id"))
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
    author = Column(Integer, ForeignKey("user.id"))
    note = Column(Unicode(300))
    dateline = Column(DateTime)

    def __init__(self, project, task, author, note):
        self.project = project
        self.task = task
        self.author = author
        self.note = note
        self.dateline = datetime.now()