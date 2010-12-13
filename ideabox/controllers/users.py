# -*- coding: utf-8 -*-
import logging
import hashlib
import json
from formalchemy import FieldSet, Field

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from ideabox.lib.base import BaseController, Session, render
from ideabox.model.user import User

log = logging.getLogger(__name__)

user_form = FieldSet(User)
user_form.configure(
    include = [
        user_form.username.required(),
        user_form.firstname,
        user_form.lastname,
        user_form.email.required()
    ]
)

class UsersController(BaseController):

    def new(self):
        return render('users/new.html', {'user_form': user_form.render()})

    def create(self):
        password = request.POST.pop('password')
        password_conf = request.POST.pop('password2')
        create_form = user_form.bind(User, data=request.POST)
        if request.POST and create_form.validate():
            user_dict = {
                'firstname': create_form.firstname.value,
                'lastname': create_form.lastname.value,
                'username': create_form.username.value.strip(),
                'email': create_form.email.value.strip(),
            }
            if password == password_conf:
                user_dict['password'] = hashlib.md5(password).hexdigest()
                user = User(**user_dict)
                Session.add(user)
                Session.commit()
                session['user'] = {'id': user.id, 'name': '%s %s' % (user.firstname, user.lastname)}
                session.save()
                return redirect('/projects')
            else:
                session['flash'] = 'Passwords did not match'
                session.save()
        return render('users/new.html', {'user_form': create_form.render()})

    def edit(self, id):
        if id is not None:
            user = Session.query(User).filter_by(id = id).first()
            if user is None:
                #TODO something better than 404
                abort(404)
            edit_form = user_form.bind(user, data=request.POST or None)
            if request.POST and edit_form.validate():
                edit_form.sync()
                # NOTE id is probably never none, consider removing
                if id is None:
                    Session.add(user)
                Session.commit()
                #redirect("/projects/show/%s" % id)
                session['flash'] = 'User updated'
            return render('users/edit.html', {
                'user': user,
                'user_form': edit_form.render()
            })
        else:
            return redirect('/users/new')

    def login(self):
        return render('users/login.html')

    def dologin(self):
        if request.params['email'] and request.params['password']:
            password = hashlib.md5(request.params['password']).hexdigest()
            try:
                user = Session.query(User).filter(User.email==request.params['email']).\
                    filter(User.password==password).one()
            except:
                return render('users/login.html')
            session['user'] = {'id': user.id, 'name': '%s %s' % (user.firstname, user.lastname)}
            session.save()
            return redirect('/projects')
        else:
            return redirect('/users/login')

    def logout(self):
        if 'user' not in session:
            return redirect('/')
        else:
            session.pop('user')
            session.save()
            return redirect('/')

    def find(self):
        users = Session.query(User).filter(User.username.like(request.params['q']+'%')).all()
        for user in users:
            yield user.username

