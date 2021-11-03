### 简易隧道代理服务器

* 可以动态的切换代理
* 依赖
    * loguru # 日志输出第三方包
    * aioredis # 异步的redis第三方包

#### 一、安装依赖

* 普通安装使用

```commandline
pip install -r requirement.txt -i https://mirrors.aliyun.com/pypi/simple
```

* docker 安装

```shell
docker build -t DynamicsProxyServer . # 创建镜像
docker run --name DynamicsProxyServer -p 18001:18001 -itd DynamicsProxyServer python main.py --listhen_port 18001 # 运行容器
firewall-cmd --permanent --add-port=18001/tcp # 打开防火墙端口
```

#### 二、配置文件

* 复制配置文件 default_config.ini 并重命名 config.ini
* 配置 redis 的参数

#### 三、存储上游代理

* 将上游戏代理存储在 redis 当中
* 代理池键名在配置文件中配置
* 上游戏代理的格式 ip:port
* 例如 127.0.0.1:45525
* 最后是有个代理池程序来维护这个键
* 确保代理池的可用性

#### 四、运行

```commandline
python main.py --listen_port 18001 --bind 0.0.0.0
```

#### 五、使用

* 以 httpx 为例子

```python
# -*- coding: utf-8 -*-
import asyncio

import httpx


async def _request(client, i):
    while 1:
        try:
            resp = await client.get('https://httpbin.org/get')
        except httpx.ProxyError:
            continue
        else:
            print(resp.text)
            break


async def run():
    # 如果上游代理有认证，需要在这里把认证带上
    # 用户名:密码@代理服务器IP:端口
    p = 'username:password@127.0.0.1:18001'
    # 如果上游借没有认证，直接使用
    p = '127.0.0.1:18001'
    proxies = {
        'http://': f'http://{p}',
        'https://': f'http://{p}',
    }
    async with httpx.AsyncClient(proxies=proxies, timeout=10) as client:
        task_list = []
        for i in range(32):
            task_list.append(asyncio.create_task(_request(client, i)))
        await asyncio.wait(task_list)


if __name__ == '__main__':
    asyncio.run(run())

```