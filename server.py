import os

import jinja2
from aiohttp import web
import asyncio
import aiohttp_jinja2


@aiohttp_jinja2.template('index.html')
class IndexHandler(web.View):
    async def get(self):
        return {}


online_users = []


class WebSocketHandler(web.View):
    async def get(self):
        ws = web.WebSocketResponse()
        await ws.prepare(self.request)

        online_users.append(ws)

        try:
            async for msg in ws:
                if msg.tp == web.MsgType.text:
                    pass # todo:
                elif msg.tp == web.MsgType.error:
                    continue  # тут обработка ошибки
        finally:
            await ws.close()
            online_users.remove(ws)

        return ws


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
