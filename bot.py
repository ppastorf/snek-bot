from game import Game
from pprint import pprint


def random_dna():
    return "a"


class Bot(object):

    def __init__(self, dna=random_dna(), name="robson"):
        self.dna = dna
        self.name = name
        self.snake = None

    @property
    def info(self):
        return {
            "name": self.name,
            "dna": self.dna
        }


if __name__ == '__main__':
    bot = Bot()
    game = Game.bot_playable(bot)
    game.play()

    pprint(game.game_state, indent=2)
    pprint(bot.info, indent=2)
