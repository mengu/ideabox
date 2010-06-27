import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from ideabox.lib.base import BaseController, Session, render
from ideabox.model.project import Project, Task

log = logging.getLogger(__name__)

class ProjectsController(BaseController):

    def new(self):
        return render("projects/new.html")

    def create(self):
        try:
            project = Session.query(Project).filter_by(title=request.params["name"]).one()
        except:
            project_args = {
                "name": request.params["name"],
                "description": request.params["description"],
                "author": 1
            }
            project = Project(**project_args)
            Session.add(project)
            Session.commit()
        return redirect("/projects/show/%s" % project.id)

    def index(self):
        # Return a rendered template
        #return render('/projects.mako')
        # or, return a string
        return 'Hello World'

    def show(self, id):
        try:
            project = Session.query(Project).filter_by(id=id).one()
        except:
            abort(404)
        tasks = Session.query(Task).filter_by(project=id).all()
        context = {"project": project, "tasks": tasks}
        return render("projects/show.html", context)
