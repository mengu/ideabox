# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="mengu"
__date__ ="$Jun 27, 2010 5:16:19 PM$"

from sqlalchemy import Column
from sqlalchemy.types import Integer, Unicode, DateTime
from ideabox.model.meta import Base
from datetime import datetime

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    firstname = Column(Unicode(100))
    lastname = Column(Unicode(100))
    username = Column(Unicode(100), unique=True)
    email = Column(Unicode(150), unique=True)
    password = Column(Unicode(32))
    joindate = Column(DateTime)

    def __init__(self, firstname, lastname, username, email, password):
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.email = email
        self.password = password
        self.joindate = datetime.now()