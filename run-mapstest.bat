CD /d "%~dp0"

start "Server" cmd /K py -3 src/startserver.py -game "mapstest" -test
start "Client" cmd /K py -3 src/startclient.py -game "mapstest" -player "Goose"