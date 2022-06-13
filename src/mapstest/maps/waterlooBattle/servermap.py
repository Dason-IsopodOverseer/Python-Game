from engine.log import log
import mapstest.servermap
import engine.geometry as geo

class ServerMap(mapstest.servermap.ServerMap):
    # battle
    hellX = 534
    hellY = 114
    enemyHealth = 350
    enemyDmgMult = 1.9

    playerDeath = [False, False, False]
    players = {
        "Eric" : 25,
        "Andre" : 45,
        "Leslie" : 30
    }
    eAttacks = [
        ["Waterloo Simp", 0.8, 7],
        ["Main Method", 1, 10]
    ]

    aAttacks = [
        ["Big Flex", 1.7, 6],
        ["Creatine", 2, 8]
    ]

    lAttacks = [
        ["Colour Theory", 1.2, 4],
        ["Purple Prose", 1.6, 7]
    ]

    enemyLines = [
        "Get deferred to Geomatics, b*tch.",
        "Taste the wrath of a thousand angry geese.",
        "......You don't have a 101 average. REJECTED.",
        "The only co-op you're getting is a job at McDonalds." #fire
    ]