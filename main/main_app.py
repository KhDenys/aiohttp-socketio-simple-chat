import socketio

from aiohttp import web
from motor import motor_asyncio

from auth.routers import routes as auth_routes
from chat.routers import routes as chat_routes
from chat import ChatNamespace

from .middlewares import authorize
from .utils import (setup_debugtoolbar,
                    setup_jinja2,
                    setup_session,
                    setup_routers)


def create_app(config):
    app = web.Application()
    app['config'] = config

    setup_debugtoolbar(app, config['DEBUG'])
    setup_jinja2(app)
    setup_session(app, config['SECRET_KEY'])
    setup_routers(app, chat_routes + auth_routes)

    app.middlewares.append(authorize)

    app.on_startup.append(mongodb_setup)
    app.on_cleanup.append(mongodb_shutdown)

    sio = socketio.AsyncServer(async_mode='aiohttp')
    sio.attach(app)
    sio.register_namespace(ChatNamespace('/chat'))

    return app


async def mongodb_setup(app):
    mongodb_config = app['config']['mongodb_config']
    app['mongodb_client'] = motor_asyncio.AsyncIOMotorClient(mongodb_config['HOST'])
    app['db'] = app['mongodb_client'][mongodb_config['DB_NAME']]


async def mongodb_shutdown(app):
    app['mongodb_client'].close()
