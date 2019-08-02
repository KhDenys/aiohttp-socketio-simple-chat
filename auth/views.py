from time import time

import aiohttp_jinja2
from aiohttp import web
from aiohttp_session import get_session
from auth.models import User


def get_url(request, router_name):
    return request.app.router[router_name].url_for()


def redirect(request, router_name):
    url = get_url(request, router_name)
    raise web.HTTPFound(url)


def set_session(session, user, request):
    user['_id'] = str(user['_id'])

    session['user'] = user
    session['last_visit'] = time()

    redirect(request, 'index')


class SignIn(web.View):
    @aiohttp_jinja2.template('auth/login.html')
    async def get(self):
        session = await get_session(self.request)
        if session.get('user'):
            redirect(self.request, 'index')
        return {'conten': 'Please enter LOGIN and PASSWORD',
                'signup': get_url(self.request, 'signup')}

    async def post(self):
        data = await self.request.post()
        user = User(self.request.app['db'], data)
        result = await user.check_user()
        if isinstance(result, dict):
            session = await get_session(self.request)
            set_session(session, result, self.request)
        raise web.HTTPFound(get_url(self.request, 'index'))


class SignUp(web.View):
    @aiohttp_jinja2.template('auth/signup.html')
    async def get(self):
        session = await get_session(self.request)
        if session.get('user'):
            redirect(self.request, 'index')
        return {'conten': 'Please enter your data'}

    async def post(self):
        data = await self.request.post()
        user = User(self.request.app['db'], data)
        result = await user.create_user()
        if isinstance(result, dict):
            session = await get_session(self.request)
            set_session(session, result, self.request)
        raise web.HTTPFound(get_url(self.request, 'index'))


class SignOut(web.View):
    async def get(self):
        session = await get_session(self.request)
        if session.get('user'):
            del session['user']

        raise web.HTTPFound(get_url(self.request, 'signin'))
