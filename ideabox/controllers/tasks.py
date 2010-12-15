import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from ideabox.lib.base import BaseController, Session, render
from ideabox.model.project import Task, TaskList, Note
from ideabox.model.user import User
from datetime import datetime
from formalchemy import FieldSet, Grid, Field, FieldRenderer

log = logging.getLogger(__name__)

class DatePickerFieldRenderer(FieldRenderer):
    def render(self):
        value = self.value and self.value or ''
        vars = dict(name=self.name, value=value)
        return """
            <input id="%(name)s" class="widthAuto" name="%(name)s" type="text" value="%(value)s" />
        """ % vars

task_form = FieldSet(Task)
task_form.configure(include=[
    task_form.task.textarea(),
    task_form.assigned_to.dropdown(
        options=[(user.username, user.id) for user in Session.query(User).all()]
    ).required(),
    task_form.deadline.with_renderer(DatePickerFieldRenderer),
    #task_form.tasklist_id,
    #task_form.project_id.hidden(),
])

class TasksController(BaseController):

    def __before__(self, action, **params):
        filter_actions = ["new", "edit", "create", "update", "delete"]
        if "user" not in session and action in filter_actions:
            redirect("/users/login")

    def new(self):
        # TODO this doesn't work
        if not request.params["tasklist"] or \
            not request.params["project"]:
                # TODO do something bad
                return redirect("/projects")
        #task_form.append(Field(name="tasklist_id", value=request.params["tasklist"]))
        #task_form.append(Field(name="project_id", value=request.params["project"]))
        return render("tasks/new.html", {
            "task_form": task_form.render(),
            "tasklist_id": request.params["tasklist"],
            "project_id": request.params["project"]
        })

    def create(self):
        create_form = task_form.bind(Task, data=request.params)

        if request.POST and create_form.validate():
            task_args = {
                "task": create_form.task.value,
                "tasklist_id": request.params["tasklist_id"], #create_form.tasklist_id.value,
                "project_id": request.params["project_id"], #create_form.project_id.value,
                "user_id": 1, # TODO fix this
                "assigned_to": create_form.assigned_to.value,
                "deadline": create_form.deadline.value
            }
            task = Task(**task_args)
            Session.add(task)
            Session.commit()
            return redirect("/projects/show/%s" % task_args["project_id"])

        context = {
        }
        return render("tasks/new.html", {
            "task_form": create_form.render(),
            "tasklist_id": request.params["tasklist"],
            "project_id": request.params["project"],
        })

    def show(self, id):
        try:
            task = Session.query(Task).filter_by(id=id).one()
        except:
            abort(404)
        notes = Session.query(Note).filter_by(task=id).all()
        return render("tasks/show.html", {"task": task, "notes": notes})

    def edit(self, id=None):
        try:
            task = Session.query(Task).filter_by(id=id).one()
        except:
            abort(404)

        edit_form = task_form.bind(task, data=request.POST or None)
        tasklist = Field('tasklist_id').dropdown(
            options=[(tasklist.name, tasklist.id) for tasklist in Session.query(TaskList).\
                        filter_by(project_id=task.project_id).all()]).\
            required().label('Task List')
        edit_form.append(tasklist)

        if request.POST and edit_form.validate():
            task.tasklist = Session.query(TaskList).filter_by(id=request.POST.values()[-1]).one()
            edit_form.sync()
            Session.commit()
            return redirect("/projects/show/%s" % task.project_id)

        return render("tasks/edit.html", {
            "task": task,
            "task_form": edit_form.render()
        })

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
            task = Session.query(Task).filter_by(id=id)
            proj_id = task.one().project.id
            task.delete()
        except:
            abort(404)
        return redirect("/projects/show/%s" % proj_id)

