# mpv_np
mpv now playing script for Weechat (remote or local)

This script uses the mpv json ipc via named pipes on Windows and unix sockets on Macos/Linux/BSD so make sure to add "input-ipc-server=\\.\pipe\mpvsocket" for Windows or "input-ipc-server=/tmp/mpvsocket" for MacOS/Linux/BSD to your mpv config.
To use weechat on a remote server use an ssh (reverse) tunnel.

Use "mpv_np_httpd.pyw/mpv_np_httpd.exe" on Windows, "mpv_np_httpd_unix.py/mpv_np_httpd.app" on MacOS, "mpv_np_httpd_unix.py/mpv_np_httpd_unix(binary)" on Linux/BSD
