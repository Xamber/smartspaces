from aiohttp import web
import asyncio


class IndexHandler(web.View):

    async def get(self):
        return web.Response(body=b"Smart Spaces")


class WebSocketHandler(web.View):

    async def get(self):
        return web.Response(body=b"Smart Spaces")


async def create_app():
    # настройка приложения

    app = web.Application()

    app.router.add_route('GET', '/', IndexHandler)
    app.router.add_route('GET', '/ws', WebSocketHandler)

    app.router.add_static('/static', 'static')

    return app


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(create_app())
    web.run_app(app, port=1337)
