"""The application's model objects"""
from ideabox.model.meta import Session, Base
from ideabox.model.project import Project, Task
from ideabox.model.user import User


def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
    Session.configure(bind=engine)
