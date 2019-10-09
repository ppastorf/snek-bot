from game import Game
import pprint


def random_dna():
    return "a"


class Bot(object):

    def __init__(self, dna=random_dna(), name="robson"):
        self.dna = dna
        self.name = name
        self.snake = None


if __name__ == '__main__':
    bot = Bot()
    game = Game.bot_playable(bot)
    game.play()

    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(game.game_state)
