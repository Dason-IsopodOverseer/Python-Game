from engine.log import log
import mapstest.servermap
import engine.geometry as geo

class ServerMap(mapstest.servermap.ServerMap):
    # battle
    hellX = 98
    hellY = 516
    enemyHealth = 3
    enemyDmgMult = 1.5

    playerDeath = [False, False, False]
    players = {
        "Eric" : 3,
        "Andre" : 4,
        "Leslie" : 2
    }
    eAttacks = [
        ["Otaku Tendencies", 1, 3],
        ["Anime Obsession", 1.5, 8]
    ]

    aAttacks = [
        ["Athletic Leadership", 1.2, 3],
        ["Tackle", 1.4, 5]
    ]

    lAttacks = [
        ["DeviantArt Portfolio", 0.8, 3],
        ["Wattpad Fanfiction", 1.2, 7]
    ]