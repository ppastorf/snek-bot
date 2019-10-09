from game import Game
import pprint


if __name__ == '__main__':
    game = Game.human_playable()
    game.play()
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(game.game_state)
