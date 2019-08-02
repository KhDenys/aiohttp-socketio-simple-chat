import aiohttp_jinja2

from datetime import datetime

from aiohttp import web
from aiohttp_session import get_session
from socketio import AsyncNamespace
from main.settings import config
from chat.models import Message


class ChatView(web.View):
    @aiohttp_jinja2.template('chat/index.html')
    async def get(self):
        message = Message(self.request.app['db'])
        messages = await message.get_messages()
        return {'messages': messages,
                'port': config['PORT']}


class ChatNamespace(AsyncNamespace):
    async def on_connect(self, sid, environ):
        self.db = environ['aiohttp.request'].app['db']

        session = await get_session(environ['aiohttp.request'])
        async with self.session(sid) as sio_session:
            sio_session['username'] = session['user']['login']

    async def on_client(self, sid, message):
        async with self.session(sid) as sio_session:
            data = {
                    'username': sio_session['username'],
                    'time': str(datetime.now()),
                    'msg': message
                }

            message = Message(self.db)
            await message.save(**data)
            await self.emit(
                'server',
                data,
                skip_sid=sid
            )
