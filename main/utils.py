import hashlib

import jinja2
import aiohttp_debugtoolbar


from aiohttp import web
from aiohttp_jinja2 import setup as jinja2_setup
from aiohttp_session import setup as session_setup
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from aiohttp_debugtoolbar.main import default_settings

from .settings import STATIC_PATH, TEMPLATES_PATH


def setup_debugtoolbar(app, DEBUG):
    if DEBUG:
        default_settings['intercept_redirects'] = False
        aiohttp_debugtoolbar.setup(app)


def setup_jinja2(app):
    jinja2_setup(app, loader=jinja2.FileSystemLoader(TEMPLATES_PATH))


def setup_routers(app, routes):
    for route in routes:
        app.router.add_route(route[0], route[1], route[2], name=route[3])

    app['static_root_url'] = '/static'
    app.add_routes([web.static('/prefix', STATIC_PATH)])


def setup_session(app, SECRET_KEY):
    cookie_storage = EncryptedCookieStorage(
        hashlib.sha256(bytes(SECRET_KEY, 'utf-8')).digest()
    )
    session_setup(app, cookie_storage)
