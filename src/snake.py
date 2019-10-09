from random import randrange

DEFAULT_SIZE = 10
DEFAULT_COLOR = "#aaaaaa"

SNAKE_SIZE = DEFAULT_SIZE
FOOD_SIZE = DEFAULT_SIZE

FOOD_COLOR = "#006600"
HEAD_COLOR = "#804d00"
BODY_COLOR = "#e68a00"


class Element(object):
    def __init__(
            self,
            game,
            pos_x, pos_y,
            color=DEFAULT_COLOR,
            size=DEFAULT_SIZE):

        self.pos_x = pos_x
        self.pos_y = pos_y
        self.color = color
        self.size = size
        self.game = game

    def update(self):
        pass

    def show(self):
        self.game.canvas.create_rectangle(
            self.pos_x,
            self.pos_y,
            self.pos_x + self.size,
            self.pos_y + self.size,
            fill=self.color
        )

    @property
    def pos(self):
        return self.pos_x, self.pos_y

    @property
    def state(self):
        return {
            "pos": self.pos,
        }


class Food(Element):
    def __init__(
            self,
            game,
            size=FOOD_SIZE, color=FOOD_COLOR):
        super().__init__(
            game,
            randrange(game.playable_x[0], game.playable_x[1], size),
            randrange(game.playable_y[0], game.playable_y[1], size),
            color=color
        )


class SnakeTail(Element):

    def __init__(
            self,
            master,
            last_part,
            size=SNAKE_SIZE,
            color=BODY_COLOR):

        super().__init__(
            master.game,
            last_part.last_pos_x,
            last_part.last_pos_y,
            color=color
        )

        self.last_part = last_part
        self.last_pos_x = self.pos_x
        self.last_pos_y = self.pos_y

    def _update_last_position(self):
        self.last_pos_x = self.pos_x
        self.last_pos_y = self.pos_y

    def _update_position(self):
        self.pos_x = self.last_part.last_pos_x
        self.pos_y = self.last_part.last_pos_y

    def walk(self):
        self._update_last_position()
        self._update_position()


class SnakeHead(Element):

    def __init__(
            self,
            master,
            start_x,
            start_y,
            size=SNAKE_SIZE,
            color=HEAD_COLOR):

        super().__init__(
            master.game,
            start_x,
            start_y,
            color=color
        )

        self.last_pos_x = start_x + self.size
        self.last_pos_y = start_y

    def walk(self, direction):
        self.last_pos_x = self.pos_x
        self.last_pos_y = self.pos_y

        if direction == 'left':
            self.pos_x -= self.size

        if direction == 'right':
            self.pos_x += self.size

        if direction == 'up':
            self.pos_y -= self.size

        if direction == 'down':
            self.pos_y += self.size


class Snake(object):
    def __init__(
            self,
            game,
            start_x,
            start_y,
            start_dir='left',
            lenght=1, size=SNAKE_SIZE):

        self.game = game
        self.direction = start_dir
        self.head = SnakeHead(self, start_x, start_y)
        self.tail = []
        self.turns = 0
        self.time_alive = 0.0
        self.is_alive = True
        self.bind = None

        for i in range(lenght):
            self.tail.append(
                SnakeTail(self, self.head)
            )

    def update(self):
        self.time_alive += self.game.tick_delay
        self.walk()

    def show_body(self):
        for i in range(0, self.body_size):
            self.tail[i].show()

    def show(self):
        self.head.show()
        self.show_body()

    def walk(self):
        self.head.walk(self.direction)

        for i in range(0, self.body_size):
            self.tail[i].walk()

    def turn(self, new_dir):
        if not self.in_valid_position:
            return

        self.turns += 1

        if new_dir == 'left':
            if self.direction != 'right':
                self.direction = 'left'

        if new_dir == 'right':
            if self.direction != 'left':
                self.direction = 'right'

        if new_dir == 'up':
            if self.direction != 'down':
                self.direction = 'up'

        if new_dir == 'down':
            if self.direction != 'up':
                self.direction = 'down'

    def eat(self):
        self.tail.append(
            SnakeTail(self, self.tail[self.body_size - 1])
        )

    def die(self):
        self.is_alive = False

    @property
    def in_valid_position(self):
        min_x = self.game.playable_x[0]
        max_x = self.game.playable_x[1]
        min_y = self.game.playable_y[0]
        max_y = self.game.playable_y[1]

        out_of_bounds = (
            (self.pos_x >= max_x or self.pos_x < min_x) or
            (self.pos_y >= max_y or self.pos_y < min_y)
        )

        eaten_itself = any([parts.pos == self.pos for parts in self.tail])

        dead = out_of_bounds or eaten_itself
        return not dead

    @property
    def body_size(self):
        return len(self.tail)

    @property
    def pos_y(self):
        return self.head.pos_y

    @property
    def pos_x(self):
        return self.head.pos_x

    @property
    def pos(self):
        return self.head.pos

    @property
    def state(self):
        return {
            "bind": self.bind,
            "pos": self.pos,
            "body_size": self.body_size,
            "direction": self.direction,
            "turns": self.turns,
            "time_alive": self.time_alive
        }

    def bind_to_keys(self):
        if self.bind is not None:
            return

        self.game.root.bind('<Left>', self.game.keyboard_event)
        self.game.root.bind('<Right>', self.game.keyboard_event)
        self.game.root.bind('<Up>', self.game.keyboard_event)
        self.game.root.bind('<Down>', self.game.keyboard_event)
        self.bind = "player"

    def bind_to_bot(self, bot):
        if self.bind is not None:
            return

        self.bind = bot.name
        # TODO
