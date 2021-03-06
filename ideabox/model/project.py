__author__="mengu"
__date__ ="$Jun 27, 2010 5:16:14 PM$"

from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.types import Integer, Unicode, UnicodeText, Date, DateTime, Boolean
from sqlalchemy.orm import relation
from ideabox.model.meta import Base
from ideabox.model.user import User
from ideabox.lib.helpers import slugify
from datetime import datetime
from datetime import date

project_member_table = Table('project_member', Base.metadata,
    Column('project_id', Integer, ForeignKey('project.id'), primary_key=True),
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True)
)

class Project(Base):
    __tablename__ = "project"

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(100), nullable=False)
    slug = Column(Unicode(150), nullable=False)
    description = Column(Unicode(300), nullable=False)
    author_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    dateline = Column(DateTime, nullable=False)

    #users = relation(User, secondary=project_member_table, backref="projects")
    author = relation(User, backref="project", primaryjoin="Project.author_id == User.id")
    tasklists = relation("TaskList", backref="project", 
        primaryjoin="Project.id == TaskList.project_id", cascade="all")

    def __init__(self, *args, **kwargs):
        if len(kwargs) > 0:
            self.name = kwargs["name"]
            self.slug = slugify(self.name)
            self.description = kwargs["description"]
            self.author_id = kwargs["author_id"]
            self.dateline = datetime.utcnow()

class Task(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True)
    task = Column(UnicodeText, nullable=False)
    project_id = Column(Integer, ForeignKey("project.id"), nullable=False)
    tasklist_id = Column(Integer, ForeignKey("tasklist.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    assigned_to = Column(Integer, ForeignKey("user.id"), nullable=False)
    completed = Column(Boolean, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    deadline = Column(Date, nullable=True)
    dateline = Column(DateTime, nullable=False, default=datetime.now())

    project = relation(Project, backref="tasks", primaryjoin="Task.project_id == Project.id")
    #user = relation(User, backref="tasks", primaryjoin="Task.user_id == User.id")
    assigned_user = relation(User, backref="tasks_assigned", primaryjoin="Task.assigned_to == User.id")

    def __init__(self, *args, **kwargs):
        if len(kwargs) > 0:
            self.task = kwargs["task"]
            self.tasklist_id = kwargs["tasklist_id"]
            self.project_id = kwargs["project_id"]
            self.user_id = kwargs["user_id"]
            self.assigned_to = kwargs["assigned_to"]
            self.completed = False
            self.deadline = kwargs["deadline"]

class TaskList(Base):
    __tablename__ = "tasklist"

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(100), nullable=False)
    project_id = Column(Integer, ForeignKey("project.id"), nullable=False)

    tasks = relation("Task", backref="tasklist", primaryjoin="TaskList.id == Task.tasklist_id", 
        cascade="all", order_by=[Task.completed, Task.task])

    def __init__(self, *args, **kwargs):
        if len(kwargs) > 0:
            self.name = kwargs['name']
            self.project_id = kwargs['project_id']

class Note(Base):
    __tablename__ = "note"

    id = Column(Integer, primary_key=True)
    project = Column(Integer, ForeignKey("project.id"), nullable=False)
    task = Column(Integer, ForeignKey("task.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    note = Column(Unicode(300), nullable=False)
    dateline = Column(DateTime, nullable=False)

    user = relation(User, backref="note", primaryjoin="Note.user_id == User.id")

    def __init__(self, project, task, author, note):
        self.project = project
        self.task = task
        self.author = author
        self.note = note
        self.dateline = datetime.utcnow()

class Ticket(Base):
    __tablename__ = "ticket"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("project.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    body = Column(UnicodeText, nullable=False)
    status = Column(Integer, nullable=False)
    priority = Column(Integer, nullable=False)
    dateline = Column(DateTime, nullable=False)

    project = relation(Project, backref="tickets", primaryjoin="Ticket.project_id == Project.id")
    user = relation(User, backref="tickets", primaryjoin="Ticket.user_id == User.id")

    def __init__(self, project_id, user_id, body, status, priority):
        self.project_id = project_id
        self.user_id = user_id
        self.body = body
        self.status = status
        self.priority = priority
        self.dateline = datetime.utcnow()


