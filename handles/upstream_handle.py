# -*- coding: utf-8 -*-
import asyncio

import config
from db_tools import async_redis_cli
from logger import logger


class UpstreamProxyHandle:
    def __init__(self):
        self.__redis_key = config.get('application', 'proxy_redis_key')

    def __format_upstream(self, upstream_server):
        ip, port = upstream_server.split(':')
        return ip, int(port)

    async def __copy_data_thread(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        while True:
            chunk = await reader.read(65536)
            if not chunk:
                break
            writer.write(chunk)
            await writer.drain()
        writer.close()

    async def __get_proxy_from_redis(self):
        upstream_server = await async_redis_cli.srandmember(self.__redis_key)
        return self.__format_upstream(upstream_server)

    async def download(self, a_reader: asyncio.StreamReader, a_writer: asyncio.StreamWriter):
        __remote_ip, __remote_port = await self.__get_proxy_from_redis()

        logger.info(f'connect upstream server {__remote_ip}')
        c_reader, c_writer = await asyncio.open_connection(
            host=__remote_ip,
            port=__remote_port
        )

        download_task = set()
        download_task.add(asyncio.ensure_future(self.__copy_data_thread(c_reader, a_writer)))
        download_task.add(asyncio.ensure_future(self.__copy_data_thread(a_reader, c_writer)))
        await asyncio.wait(download_task, return_when=asyncio.FIRST_COMPLETED)


if __name__ == '__main__':
    UpstreamProxyHandle()
