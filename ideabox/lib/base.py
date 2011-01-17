"""The base Controller API

Provides the BaseController class for subclassing.
"""
from pylons import session, request
from pylons.controllers import WSGIController
from pylons.controllers.util import redirect
from pylons.templating import render_mako as render

from ideabox.model.meta import Session

class BaseController(WSGIController):
    filter_actions = ["new", "edit", "create", "update", "delete"]

    def __before__(self, action, **params):
        if "user" not in session and action in self.filter_actions:
            session['path_before_login'] = request.path_info
            session.save()
            redirect("/users/login")

    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        # WSGIController.__call__ dispatches to the Controller method
        # the request is routed to. This routing information is
        # available in environ['pylons.routes_dict']
        try:
            return WSGIController.__call__(self, environ, start_response)
        finally:
            Session.remove()
