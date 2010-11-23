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
    joindate = Column(DateTime, default='now()')

    def __init__(self, *args, **kwargs):
        if len(kwargs) > 0:
            self.firstname = kwargs['firstname']
            self.lastname = kwargs['lastname']
            self.username = kwargs['username']
            self.email = kwargs['email']
            self.password = kwargs['password']
