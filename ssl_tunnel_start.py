import json
import os
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Treeview
import ssl_tunnel
import cryptocode

global localhost_port
localhost_port = None
global ssh_ip
ssh_ip = None
global ssh_port
ssh_port = None
global ssh_password
ssh_password = None
global ssh_username
ssh_username = None
global remote_ip
remote_ip = None
global remote_port
remote_port = None
global tunnel_name
tunnel_name = None
global treeview
treeview = None
global tunnel_row_id
tunnel_row_id = None
global boolvar
boolvar = None
global password_entry
password_entry = None
global showpwd
showpwd = None

tunnel_infos = {}

tunnel_infos_start = {}


class tunnel_info_class:
    localhost_port = ""
    ssh_ip = ""
    ssh_port = ""
    ssh_username = ""
    ssh_password = ""
    remote_ip = ""
    remote_port = ""
    tunnel_name = ""


def clear():
    localhost_port.set('port')
    ssh_ip.set('ssh ip')
    ssh_port.set('ssh port')
    ssh_username.set('ssh username')
    ssh_password.set('ssh password')
    ##目的地的ip端口
    remote_ip.set('remote ip')
    remote_port.set('remote port')
    tunnel_name.set('tunnel_name')
    tunnel_row_id.set('')


def save_config():
    tunnel_info = tunnel_info_class()
    tunnel_row_id_value = tunnel_row_id.get()
    if tunnel_row_id_value != "" and tunnel_row_id_value != None:
        if tunnel_row_id_value in tunnel_infos.keys():
            tunnel_info = tunnel_infos[tunnel_row_id_value]
        if tunnel_row_id_value in tunnel_infos_start.keys():
            messagebox.showinfo(title='修改提醒', message='服务已启动，无法修改')
            return

    localhost_port_value = localhost_port.get()
    if localhost_port_value != "" and localhost_port_value != "port":
        tunnel_info.localhost_port = localhost_port_value
    else:
        messagebox.showinfo(title='输入提示', message='本地端口不能为空')
        return
    ssh_ip_value = ssh_ip.get()
    if ssh_ip_value != "" and ssh_ip_value != "ssh ip":
        tunnel_info.ssh_ip = ssh_ip_value
    else:
        messagebox.showinfo(title='输入提示', message='中转地址不能为空')
        return
    ssh_port_value = ssh_port.get()
    if ssh_port_value != "" and ssh_port_value != "ssh port":
        tunnel_info.ssh_port = ssh_port_value
    else:
        messagebox.showinfo(title='输入提示', message='中转端口不能为空')
        return
    ssh_password_value = ssh_password.get()
    if ssh_password_value != "" and ssh_password_value != "ssh password":
        tunnel_info.ssh_password = ssh_password_value
    else:
        messagebox.showinfo(title='输入提示', message='中转服务器密码不能为空')
        return
    ssh_username_value = ssh_username.get()
    if ssh_username_value != "" and ssh_username_value != "ssh username":
        tunnel_info.ssh_username = ssh_username_value
    else:
        messagebox.showinfo(title='输入提示', message='中转服务器账户不能为空')
        return
    remote_ip_value = remote_ip.get()
    if remote_ip_value != "" and remote_ip_value != "remote ip":
        tunnel_info.remote_ip = remote_ip_value
    else:
        messagebox.showinfo(title='输入提示', message='目标服务器地址不能为空')
        return
    remote_port_value = remote_port.get()
    if remote_port_value != "" and remote_port_value != "remote port":
        tunnel_info.remote_port = remote_port_value
    else:
        messagebox.showinfo(title='输入提示', message='目标端口不能为空')
        return
    tunnel_name_value = tunnel_name.get()
    if tunnel_name_value != "" and remote_port_value != "tunnel_name":
        tunnel_info.tunnel_name = tunnel_name_value
    tree_id = ""
    if tunnel_row_id_value != "" and tunnel_row_id_value != None:
        if tunnel_row_id_value in tunnel_infos.keys():
            tree_id = tunnel_row_id_value
            update_tree_view(tunnel_row_id_value, tunnel_info, "未启动")
    else:
        tree_id = insert_tree_view(tunnel_info, "未启动")
    tunnel_infos.update({tree_id: tunnel_info})
    tunnel_row_id.set(tree_id)
    write_json()
    ##保存到json文件中


def read_json():
    if os.path.exists('tunnel_data.json'):
        with open('tunnel_data.json', 'r', encoding='utf-8') as load_f:
            data = load_f.read()
        if len(data) > 0:
            json_str = cryptocode.decrypt(data, "EjdeB55cvQMN2WHf")
            return json.loads(json_str)
        else:
            return


def write_json():
    tunnel_info_arr = []
    for tunnel_key in tunnel_infos:
        tunnel_info = tunnel_infos[tunnel_key]
        tunnel_info_json = {}
        tunnel_info_json['localhost_port'] = tunnel_info.localhost_port
        tunnel_info_json['ssh_ip'] = tunnel_info.ssh_ip
        tunnel_info_json['ssh_port'] = tunnel_info.ssh_port
        tunnel_info_json['ssh_username'] = tunnel_info.ssh_username
        tunnel_info_json['ssh_password'] = cryptocode.encrypt(tunnel_info.ssh_password, "F1jgEg1arVyxmUqC")
        tunnel_info_json['remote_ip'] = tunnel_info.remote_ip
        tunnel_info_json['remote_port'] = tunnel_info.remote_port
        tunnel_info_json['tunnel_name'] = tunnel_info.tunnel_name
        tunnel_info_arr.append(tunnel_info_json)
    json_str = json.dumps(tunnel_info_arr)
    json_str = cryptocode.encrypt(json_str, "EjdeB55cvQMN2WHf")
    with open('tunnel_data.json', 'w', encoding='utf-8') as json_file:
        json_file.write(json_str)


def start_tunnel():
    iid = treeview.selection()
    if len(iid) > 0:
        if iid[0] not in tunnel_infos_start.keys():
            tunnel_info = tunnel_infos[iid[0]]
            try:
                tunnel = ssl_tunnel.operate_sshtunnel(tunnel_info)
                if tunnel is not None:
                    tunnel.start()
                    tunnel_infos_start.update({iid[0]: tunnel})
                    update_tree_view(iid[0], tunnel_info, "启动")
                    pass
            except Exception  as e:
                messagebox.showinfo(title='连接异常', message=e.args[0])
    else:
        messagebox.showinfo(title='选择异常', message="未选择列表")


def stop_tunnel():
    iid = treeview.selection()
    if len(iid) > 0:
        if iid[0] in tunnel_infos_start.keys():
            tunnel_info = tunnel_infos[iid[0]]
            tunnel = tunnel_infos_start[iid[0]]
            if tunnel is not None:
                try:
                    tunnel.stop()
                    tunnel_infos_start.pop(iid[0])
                    update_tree_view(iid[0], tunnel_info, "未启动")
                    pass
                except Exception  as e:
                    messagebox.showinfo(title='连接异常', message=e.args[0])
    else:
        messagebox.showinfo(title='选择异常', message="未选择列表")


def remove_tunnel():
    iid = treeview.selection()
    if len(iid) > 0:
        if iid[0] in tunnel_infos_start.keys():
            stop_tunnel()
        ## 从列表删除
        treeview.delete(iid)
        tunnel_infos.pop(iid[0])
        write_json()
    else:
        messagebox.showinfo(title='选择异常', message="未选择列表")


def on_click(event):
    global localhost_port, ssh_ip, ssh_port, ssh_password, ssh_username, remote_ip, remote_port, tunnel_name, treeview, tunnel_row_id
    iid = treeview.selection()
    if len(iid) > 0:
        if iid[0] in tunnel_infos.keys():
            tunnel_info = tunnel_infos[iid[0]]
            localhost_port.set(tunnel_info.localhost_port)
            ssh_ip.set(tunnel_info.ssh_ip)
            ssh_port.set(tunnel_info.ssh_port)
            ssh_password.set(tunnel_info.ssh_password)
            ssh_username.set(tunnel_info.ssh_username)
            remote_ip.set(tunnel_info.remote_ip)
            remote_port.set(tunnel_info.remote_port)
            tunnel_name.set(tunnel_info.tunnel_name)
            tunnel_row_id.set(iid[0])


def update_tree_view(id, tunnel_info, state):
    treeview.item(id, values=(tunnel_info.tunnel_name, tunnel_info.localhost_port,
                              tunnel_info.ssh_username + "@" + tunnel_info.ssh_ip + ":" + tunnel_info.ssh_port,
                              tunnel_info.remote_port + ":" + tunnel_info.remote_ip,
                              state
                              ))


def insert_tree_view(tunnel_info, state):
    return treeview.insert("", len(tunnel_infos) - 1, values=(tunnel_info.tunnel_name, tunnel_info.localhost_port,
                                                              tunnel_info.ssh_username + "@" + tunnel_info.ssh_ip + ":" + tunnel_info.ssh_port,
                                                              tunnel_info.remote_port + ":" + tunnel_info.remote_ip,
                                                              "未启动"
                                                              ))


def start_all_tunnel():
    for tunnel_id in tunnel_infos:
        if tunnel_id in tunnel_infos_start.keys():
            continue
        tunnel_info = tunnel_infos[tunnel_id]
        if tunnel_info is not None:
            try:
                tunnel = ssl_tunnel.operate_sshtunnel(tunnel_info)
                if tunnel is not None:
                    tunnel.start()
                    tunnel_infos_start.update({tunnel_id: tunnel})
                    update_tree_view(tunnel_id, tunnel_info, "启动")
                    pass
            except Exception as e:
                messagebox.showinfo(title='连接异常', message=e.args[0])


def stop_all_tunnel():
    for tunnel_id in list(tunnel_infos_start.keys()):
        tunnel = tunnel_infos_start[tunnel_id]
        tunnel_info = tunnel_infos[tunnel_id]
        if tunnel is not None:
            try:
                tunnel.stop()
                tunnel_infos_start.pop(tunnel_id)
                update_tree_view(tunnel_id, tunnel_info, "未启动")
            except Exception  as e:
                messagebox.showinfo(title='连接异常', message=e.args[0])


def tk_desktop(tk_obj):
    global localhost_port, ssh_ip, ssh_port, ssh_password, \
        ssh_username, remote_ip, remote_port, tunnel_name\
        , treeview, tunnel_row_id, boolvar, password_entry, \
        showpwd

    # GUI
    tk_obj.title('SSHTunnel')
    width = 1000
    height = 500
    xscreen = tk_obj.winfo_screenwidth()
    yscreen = tk_obj.winfo_screenheight()
    xmiddle = (xscreen - width) / 2
    ymiddle = (yscreen - height) / 2
    tk_obj.geometry('%dx%d+%d+%d' % (width, height, xmiddle, ymiddle))

    # 本地的端口
    Label(tk_obj, text='本地端口', font='宋体 15 bold', bg='white').place(x=20, y=20)
    localhost_port = StringVar()
    Entry(tk_obj, textvariable=localhost_port, width=20, font='宋体 12').place(x=20, y=50)
    localhost_port.set('port')
    ##中转的服务器的 ip 端口 账号 密码
    Label(tk_obj, text='中转服务器', font='宋体 15 bold', bg='white').place(x=20, y=80)
    ##ip 端口
    ssh_ip = StringVar()
    Entry(tk_obj, textvariable=ssh_ip, width=20, font='宋体 12').place(x=20, y=110)
    ssh_ip.set('ssh ip')
    ssh_port = StringVar()
    Entry(tk_obj, textvariable=ssh_port, width=20, font='宋体 12').place(x=20, y=140)
    ssh_port.set('ssh port')
    ##账号 密码
    ssh_username = StringVar()
    Entry(tk_obj, textvariable=ssh_username, width=20, font='宋体 12').place(x=20, y=170)
    ssh_username.set('ssh username')
    ssh_password = StringVar()
    password_entry = Entry(tk_obj, textvariable=ssh_password, width=20, show='*', font='宋体 12')
    password_entry.place(x=20, y=200)
    ssh_password.set('ssh password')

    boolvar = BooleanVar()
    boolvar.set(False)
    showpwd = Checkbutton(tk_obj, text="显示密码", variable=boolvar, command=passWord)
    showpwd.place(x=200, y=200)

    ##目的地的ip端口
    Label(tk_obj, text='目标服务器', font='宋体 15 bold', bg='white').place(x=20, y=230)
    ##ip 端口
    remote_ip = StringVar()
    Entry(tk_obj, textvariable=remote_ip, width=20, font='宋体 12').place(x=20, y=260)
    remote_ip.set('remote ip')
    remote_port = StringVar()
    Entry(tk_obj, textvariable=remote_port, width=20, font='宋体 12').place(x=20, y=290)
    remote_port.set('remote port')

    Label(tk_obj, text='名称', font='宋体 15 bold', bg='white').place(x=20, y=330)
    tunnel_name = StringVar()
    Entry(tk_obj, textvariable=tunnel_name, width=20, font='宋体 12').place(x=20, y=360)
    tunnel_name.set('tunnel_name')

    Button(tk_obj, text='保存', bd=3, width=10, command=save_config, bg='#1d953f').place(x=20, y=390)
    Button(tk_obj, text='清空', bd=3, width=10, command=clear).place(x=100, y=390)

    tunnel_row_id = StringVar()
    tunnel_row_entry = Entry(tk_obj, textvariable=tunnel_row_id, width=20, font='宋体 12')
    tunnel_row_entry.pack_forget()
    frame_right = LabelFrame(tk_obj, text="服务列表", labelanchor="n")
    frame_right.place(relx=0.3, rely=0.04, relwidth=0.65, relheight=0.85)
    columns = ("名称", "本地端口", "中转信息", "目标信息", "状态")
    treeview = Treeview(frame_right, height=18, show="headings", columns=columns)
    treeview.column("名称", width=96, anchor='center')
    treeview.column("本地端口", width=96, anchor='center')
    treeview.column("中转信息", width=176, anchor='center')
    treeview.column("目标信息", width=176, anchor='center')
    treeview.column("状态", width=90, anchor='center')
    treeview.heading("名称", text="名称")
    treeview.heading("本地端口", text="本地端口")
    treeview.heading("中转信息", text="中转信息")
    treeview.heading("目标信息", text="目标信息")
    treeview.heading("状态", text="状态")
    treeview.pack(side=LEFT, fill=BOTH)
    treeview.bind("<<TreeviewSelect>>", on_click)
    fr1 = Frame(tk_obj)
    fr1.place(relx=0.45, rely=0.9)
    but1 = Button(fr1, text="启动", command=start_tunnel)
    but1.pack(side=LEFT, padx=(20, 0))
    but4 = Button(fr1, text="全部启动", command=start_all_tunnel)
    but4.pack(side=LEFT, padx=(20, 0))
    but2 = Button(fr1, text="停止", command=stop_tunnel)
    but2.pack(side=LEFT, padx=(20, 0))
    but5 = Button(fr1, text="全部停止", command=stop_all_tunnel)
    but5.pack(side=LEFT, padx=(20, 0))
    but3 = Button(fr1, text="删除", command=remove_tunnel)
    but3.pack(side=LEFT, padx=(20, 0))
    # 垂直滚动条
    scr1 = Scrollbar(frame_right)
    scr1.pack(fill=Y, side=RIGHT)
    treeview.config(yscrollcommand=scr1.set)
    scr1.config(command=treeview.yview)


def passWord():
    if boolvar.get():
        password_entry.config(show="")
    else:
        password_entry.config(show="*")


def load_config():
    load_arr = read_json()
    if load_arr is not None:
        for tunnel_info_json in load_arr:
            tunnel_info = tunnel_info_class()
            tunnel_info.localhost_port = tunnel_info_json['localhost_port']
            tunnel_info.ssh_ip = tunnel_info_json['ssh_ip']
            tunnel_info.ssh_port = tunnel_info_json['ssh_port']
            tunnel_info.ssh_username = tunnel_info_json['ssh_username']
            tunnel_info.ssh_password = cryptocode.decrypt(tunnel_info_json['ssh_password'], "F1jgEg1arVyxmUqC")
            tunnel_info.remote_ip = tunnel_info_json['remote_ip']
            tunnel_info.remote_port = tunnel_info_json['remote_port']
            tunnel_info.tunnel_name = tunnel_info_json['tunnel_name']
            tree_id = insert_tree_view(tunnel_info, "未启动")
            tunnel_infos.update({tree_id: tunnel_info})


if __name__ == '__main__':
    tk_obj = Tk()
    tk_desktop(tk_obj)
    load_config()
    tk_obj.mainloop()
