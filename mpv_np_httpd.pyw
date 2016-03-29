# -*- coding: utf-8 -*-
import win32pipe
import socket
import json

## Make sure to add "input-ipc-server=\\.\pipe\mpvsocket" to your mpv config.
## To use weechat on a remote server use an ssh (reverse) tunnel

MPVSOCK = '\\\\.\pipe\mpvsocket'

def getprop(property):
    try:
        data = win32pipe.CallNamedPipe(MPVSOCK,'{"command":["get_property","'+property+'"]}\n',1024,0)
    except:
        print "Error getting property from named pipe."
        return "PIPE_ERROR"
    else:
        try:
            j = json.loads(data)
            if j["error"] == "success":
                return j["data"]
            else:
                return "PROPERTY_ERROR"
        except:
            print "Invalid json returned from mpv"
            return None


server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.bind(('127.0.0.1', 8091))
server_sock.listen(10)

while True:
    titles = []
    cli_sock, addr = server_sock.accept()
    print 'We have opened a cli_sockection with', addr
    req = cli_sock.recv(1024)
    prop = req.split(' ')[1][1:]

    cli_sock.send("HTTP/1.1 200 OK\n")
    cli_sock.send("Content-Type: text/html; encoding=utf8\n")
    cli_sock.send('\n')

    ret = getprop(prop)
    if ret is not None:
        formattedret = u'%s' % (ret)
        cli_sock.send(formattedret.encode('utf-8'))

    cli_sock.close()