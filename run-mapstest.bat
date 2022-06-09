CD /d "%~dp0"

start "Server" cmd /K py -3 src/startserver.py -game "mapstest" -test
start "Client" cmd /K py -3 src/startclient.py -game "mapstest" -player "player1"
start "Client" cmd /K py -3 src/startclient.py -game "mapstest" -player "player2"
start "Client" cmd /K py -3 src/startclient.py -game "mapstest" -player "player3"