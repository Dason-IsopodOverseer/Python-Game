CD /d "%~dp0"

start "Server" cmd /K py -3 src/startserver.py -game "dialogSequence" -test -verbose
start "Client" cmd /K py -3 src/startclient.py -game "dialogSequence" -player "Character"

