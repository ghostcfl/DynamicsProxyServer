FROM python:3.9.7-slim-buster

WORKDIR /DynamicsProxyServer
RUN apt-get update
RUN apt-get install -y vim git
COPY . .
RUN python -m pip install --upgrade pip -i https://mirrors.aliyun.com/pypi/simple
RUN pip install -r requirement.txt -i https://mirrors.aliyun.com/pypi/simple
# docker build -t DynamicsProxyServer .
# docker run --name DynamicsProxyServer -p 18001:18001 -itd DynamicsProxyServer python main.py --listhen_port 18001
