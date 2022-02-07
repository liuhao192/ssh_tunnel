#!/usr/bin/env python
# -*- coding:utf-8 -*-
from tkinter import messagebox

from sshtunnel import SSHTunnelForwarder

def operate_sshtunnel(tunnel_info):
    try:
        tunnel = SSHTunnelForwarder(
            (tunnel_info.ssh_ip, int(tunnel_info.ssh_port)),
            ssh_username=tunnel_info.ssh_username,
            ssh_password=tunnel_info.ssh_password,
            remote_bind_address=(tunnel_info.remote_ip, int(tunnel_info.remote_port)),
            local_bind_address=('127.0.0.1', int(tunnel_info.localhost_port))
        )
        return tunnel
    except Exception as e:
        print(e.args[0])
        messagebox.showinfo(title='连接异常', message=e.args[0])
        return


