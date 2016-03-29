# mpv_np
mpv (Windows) now playing script for Weechat (remote or local)

This script uses the mpv json ipc via named pipes on Windows so make sure to add "input-ipc-server=\\.\pipe\mpvsocket" to your mpv config.
To use weechat on a remote server use an ssh (reverse) tunnel.
