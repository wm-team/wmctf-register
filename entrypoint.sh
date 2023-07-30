#!/bin/sh
env | grep _ >> /etc/environment
/usr/sbin/sshd -D -e
