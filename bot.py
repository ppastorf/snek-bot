from game import Game
from pprint import pprint
from random import randrange


class Bot(object):

    def __init__(self, snake=None, name="robson"):
        self.name = name
        self.snake = snake

        self.dir_map = {
            0: 'left',
            1: 'right',
            2: 'up',
            3: 'down'
        }

    def take_turn(self):
        dir_index = randrange(0, len(self.dir_map.keys()), 1)
        direction = self.dir_map[dir_index]
        self.snake.next_dir = direction

        return direction

    @property
    def info(self):
        return {
            "name": self.name,
            "bind": self.snake.elem_id
        }


if __name__ == '__main__':

    bot1 = Bot()
    game = Game.bot_playable(bot1)

    bot2 = Bot()
    snake2 = game.add_snake(bot=bot2, color='red')

    bot3 = Bot()
    snake3 = game.add_snake(bot=bot3, color='yellow')

    for i in range(300):
        food = game.add_food('random_pos')

    game.play()

    pprint(game.game_state, indent=2)
    pprint(bot1.info, indent=2)
    pprint(bot2.info, indent=2)
