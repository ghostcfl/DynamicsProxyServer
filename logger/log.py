# -*- coding: utf-8 -*-
import sys
import datetime
import os
from loguru import logger
import config

log_config = {
    "handlers": [
        {
            "sink": sys.stdout,
            "level": config.get('log', 'std_level'),
        },
        {
            "sink": os.path.join(os.path.dirname(__file__), f"{datetime.date.today()}.log"),  # log文件的路径
            "format": "{time:YYYY-MM-DD HH:mm:ss} | {level} | {file}:{line} | {message}",
            "enqueue": True,
            "rotation": '00:00',  # 每天 0 点创建一个文件
            "level": config.get('log', 'file_level'),
            "encoding": "utf-8",
        },
    ]
}
logger.configure(**log_config)
