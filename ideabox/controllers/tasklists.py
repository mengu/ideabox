import logging
from formalchemy import FieldSet

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from ideabox.lib.base import BaseController, Session, render
from ideabox.model.project import TaskList

log = logging.getLogger(__name__)

tasklist_form = FieldSet(TaskList)
tasklist_form.configure(
    include = [
        tasklist_form.name.required(),
    ]
)

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


    def edit(self, id=None):
        if id is not None:
            tasklist = Session.query(TaskList).filter_by(id=id).first()
            if tasklist is None:
                abort(404)

            edit_form = tasklist_form.bind(tasklist, data=request.POST or None)
            if request.POST and edit_form.validate():
                edit_form.sync()
                Session.commit()
                # TODO left off here
                #redirect("/projects/show/%s" % id)
            #context = {
            #    "project": project,
            #    "project_form": edit_form.render(),
            #}
            #return render("projects/edit.html", context)
        else:
            return redirect("/projects/new")


    def delete(self, id):
        try:
            tasklist = Session.query(TaskList).filter_by(id=id).one()
        except:
            abort(404)
        if "_method" in request.params and request.params["_method"] == "DELETE":
            Session.delete(tasklist)
            Session.commit()
            # TODO flash a message
            return redirect("/projects/show/%s" % tasklist.project.id)
        return render("tasklists/delete.html", {"tasklist": tasklist})
