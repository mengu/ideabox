import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from ideabox.lib.base import BaseController, Session, render
from ideabox.model.project import Task, Note
from ideabox.model.user import User
from datetime import datetime
from formalchemy import FieldSet, Grid

log = logging.getLogger(__name__)

class TasksController(BaseController):

    def __before__(self, action, **params):
        filter_actions = ["new", "edit", "create", "update", "delete"]
        if "user" not in session and action in filter_actions:
            redirect("/users/login")

    def new(self):
        if not request.params["tasklist"]:
            return redirect("/projects")
        users = Session.query(User).all()
        context = {
            "users": users,
            "tasklist_id": request.params["tasklist"],
            "project_id": request.params["project"]
        }
        return render("tasks/new.html", context)

    def create(self):
        task_dict = {}
        for param in request.params:
            task_dict[param] = request.params[param]
        task_dict["user_id"] = unicode(session["user"]["id"])
        new_task = Task(**task_dict)
        Session.add(new_task)
        Session.commit()
        return redirect("/projects/show/%s" % new_task.tasklist.project.id)

    def show(self, id):
        try:
            task = Session.query(Task).filter_by(id=id).one()
        except:
            abort(404)
        notes = Session.query(Note).filter_by(task=id).all()
        return render("tasks/show.html", {"task": task, "notes": notes})

    def complete(self, id):
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
        try:
            task = Session.query(Task).filter_by(id=id).delete()
        except:
            abort(404)
        return redirect("/projects/index")

