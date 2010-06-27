import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from ideabox.lib.base import BaseController, Session, render
from ideabox.model.project import Task
from ideabox.model.user import User
from datetime import datetime

log = logging.getLogger(__name__)

class TasksController(BaseController):

    def new(self):
#        did_login_or_redirect(session)
        if not request.params["projectid"]:
            return redirect("/projects")
        users = Session.query(User).all()
        return render("tasks/new.html", {"users": users, "projectid":request.params["projectid"]})

    def create(self):
#        did_login_or_redirect(session)
        task_dict = {}
        for param in request.params:
            task_dict[param] = request.params[param]
        task_dict["author"] = session["user"]["id"]
        new_task = Task(**task_dict)
        Session.add(new_task)
        Session.commit()
        return redirect("/tasks/show/%s" % new_task.id)

    def show(self, id):
        try:
            task = Session.query(Task).filter_by(id=id).one()
            assigned_user = Session.query(User).filter_by(id=task.assigned_to).one()
        except:
            abort(404)
        print task.status
        return render("tasks/show.html", {"task": task, "assigned_user":assigned_user})

    def complete(self, id):
#        did_login_or_redirect(session)
        try:
            task = Session.query(Task).filter_by(id=id).one()
        except:
            abort(404)
        mark_completed = Session.query(Task).filter_by(id=id).update({
            "status": True,
            "completed_at": datetime.now()
            })
        Session.commit()
        return redirect("/tasks/show/%s" % task.id)

    def delete(self, id):
#        did_login_or_redirect(session)
        try:
            task = Session.query(Task).filter_by(id=id).delete()
        except:
            abort(404)
        return redirect("/tasks")

