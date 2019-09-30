import game.snake as sn
import game.bot_game as bg


class BotTrain(bg.BotGame):
    def __init__(self, bot):
        self.root = None
        self.canvas = None

        # main game objects
        self.snake = sn.Snake(self.canvas)
        self.food = sn.Food(self.canvas)

        # main game variables
        self.score = 0
        self.playtime = 0.0
        self.turns = 0

        # used to check for infinite looping snakes
        self.last_score_playtime = 0.0

        self.is_alive = True

        # reference to the bot thats playing the game
        self.bot = bot

    def tick(self):
        if not self.snake.in_valid_position:
            self.game_over()
            return

        if self.snake_has_eaten_food:
            self.score_up()
            self.last_score_playtime = self.playtime

        ''' bot integration related '''
        # bot learns current state of the game and makes a decision
        self.bot.learn_state(self.game_state)
        action = self.bot.take_action()

        # interpreting the action
        self.control_snake(action)
        self.snake.walk()

    def infinte_looping(self):
        threshold = 100000

        return (self.playtime - self.last_score_playtime >=
                threshold)

    def play(self):
        while self.is_alive:
            self.tick()
            self.playtime += 1

            # checks of the ocurrence of an infinite looping snake
            if self.infinte_looping():
                    self.game_over()

        # on game over, set bot's attributes (scores for calculating fitness)
        self.bot.score = self.score
        self.bot.playtime = self.playtime
        self.bot.turns = self.turns
