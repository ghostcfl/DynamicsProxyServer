# -*- coding:utf-8 -*-
import socket

import aioredis
import config

config = config.redis_config(True)
async_redis_cli = aioredis.from_url(
    socket_keepalive=True,
    socket_keepalive_options={socket.TCP_KEEPIDLE: 60, socket.TCP_KEEPINTVL: 30, socket.TCP_KEEPCNT: 3},
    **config
)
