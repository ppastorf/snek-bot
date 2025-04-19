#!/bin/env python3

from . import elements as elm
import pandas as pd
import torch
import torch.nn as nn
import numpy as np

import gymnasium as gym
import math
import random
import matplotlib
import matplotlib.pyplot as plt
from collections import namedtuple, deque
from itertools import count

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

Transition = namedtuple('Transition',
    ('state', 'action', 'next_state', 'reward')
)


def _get_empty_tensor(device, length):
    return torch.tensor(pd.DataFrame(np.zeros((length))).values.flatten(), dtype=torch.float32, device=device).unsqueeze(0)


class ReplayMemory(object):
    def __init__(self, capacity):
        self.memory = deque([], maxlen=capacity)

    def push(self, *args):
        """Save a transition"""
        self.memory.append(Transition(*args))

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)


class DQN(nn.Module):
    def __init__(self, n_observations, n_actions, n_hiden_layers, hidden_layer_len):
        super(DQN, self).__init__()
        self.input_layer = nn.Linear(n_observations, hidden_layer_len)

        self.hidden_layers = []
        for i in range(n_hiden_layers):
            self.hidden_layers.append(nn.Linear(hidden_layer_len, hidden_layer_len))

        self.output_layer = nn.Linear(hidden_layer_len, n_actions)

    # Called with either one element to determine next action, or a batch
    # during optimization. Returns tensor([[left0exp,right0exp]...]).
    def forward(self, x):
        x = F.relu(self.input_layer(x))
        for layer in self.hidden_layers:
            x = F.relu(layer(x))
        return self.output_layer(x)


class BotAI(object):
    def __init__(self, bot, parameters: list, activations_length: int):
        self.bot = bot

        ## parameters
        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else
            "mps" if torch.backends.mps.is_available() else
            "cpu"
        )
        self.gamma = 0.99
        self.eps_start = 0.9
        self.eps_end = 0.05
        self.eps_decay = 1000
        self.tau = 0.005
        self.batch_size = 128
        self.lr = 1e-4
        self.n_hidden_layers = 2
        self.hidden_layer_len = 128
        self.food_reward = 10
        self.playtime_reward = 1
        self.death_penalty = 10

        self.replay_memory_size = 10000

        self.n_inputs = activations_length
        self.n_actions = elm.BotDecision.n_actions()

        self._last_state  = _get_empty_tensor(self.device, self.n_inputs)
        self._last_action = _get_empty_tensor(self.device, 1)
        self._last_score = 0
        self._score = 0

        self.memory = ReplayMemory(self.replay_memory_size)

        self.policy_net = DQN(
            self.n_inputs, 
            self.n_actions,
            self.n_hidden_layers,
            self.hidden_layer_len
        ).to(self.device)

        self.target_net = DQN(
            self.n_inputs, 
            self.n_actions,
            self.n_hidden_layers,
            self.hidden_layer_len
        ).to(self.device)

        self.target_net.load_state_dict(self.policy_net.state_dict())
        self.optimizer = optim.AdamW(self.policy_net.parameters(), lr=self.lr, amsgrad=True)
        self.steps_done = 0
        self.episode_durations = []

    def _random_action(self) -> elm.BotDecision:
        return elm.BotDecision(random.randint(0, elm.BotDecision.n_actions()-1))

    def _model_choose_action(self, state: torch.Tensor):
        sample = random.random()
        eps_threshold = self.eps_end + (self.eps_start - self.eps_end) * \
            math.exp(-1. * self.steps_done / self.eps_decay)
        self.steps_done += 1
        if sample > eps_threshold:
            with torch.no_grad():
                return self.policy_net(state).max(1).indices.view(1, 1)
        else:
            return torch.tensor([[random.randrange(0, self.n_actions)]], device=self.device, dtype=torch.long)

    def _optimize_model(self):
        if len(self.memory) < self.batch_size:
            return

        transitions = self.memory.sample(self.batch_size)
        batch = Transition(*zip(*transitions))

        non_final_mask = torch.tensor(
            tuple(map(lambda s: s is not None, batch.next_state)),
            device=self.device, dtype=torch.bool
        )
        non_final_next_states = torch.cat([s for s in batch.next_state if s is not None])
        state_batch = torch.cat(batch.state)
        action_batch = torch.cat(batch.action)
        reward_batch = torch.cat(batch.reward)

        state_action_values = self.policy_net(state_batch).gather(1, action_batch)

        next_state_values = torch.zeros(self.batch_size, device=self.device)
        with torch.no_grad():
            next_state_values[non_final_mask] = self.target_net(non_final_next_states).max(1)[0]

        expected_state_action_values = (next_state_values * self.gamma) + reward_batch
        loss = F.smooth_l1_loss(state_action_values, expected_state_action_values.unsqueeze(1))

        self.optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_value_(self.policy_net.parameters(), 100)
        self.optimizer.step()

        # Soft update target net
        target_dict = self.target_net.state_dict()
        policy_dict = self.policy_net.state_dict()
        for key in policy_dict:
            target_dict[key] = policy_dict[key] * self


    def choose_action(self, vision: elm.BotVision) -> elm.BotDecision:
        activations = vision.as_dataframe().values.flatten()
        if not len(activations):
            return elm.BotDecision(0)

        assert len(activations) == self.n_inputs, "Mismatch between activations size and model expected size"

        # Save state for later use
        state = torch.tensor(activations, dtype=torch.float32, device=self.device).unsqueeze(0)
        self._last_state = state
        self._last_score = self.bot.snake.score

        action_tensor = self._model_choose_action(state)
        self._last_action = action_tensor  # Save for training step

        return elm.BotDecision(action_tensor.item())

    @property
    def _reward(self):
        if self.bot.snake.is_alive:
            return (
                ((self._score - self._last_score) * self.food_reward) + self.playtime_reward
            )
        else:
            return - self.death_penalty * self._score

    def record_transition_and_train(self, vision: elm.BotVision):
        activations = vision.as_dataframe().values.flatten()
        if not len(activations):
            next_state = None
        else:
            next_state = torch.tensor(activations, dtype=torch.float32, device=self.device).unsqueeze(0)

        self._score = self.bot.snake.score
        reward_tensor = torch.tensor([self._reward], device=self.device)
        self.memory.push(self._last_state, self._last_action, next_state, reward_tensor)
        
        try:
            self._optimize_model()
        except KeyboardInterrupt:
            raise
        except:
            pass
