from ideabox.tests import *

class TestTasksController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='tasks', action='index'))
        # Test response...
