import os

import jinja2
from aiohttp import web
import asyncio
import aiohttp_jinja2



@aiohttp_jinja2.template('index.html')
class IndexHandler(web.View):
    async def get(self):
        return {}


class WebSocketHandler(web.View):
    async def get(self):
        return web.Response(body=b"Smart Spaces")


async def create_app():
    # настройка приложения

    app = web.Application()

    app.router.add_route('GET', '/', IndexHandler)
    app.router.add_route('GET', '/ws', WebSocketHandler)

    app.router.add_static('/static', 'static')

    template_dir = os.path.dirname(os.path.abspath(__file__)) + '/templates/'
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(template_dir), context_processors=[])

    return app


if __name__ == '__main__':



    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(create_app())
    web.run_app(app, port=1337)
