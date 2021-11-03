import asyncio

from handles import UpstreamProxyHandle
from logger import logger
from io_loop import IoLoop
from db_tools import async_redis_cli


class ProxyServer:
    def __init__(self, *args, **kwargs):
        self.bind = kwargs.get('bind', '0.0.0.0')
        self.port = kwargs.get('listen_port', 18001)

        self.handle = UpstreamProxyHandle()

    @classmethod
    def start(cls, *args, **kwargs):
        c = cls(*args, **kwargs)
        loop = asyncio.get_event_loop()
        future = asyncio.start_server(c.handle.download, c.bind, c.port, loop=loop)
        server = loop.run_until_complete(future)

        logger.warning(f'server listen on port:{c.port},bind_ip:{c.bind}')
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            ...
        finally:
            IoLoop.run_sync(async_redis_cli.close, loop=loop)
            server.close()
            IoLoop.run_sync(server.wait_closed, loop=loop)
