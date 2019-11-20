from aiohttp import web

from . import abusereport


async def App():
    app = web.Application()

    app.router.add_post('/', abusereport.receive_report)

    return app


if __name__ == '__main__':
    web.run_app(App())

