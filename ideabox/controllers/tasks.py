import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from ideabox.lib.base import BaseController, Session, render
from ideabox.lib.helpers import did_login_or_redirect
from ideabox.model.project import Task, Note
from ideabox.model.user import User
from datetime import datetime

log = logging.getLogger(__name__)

class TasksController(BaseController):

    def new(self):
        did_login_or_redirect(session)
        if not request.params["projectid"]:
            return redirect("/projects")
        users = Session.query(User).all()
        return render("tasks/new.html", {"users": users, "projectid":request.params["projectid"]})

    def create(self):
        did_login_or_redirect(session)
        task_dict = {}
        for param in request.params:
            task_dict[param] = request.params[param]
        task_dict["author"] = session["user"]["id"]
        new_task = Task(**task_dict)
        Session.add(new_task)
        Session.commit()
        return redirect("/projects/show/%s" % task_dict["project"])

    def show(self, id):
        try:
            task = Session.query(Task).filter_by(id=id).one()
            assigned_user = Session.query(User).filter_by(id=task.assigned_to).one()
        except:
            abort(404)
        notes = Session.query(Note).filter_by(task=id).all()
        return render("tasks/show.html", {"task": task, "assigned_user":assigned_user, "notes": notes})

    def complete(self, id):
        did_login_or_redirect(session)
        try:
            task = Session.query(Task).filter_by(id=id).one()
        except:
            abort(404)
        completed = True if request.params["completed"] == "true" else False
        completed_at = datetime.now() if completed else None
        change_status = Session.query(Task).filter_by(id=id).update({
            "completed": completed,
            "completed_at": completed_at
        })
        Session.commit()

    def delete(self, id):
        did_login_or_redirect(session)
        try:
            task = Session.query(Task).filter_by(id=id).delete()
        except:
            abort(404)
        return redirect("/tasks")

