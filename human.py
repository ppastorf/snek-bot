from game import Game
from pprint import pprint


if __name__ == '__main__':
    game = Game.human_playable()
    game.play()
    pprint(game.game_state, indent=2)
