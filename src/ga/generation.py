import numpy as np
import uuid
import random
from typing import Self, TypedDict

from ..game import game 


####################
# Generation
####################
class Generation(object):
    id: str
    name: str
    n_bots: int
    bots: dict[str, game.Bot]

    def __init__(self, name: str, bots: dict[str, game.Bot]):
        self.id = uuid.uuid4()
        self.name = name
        self.n_bots = len(bots.items())
        self.bots = bots

    def top_n_fit(self, n: int):
        pass
    
    def bottom_n_fit(self, n: int)
        pass

    def bot_by_id(self, id: str):
        return self.bots.get(id, None)
    