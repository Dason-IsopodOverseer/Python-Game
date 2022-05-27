CD /d "%~dp0"

start "Server" cmd /K py -3 src/startserver.py -game "dialogSequence" -test
start "Client for Player 1" cmd /K py -3 src/startclient.py -game "dialogSequence" -player "Eric"
start "Client for Player 2" cmd /K py -3 src/startclient.py -game "dialogSequence" -player "Andre"

