


import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from ideabox.lib.base import BaseController, Session, render
from ideabox.model.project import Note
from ideabox.model.user import User
from datetime import datetime

log = logging.getLogger(__name__)

class NotesController(BaseController):

    def __before__(self, action, **params):
        filter_actions = ["new", "edit", "create", "update", "delete"]
        if "user" not in session and action in filter_actions:
            redirect("/users/login")

    def create(self):
        note_dict = {}
        for param in request.params:
            note_dict[param] = request.params[param]
        note_dict["author"] = session["user"]["id"]
        new_note = Note(**note_dict)
        Session.add(new_note)
        Session.commit()
        return redirect("/tasks/show/%s" % note_dict["task"])

    def delete(self, id):
        try:
            note = Session.query(Note).filter_by(id=id).delete()
        except:
            abort(404)
        return redirect("/Notes")


