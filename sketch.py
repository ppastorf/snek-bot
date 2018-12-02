#!/usr/bin/python3

from bot import Bot
from bot_show import BotShow
from tweak.ga_tweak import *
from tweak.game_tweak import *
from random import randint, uniform

dna = [uniform(GENE1[0], GENE1[1]),
       uniform(GENE2[0], GENE2[1]),
       uniform(GENE3[0], GENE3[1]),
       uniform(GENE4[0], GENE4[1]),
       uniform(GENE5[0], GENE5[1])]

# bot object
bot = Bot(dna)

# bot-playable game
playable = BotShow(bot)

playable.play()