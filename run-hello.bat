CD /d "%~dp0"

start "Server" cmd /K py -3 src/startserver.py -game "helloworld" -test
start "Client" cmd /K py -3 src/startclient.py -game "helloworld" -player "Belston"

