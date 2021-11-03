# -*- coding: utf-8 -*-
import asyncio


class IoLoop:
    @staticmethod
    def run_sync(func, args=None, kwargs=None, loop=None):
        if kwargs is None:
            kwargs = {}
        if args is None:
            args = []
        if not loop:
            loop = asyncio.events.get_event_loop()
        return loop.run_until_complete(func(*args, **kwargs))
