import configparser
import json
import os
import re

config_file_path = os.path.join(os.path.dirname(__file__), 'config.ini')
__config = configparser.ConfigParser()

__config.read(config_file_path)

get = __config.get

sections = __config.sections


def redis_config(get_url=False) -> dict:
    res = {}
    for item in __config.items('redis'):
        if item[1] == 'true':
            res[item[0]] = True
        elif item[1] == 'false':
            res[item[0]] = False
        elif '{' in item[1] or '[' in item[1]:
            res[item[0]] = json.loads(item[1])
        elif re.match('^\d+$', item[1]):
            res[item[0]] = int(item[1])
        else:
            res[item[0]] = item[1]
    if get_url:
        res['url'] = f'redis://{res["host"]}'
        res.pop('host')
    return res
