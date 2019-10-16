from random import randrange

DEFAULT_SIZE = 10
DEFAULT_COLOR = "#aaaaaa"

SNAKE_SIZE = DEFAULT_SIZE
FOOD_SIZE = DEFAULT_SIZE

FOOD_COLOR = "#006600"
HEAD_COLOR = "#804d00"
TAIL_COLOR = "#e68a00"


class Element(object):
    def __init__(
            self,
            game,
            pos_x, pos_y,
            elem_type="element",
            size=DEFAULT_SIZE,
            color=DEFAULT_COLOR):

        self.pos_x = pos_x
        self.pos_y = pos_y
        self.color = color
        self.size = size
        self.game = game
        self.elem_type = elem_type

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
            "type": self.elem_type,
            "id": self.elem_id,
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
            elem_type="food",
            size=size,
            color=color
        )
        self.elem_id = self.game.new_elem_id()


class SnakeTail(Element):

    def __init__(
            self,
            master,
            last_part,
            elem_type="tail",
            size=SNAKE_SIZE,
            color=TAIL_COLOR):

        super().__init__(
            master.game,
            last_part.last_pos_x,
            last_part.last_pos_y,
            size=size,
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
            elem_type="head",
            size=SNAKE_SIZE,
            color=HEAD_COLOR):

        super().__init__(
            master.game,
            start_x,
            start_y,
            size=size,
            color=color,
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
            lenght=1,
            size=SNAKE_SIZE):

        self.game = game

        self.direction = start_dir
        self.next_dir = start_dir

        self.head = SnakeHead(self, start_x, start_y)
        self.tail = []
        self.turns = 0
        self.time_alive = 0.0
        self.is_alive = True
        self.bind = None

        self.size = size

        self.elem_type = "snake"
        self.elem_id = self.game.new_elem_id()

        for i in range(lenght):
            self.tail.append(
                SnakeTail(self, self.head)
            )

    def show_tail(self):
        for i in range(self.tail_length):
            self.tail[i].show()

    def show(self):
        if self.is_alive:
            self.head.show()
            self.show_tail()

    def walk(self):
        self.head.walk(self.direction)

        for i in range(self.tail_length):
            self.tail[i].walk()

    def turn(self):
        opposite = {
            "left": "right",
            "up": "down",
            "right": "left",
            "down": "up"
        }

        if not self.in_valid_position:
            return

        if self.next_dir == self.direction:
            return

        if opposite[self.next_dir] == self.direction:
            self.next_dir = self.direction
            return

        self.turns += 1
        self.direction = self.next_dir

    def eat(self, food):
        self.game.remove_food(food)
        self.game.add_food()
        self.game.score += 1

        self.tail.append(
            SnakeTail(
                self,
                self.tail[self.tail_length - 1]
            )
        )

    def die(self):
        self.is_alive = False

    def update(self):
        if self.is_alive:
            self.time_alive += self.game.tick_delay
            self.walk()

            if not self.in_valid_position:
                self.die()

            for food in self.game.foods.values():
                if food.pos == self.pos:
                    self.eat(food)

            self.turn()

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
    def tail_length(self):
        return len(self.tail)

    @property
    def lenght(self):
        return self.tail_length + 1

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
            "type": self.elem_type,
            "id": self.elem_id,
            "bind": self.bind,
            "pos": self.pos,
            "lenght": self.lenght,
            "direction": self.direction,
            "turns": self.turns,
            "time_alive": self.time_alive,
            "is_alive": self.is_alive
        }

    def keyboard_direction(self, event):
        direction = event.keysym.lower()
        self.next_dir = direction

    def bind_to_keys(self):
        if self.bind is not None:
            return

        self.game.root.bind('<Left>', self.keyboard_direction)
        self.game.root.bind('<Right>', self.keyboard_direction)
        self.game.root.bind('<Up>', self.keyboard_direction)
        self.game.root.bind('<Down>', self.keyboard_direction)
        self.bind = "player"

    def bind_to_bot(self, bot):
        if self.bind is not None:
            return

        bot.snake = self
        self.bind = bot.name
