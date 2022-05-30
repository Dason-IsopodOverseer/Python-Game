CD /d "%~dp0"

<<<<<<< HEAD
start "Server" cmd /K py -3 src/startserver.py -game "dialogSequence" -test -verbose
start "Client" cmd /K py -3 src/startclient.py -game "dialogSequence" -player "Character"
=======
start "Server" cmd /K py -3 src/startserver.py -game "dialogSequence" -test
start "Client for Player 1" cmd /K py -3 src/startclient.py -game "dialogSequence" -player "Eric"
start "Client for Player 2" cmd /K py -3 src/startclient.py -game "dialogSequence" -player "Andre"
>>>>>>> 0615b38d980a7a640dd28af3e91eb290685450c5

