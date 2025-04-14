#!/bin/env python3

from . import elements as elm
import pandas as pd
import torch
import torch.nn as nn
from random import randint


class BotAI(object):
    def __init__(self, game, parameters):
        self.game = game
        self.parameters = parameters

    def choose_action(self, vision: elm.BotVision) -> elm.BotDecision:
        ## random action
        return elm.BotDecision(randint(0, elm.BotDecision.n_actions()-1))

        ## action based on model
        # pass

