CD /d "%~dp0"

start "Server" cmd /K py -3 src/startserver.py -game "battletest" -test
start "Client" cmd /K py -3 src/startclient.py -game "battletest" -player "one"
start "Client" cmd /K py -3 src/startclient.py -game "battletest" -player "two"
start "Client" cmd /K py -3 src/startclient.py -game "battletest" -player "three"