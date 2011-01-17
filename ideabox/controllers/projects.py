import logging
import json
from formalchemy import FieldSet, Grid

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from ideabox.lib.base import BaseController, Session, render
from ideabox.model.project import Project, TaskList, Task
from ideabox.model.user import User
import ideabox.model as model

log = logging.getLogger(__name__)

project_form = FieldSet(Project)
project_form.configure(
    include = [
        project_form.name,
        project_form.description.textarea(),
    ]
)
# TODO project description will get cut off after 300 chars. The use should be warned.


class ProjectsController(BaseController):

    filter_actions = ["new", "edit", "create", "update", "delete", 'index']

    def new(self):
        context = {
            "project_form": project_form.render()
        }
        return render("projects/new.html", context)


    def create(self):
        create_form = project_form.bind(Project, data=request.params)
        if request.POST and create_form.validate():
            project_args = {
                #"name": request.params["Project--name"],
                "name": create_form.name.value,
                #"description": request.params["Project--description"],
                "description": create_form.description.value,
                "author_id": 1, # TODO set this based on logged-in user
            }
            project = Project(**project_args)
            project.tasklists = [TaskList("Tasks", project.id)]
            Session.add(project)
            Session.commit()
            return redirect("/projects/show/%s" % project.id)
        return render("/projects/new.html", {"project_form": create_form.render()})


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


    def edit(self, id=None):
        if id is not None:
            project = Session.query(Project).filter_by(id=id).first()
            if project is None:
                abort(404)
        else:
            return redirect("/projects/new")
        edit_form = project_form.bind(project, data=request.POST or None)
        if request.POST and edit_form.validate():
            edit_form.sync()
            # NOTE id is probably never none, consider removing
            if id is None:
                Session.add(project)
            Session.commit()
            redirect("/projects/show/%s" % id)
        context = {
            "project": project,
            "project_form": edit_form.render(),
        }
        return render("projects/edit.html", context)


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
