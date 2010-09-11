import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from ideabox.lib.base import BaseController, Session, render
from ideabox.model.project import TaskList

log = logging.getLogger(__name__)

class TasklistsController(BaseController):
    
    def create(self):
        tasklist_args = {
            "name": request.params["tasklist_name"],
            "project_id": request.params["project_id"]
        }
        tasklist = TaskList(**tasklist_args)
        Session.add(tasklist)
        Session.commit()
        
        return redirect("/projects/show/%s" % tasklist.project.id)
    
    def delete(self, id):
        if id is None:
            abort(404)
        tasklist = Session.query(TaskList).filter_by(id=id).one()
        if tasklist is None:
            abort(404)
        Session.delete(tasklist)
        Session.commit()
        return redirect("/projects/show/%s" % tasklist.project.id)