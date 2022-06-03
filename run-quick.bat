CD /d "%~dp0"

start "Server" cmd /K py -3 src/startserver.py -game "quick" -test
start "Client" cmd /K py -3 src/startclient.py -game "quick" -player "player1"
start "Client" cmd /K py -3 src/startclient.py -game "quick" -player "player2"
start "Client" cmd /K py -3 src/startclient.py -game "quick" -player "player3"