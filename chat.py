from aiohttp import web

from main import create_app
from main.settings import config


app = create_app(config)

if __name__ == '__main__':
    web.run_app(app, host=config['HOST'], port=config['PORT'])
