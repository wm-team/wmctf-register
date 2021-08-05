#!/bin/sh
cd /app && socat -T60 TCP4-LISTEN:8000,reuseaddr,fork EXEC:"/usr/bin/env python -u app.py",pty,stderr