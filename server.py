import os
import jinja2
from aiohttp import web
import asyncio
import aiohttp_jinja2
import simplejson as json


class User:
    _online = []
    _summ = 0

    @classmethod
    def broadcast(cls, on_disconnect=False):
        info = json.dumps(dict(summ=cls._summ, online=len(cls._online)))
        for u in cls._online:
            if not u.ws.closed:
                u.ws.send_str(info)

    @classmethod
    def change_summ(cls, diff):
        cls._summ -= diff

    def __init__(self, ws):
        self.number = 0
        self.ws = ws
        self._online.append(self)
        self.reset()

    async def disconnect(self):
        self.reset()
        await self.ws.close()
        self._online.remove(self)
        self.broadcast()

    def receive_number(self, new_number):
        new_number = int(new_number)
        self.change_summ(self.number - new_number)
        self.number = new_number
        self.broadcast()

    def reset(self):
        self.receive_number(0)


@aiohttp_jinja2.template('index.html')
class IndexHandler(web.View):
    async def get(self):
        return {'method': self.request.method}


class WebSocketHandler(web.View):
    async def get(self):
        ws = web.WebSocketResponse()
        await ws.prepare(self.request)

        user = User(ws)

        try:
            async for msg in ws:
                if msg.tp == web.MsgType.text:
                    user.receive_number(msg.data)
                elif msg.tp == web.MsgType.error:
                    continue  # тут обработка ошибки
        finally:
            await user.disconnect()
            del user

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
    application = loop.run_until_complete(create_app())
    web.run_app(application, port=1337)
