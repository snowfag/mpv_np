#!/usr/bin/env python2.7
import socket
import json
import yaml
import os

config_location = os.path.expanduser("~") + '/.mpv_httpd'
if not os.path.isfile(config_location):
    print('Could\'t find config file at ~/.mpv_httpd writing defaults to it now.')
    conf = {'mpvsock': '/tmp/mpvsocket', 'serverip': '127.0.0.1', 'serverport': 8091}
    try:
        with open(config_location, 'w') as configfile:
            yaml.dump(conf, configfile, default_flow_style=False)
    except:
        print('Couldn\'t write config file proceeding with defaults.')
else:
    try:
        with open(config_location, 'r') as configfile:
            conf = yaml.load(configfile)
    except:
        print('Garbage input from config file at ~/.mpv_httpd proceeding with defaults.')
        conf = {'mpvsock': '/tmp/mpvsocket', 'serverip': '127.0.0.1', 'serverport': 8091}


def getprop(property):
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        sock.connect(conf['mpvsock'])
    except:
        print('Error connecting to mpv socket')
        return 'PIPE_ERROR'
    else:
        try:
            sock.sendall('{"command":["get_property","' + property + '"]}\n')
            j = json.loads(sock.recv(1024))
            sock.close()
        except:
            print('Error getting property from mpv socket.')
            return 'PIPE_ERROR'
        else:
            try:
                if j['error'] == 'success':
                    return j['data']
                else:
                    return 'PROPERTY_ERROR'
            except:
                print('Invalid json returned from mpv')
                return None

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.bind((conf['serverip'], conf['serverport']))
server_sock.listen(10)

while True:
    cli_sock, addr = server_sock.accept()
    print('We have opened a cli_sockection with', addr)
    req = cli_sock.recv(1024)
    try:
        prop = req.split(' ')[1][1:]
    except:
        cli_sock.close()
    else:
        cli_sock.send("HTTP/1.1 200 OK\n")
        cli_sock.send("Content-Type: text/html; encoding=utf8\n")
        cli_sock.send('\n')

        ret = getprop(prop)
        if ret is not None:
            cli_sock.send(ret.encode('utf-8'))

        cli_sock.close()
