import logging
import json

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from ideabox.lib.base import BaseController, Session, render
from ideabox.model.project import Project, TaskList, Task
from ideabox.model.user import User

from formalchemy import FieldSet, Grid

log = logging.getLogger(__name__)

project_form = FieldSet(Project)
project_form.configure(
    options = [
        project_form.description.textarea(),
        project_form.users.hidden(),
        project_form.author.hidden(),
        project_form.tasklists.hidden(),
        project_form.tasks.hidden(),
    ],
    exclude = [project_form.project]
)


class ProjectsController(BaseController):

    def __before__(self, action, **params):
        filter_actions = ["new", "edit", "create", "update", "delete"]
        if "user" not in session and action in filter_actions:
            redirect("/users/login")

    def new(self):       
        context = {
            "project_form": project_form.render()
        }
        return render("projects/new.html", context)

    def create(self):
        try:
            project = Session.query(Project).filter_by(title=request.params["name"]).one()
        except:
            project_args = {
                "name": request.params["name"],
                "description": request.params["description"],
                "author_id": 1
            }
            project = Project(**project_args)
            project.tasklists = [TaskList("Default Tasks", project.id)]
            Session.add(project)
            Session.commit()
        return redirect("/projects/show/%s" % project.id)

    def index(self):
        projects = Session.query(Project).all()
        return render("projects/index.html", {"projects": projects})

    def show(self, id):
        try:
            project = Session.query(Project).filter_by(id=id).one()
        except:
            abort(404)
        tasks = Session.query(Task).filter_by(project_id=id).all()
        completed_tasks = 0
        uncompleted_tasks = 0
        for task in tasks:
            if task.completed:
                completed_tasks = completed_tasks + 1
            else:
                uncompleted_tasks = uncompleted_tasks + 1
        context = {
            "project": project,
            "tasklists": project.tasklists,
            "completed_tasks": completed_tasks,
            "uncompleted_tasks": uncompleted_tasks
        }
        return render("projects/show.html", context)

    def edit(self, id):
        project = Session.query(Project).filter_by(id=id).first()
        if project is None:
            abort(404)
        
        edit_form = project_form.bind(project)
        context = {
            "project": project,
            "project_form": edit_form.render()
        }
        return render("projects/edit.html", context)
    
    
    def save(self, id):
        project = Session.query(Project).filter_by(id=id).first()
        if project is None:
            abort(404)
        
        changed_form = project_form.bind(project, data=request.params)

        if changed_form.validate():
            changed_form.sync()
            Session.update(project)
            Session.commit()
        else:
            # TODO pass in validation errors
            return redirect("/projects/edit/%s" % project.id)
        
        return redirect("/projects/show/%s" % project.id)
    
    
    def users(self, id):
        try:
            project = Session.query(Project).filter_by(id=id).one()
        except:
            abort(404)
        return render("projects/users.html", {"project": project})

    def newuser(self, id):
        try:
            project = Session.query(Project).filter_by(id=id).one()
            user = Session.query(User).filter_by(username=request.params["username"]).one()
        except:
            abort(404)
        project.users.append(user)
        Session.commit()
        user_info = dict(id=user.id, firstname=user.firstname, lastname=user.lastname)
        return json.dumps(user_info)

    def deluser(self, id, userid):
        try:
            project = Session.query(Project).filter_by(id=id).one()
            user = Session.query(User).filter_by(id=userid).one()
        except:
            abort(404)
        if hasattr(project, "users"):
            if user in project.users:
                project.users.remove(user)
                Session.commit()
        return redirect("/projects/show/%s" % id)