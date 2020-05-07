# -*- coding: utf-8 -*-
import weechat as wc
import requests
import re

name = 'mpv_np'

wc.register(name, 'snowfag', '1.0', 'BSD-2c', 'mpv now playing', '', '')


def config(*args, **kwargs):
  if not wc.config_is_set_plugin('mpv_host'):
    wc.config_set_plugin('mpv_host', 'localhost')
  if not wc.config_is_set_plugin('mpv_port'):
    wc.config_set_plugin('mpv_port', '8091')
  if not wc.config_is_set_plugin('color1'):
    wc.config_set_plugin('color1', '06')
  if not wc.config_is_set_plugin('color2'):
    wc.config_set_plugin('color2', '13')
  c1 = wc.config_get_plugin('color1')
  c2 = wc.config_get_plugin('color2')
  colorre = re.compile(r'^[0][1-9]|[1][0-5]$')
  if not colorre.match(c1):
    wc.prnt('', 'invalid color (valid colors are 01-15)')
    wc.config_set_plugin('color1', '06')
  if not colorre.match(c2):
    wc.prnt('', 'invalid color (valid colors are 01-15)')
    wc.config_set_plugin('color2', '13')
  return wc.WEECHAT_RC_OK


def mpv_np(*args, **kwargs):
  mpv_host = wc.config_get_plugin('mpv_host')
  mpv_port = wc.config_get_plugin('mpv_port')
  c1 = wc.config_get_plugin('color1')
  c2 = wc.config_get_plugin('color2')

  def getprops(mpv_host, mpv_port, property):
    try:
      r = requests.get('http://{}:{}/{}'.format(mpv_host, mpv_port, property), timeout=0.5)
    except:
      wc.prnt('', 'Error connecting to mpv httpd script.')
      raise
    else:
      if r.content == 'PIPE_ERROR':
        wc.prnt('', 'Pipe Error. Is mpv running?')
        raise Exception
      elif r.content == 'PROPERTY_ERROR':
        wc.prnt('', 'Property Error. idk m8 you really fucked up!')
        raise Exception
      else:
        return r.content

  try:
    title = getprops(mpv_host, mpv_port, 'filename').decode('utf-8')
    rawposition = int(float(getprops(mpv_host, mpv_port, 'playback-time')))
    rawlength = int(float(getprops(mpv_host, mpv_port, 'duration')))
    rawsize = float(getprops(mpv_host, mpv_port, 'file-size'))
  except:
    return wc.WEECHAT_RC_ERROR
  if rawposition < 3600:
    m, s = divmod(rawposition, 60)
    position = '{:d}:{:02d}'.format(m, s)
  else:
    m, s = divmod(rawposition, 60)
    h, m = divmod(m, 60)
    position = '{:d}:{:02d}:{:02d}'.format(h, m, s)
  if rawlength < 3600:
    m, s = divmod(rawlength, 60)
    length = '{:d}:{:02d}'.format(m, s)
  else:
    m, s = divmod(rawlength, 60)
    h, m = divmod(m, 60)
    length = '{:d}:{:02d}:{:02d}'.format(h, m, s)
  if int(rawsize) < 1073741824:
    size = int(rawsize) / 1048576
    formattedsize = '{} MiB'.format(int(size))
  else:
    size = float(rawsize) / float(1073741824)
    formattedsize = '{:.2f} GiB'.format(size)
  wc.command(wc.current_buffer(), u'/me {5}»» {4}mpv {5}«»{4} {0} {5}«»{4} {1}{5}/{4}{2} {5}«»{4} {3}'.format(title, position, length, formattedsize, c1, c2))
  return wc.WEECHAT_RC_OK


wc.hook_command('mpv', 'mpv now playing', '', '', '', 'mpv_np', '')
wc.hook_config('plugins.var.python.' + name + '.color1', 'config', '')
wc.hook_config('plugins.var.python.' + name + '.color2', 'config', '')
config()
