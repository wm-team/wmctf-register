FROM python:3.9-slim

RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list && \
    apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y socat figlet && \
    pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip install pip lolcat -U

COPY requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt

WORKDIR /app

COPY . /app

COPY entrypoint.sh /entrypoint.sh

EXPOSE 8000

ENTRYPOINT [ "/entrypoint.sh" ]