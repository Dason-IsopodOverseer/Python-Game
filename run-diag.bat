CD /d "%~dp0"

start "Server" cmd /K py -3 src/startserver.py -game "dialogSequence" -test
start "Client" cmd /K py -3 src/startclient.py -game "dialogSequence" -player "Character"
start "Client" cmd /K py -3 src/startclient.py -game "dialogSequence" -player "Character2"

