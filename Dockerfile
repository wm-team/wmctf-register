FROM python:3.11-slim-bullseye

RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list && \
    apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y figlet openssh-server && \
    pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

COPY requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt

WORKDIR /app

COPY . /app

COPY entrypoint.sh /entrypoint.sh

COPY ./pow.py /usr/bin/pow.py

RUN sed -i 's|#PermitEmptyPasswords no|PermitEmptyPasswords yes|' /etc/ssh/sshd_config &&\
    mkdir /run/sshd &&\
    echo '' > /etc/motd &&\
    echo '#!/bin/bash\npython3 /app/main.py' >> /usr/bin/register &&\
    chmod +x /usr/bin/register &&\
    useradd -p '' -d /app -s /usr/bin/register wmctf

EXPOSE 22

ENTRYPOINT [ "/entrypoint.sh" ]
