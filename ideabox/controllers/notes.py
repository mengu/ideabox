# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="mengu"
__date__ ="$Jul 1, 2010 1:34:28 AM$"

import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from ideabox.lib.base import BaseController, Session, render
from ideabox.lib.helpers import did_login_or_redirect
from ideabox.model.project import Note
from ideabox.model.user import User
from datetime import datetime

log = logging.getLogger(__name__)

class NotesController(BaseController):

    def create(self):
        did_login_or_redirect(session)
        note_dict = {}
        for param in request.params:
            note_dict[param] = request.params[param]
        note_dict["author"] = session["user"]["id"]
        new_note = Note(**note_dict)
        Session.add(new_note)
        Session.commit()
        return redirect("/tasks/show/%s" % note_dict["task"])

    def delete(self, id):
        did_login_or_redirect(session)
        try:
            Note = Session.query(Note).filter_by(id=id).delete()
        except:
            abort(404)
        return redirect("/Notes")


