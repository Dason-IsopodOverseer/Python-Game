from engine.log import log
import mapstest.servermap
import engine.geometry as geo

class ServerMap(mapstest.servermap.ServerMap):
    # battle
    hellX = 98
    hellY = 516
    enemyHealth = 150
    enemyDmgMult = 1.7

    playerDeath = [False, False, False]
    players = {
        "Eric" : 30,
        "Andre" : 40,
        "Leslie" : 25
    }
    eAttacks = [
        ["Otaku Tendencies", 1.3, 5],
        ["Anime Obsession", 1.6, 8]
    ]

    aAttacks = [
        ["Athletic Leadership", 1.5, 5],
        ["Tackle", 1.8, 7]
    ]

    lAttacks = [
        ["DeviantArt Portfolio", 1, 3],
        ["Wattpad Fanfiction", 1.4, 7]
    ]

    enemyLines = [
        "Hmmm... your personal profile is subpar.",
        "Hmmm... your accomplishments mean nothing.",
        "Hmmm... have you considered a career in forestry?",
        "Hmmm... you are not worthy of a scholarship."
    ]