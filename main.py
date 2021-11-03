import argparse

from proxy_server import ProxyServer

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='隧道代理服务器')
    parser.add_argument('--listen_port',metavar='', help='设置服务器监听端口，默认使用18001', type=int, default=18001)
    parser.add_argument('--bind',metavar='', help='设置绑定IP使用，默认使用0.0.0.0，任意IP可以连接使用', type=str, default='0.0.0.0')
    args = parser.parse_args()

    ProxyServer.start(**{
        'listen_port': args.listen_port,
        'bind': args.bind
    })
