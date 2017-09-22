# Import libraries
import socket
import subprocess

# Config vars
server_ip = '192.168.1.235'
server_port = 8000

# Player config: 
#  - VLC: ['vlc', '--demux', 'h264', '-']
#  - Mplayer: ['mplayer', '-fps', '60', '-cache', '1024', '-']
player_config = ['mplayer', '-fps', '60', '-cache', '1024', '-']

# Start a socket listening for connections on 0.0.0.0:8000
# (0.0.0.0 means all interfaces)
server_socket = socket.socket()
server_socket.bind(('0.0.0.0', server_port ))
server_socket.listen(0)

# Accept a single connection and make a file-like object out of it
connection = server_socket.accept()[0].makefile('rb')
try:
    # Run a viewer with an appropriate command line (player_config) 
    player = subprocess.Popen( player_config, stdin=subprocess.PIPE)

    while True:
        # Repeatedly read 1k of data from the connection
        # and write it to the media player's stdin
        data = connection.read(1024)
        if not data:
            break

        player.stdin.write(data)

finally:
    connection.close()
    server_socket.close()
    player.terminate()
