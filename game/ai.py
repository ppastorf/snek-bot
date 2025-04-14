#!/bin/env python3

from elements import SnakeVision, SnakeDecision
import pandas as pd
import torch
import torch.nn as nn


class SnakeAI(object):

    def __init__(self, parameters):
        self.parameters = parameters
        self.model = DecisionModel(
            input_size=
            hidden_size=parameters[0]
            output_size=SnakeDecision.n_actions()
    )
    
    def choose_action(snakeVision: SnakeVision): SnakeDecision

    def get_genome(model):
        return torch.cat([p.data.view(-1) for p in model.parameters()])

    def set_genome(model, genome):
        with torch.no_grad():
            i = 0
            for p in model.parameters():
                shape = p.data.shape
                n_params = p.data.numel()
                p.data.copy_(genome[i:i+n_params].view(shape))
                i += n_params
        

class DecisionModel(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.Tanh(),
            nn.Linear(hidden_size, output_size)
        )

    def forward(self, x):
        return self.net(x)
