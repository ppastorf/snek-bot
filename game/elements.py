import pandas as pd
from random import randint

ELEMENT_SIZE = 10
DEFAULT_COLOR = "#aaaaaa"

FOOD_COLOR = "#006600"
WALL_COLOR = "0000000"


class Element(object):
    def __init__(
            self,
            game,
            pos_x, pos_y,
            elem_type="element",
            elem_id="none",
            color=DEFAULT_COLOR):

        self.pos_x = pos_x
        self.pos_y = pos_y
        self.color = color
        self.size = ELEMENT_SIZE
        self.game = game
        self.elem_type = elem_type
        self.elem_id = self.game.new_elem_id()

        self.game.elements.update({
            self.elem_id: self
        })

        self.set_map_pos()

    def on_snake_hit(self, snake):
        pass

    def set_map_pos(self):
        self.game.map.set_position(self.pos_x, self.pos_y, self.elem_id)

    def clear_map_pos(self, pos=None):
        if pos is None:
            pos_x, pos_y = self.pos
        else:
            pos_x, pos_y = pos

        self.game.map.set_position(pos_x, pos_y, 0)

    def expire(self, pos=None):
        if pos is None:
            pos = self.pos

        self.clear_map_pos(pos=pos)
        self.game.elements.pop(self.elem_id, None)

    @property
    def pos(self):
        return self.pos_x, self.pos_y

    @property
    def state(self):
        values = {
            'id': self.elem_id,
            'type': self.elem_type,
            'x': self.pos_x,
            'y': self.pos_y
        }

        state = pd.Series(data=values)

        return state


class Food(Element):
    def __init__(
            self,
            game,
            pos_x, pos_y,
            color=FOOD_COLOR,
            replace=True):

        super().__init__(
            game,
            pos_x, pos_y,
            elem_type="food",
            color=color
        )
        self.replace = replace

    def on_snake_hit(self, snake):
        snake.eat(self)
        if self.replace:
            self.game.add_food('random_pos')


class Wall(Element):
    def __init__(
            self,
            game,
            pos_x,
            pos_y):

        super().__init__(
            game,
            pos_x, pos_y,
            elem_type="wall",
            color=WALL_COLOR
        )

    def on_snake_hit(self, snake):
        snake.die()


class SnakeTail(Element):

    def __init__(
            self,
            master,
            last_part):

        super().__init__(
            master.game,
            last_part.last_pos_x,
            last_part.last_pos_y,
            color=master.color,
            elem_type="tail"
        )

        self.master = master
        self.last_part = last_part
        self.last_pos_x = self.pos_x
        self.last_pos_y = self.pos_y

    def walk(self):
        self.last_pos_x = self.pos_x
        self.last_pos_y = self.pos_y

        self.pos_x = self.last_part.last_pos_x
        self.pos_y = self.last_part.last_pos_y

    def on_snake_hit(self, snake):
        if self.game.collision and self.master.elem_id != snake.elem_id:
            if self.master.tail_length > snake.tail_length:
                snake.die()
            elif self.master.tail_length < snake.tail_length:
                self.master.die()
            else:
                rip = randint(0, 1)
                if rip:
                    self.master.die()
                else:
                    snake.die()

        if (self.game.self_collision and
                self.master.elem_id == snake.elem_id):
            snake.die()

    @property
    def last_pos(self):
        return (self.last_pos_x, self.last_pos_y)


class SnakeHead(Element):

    def __init__(
            self,
            master,
            start_x,
            start_y):

        super().__init__(
            master.game,
            start_x,
            start_y,
            color=master.color,
            elem_type="head"
        )

        self.master = master
        self.last_pos_x = start_x
        self.last_pos_y = start_y

    def walk(self, direction):
        self.last_pos_x = self.pos_x
        self.last_pos_y = self.pos_y

        if direction == 'left':
            self.pos_x -= 1

        if direction == 'right':
            self.pos_x += 1

        if direction == 'up':
            self.pos_y -= 1

        if direction == 'down':
            self.pos_y += 1

    def on_snake_hit(self, snake):
        if self.game.collision and self.master.elem_id != snake.elem_id:
            if self.master.tail_length > snake.tail_length:
                snake.die()
            elif self.master.tail_length < snake.tail_length:
                self.master.die()
            else:
                rip = randint(0, 1)
                if rip:
                    self.master.die()
                else:
                    snake.die()

        if (self.game.self_collision and
                self.master.elem_id == snake.elem_id):
            snake.die()

    @property
    def last_pos(self):
        return (self.last_pos_x, self.last_pos_y)


class Snake(object):
    def __init__(
            self,
            game,
            start_x,
            start_y,
            start_dir='left',
            start_length=1,
            color=None):

        self.game = game

        self.color = color
        self.head_color = color
        self.tail_color = color

        self.direction = start_dir
        self.next_dir = start_dir

        self.head = SnakeHead(self, start_x, start_y)
        self.tail = []
        self.turns = 0
        self.time_alive = 0.0
        self.is_alive = True
        self.bind = None

        self.elem_type = "snake"
        self.elem_id = self.game.new_elem_id()

        last_part = self.head
        for i in range(start_length):
            last_part = SnakeTail(self, last_part)
            self.tail.append(last_part)

    def walk(self):
        self.head.walk(self.direction)
        for i in range(self.tail_length):
            self.tail[i].walk()

    def take_turn(self):
        return self.next_dir

    def turn(self):
        new_dir = self.take_turn()

        opposite = {
            "left": "right",
            "up": "down",
            "right": "left",
            "down": "up"
        }

        if not self.in_valid_position:
            return

        if new_dir == self.direction:
            return

        if opposite[new_dir] == self.direction:
            new_dir = self.direction
            return

        self.turns += 1
        self.direction = new_dir

    def eat(self, food):
        food.expire()
        self.tail.append(
            SnakeTail(
                self,
                self.tail[self.tail_length - 1]
            )
        )

    def in_valid_position(self, map):
        min_x, max_x = self.game.x_range
        min_y, max_y = self.game.y_range

        pos_x, pos_y = self.pos

        out_of_bounds = (
            (pos_x >= max_x or pos_x < min_x) or
            (pos_y >= max_y or pos_y < min_y)
        )

        return not out_of_bounds

    def die(self):
        self.is_alive = False

        self.head.clear_map_pos()
        self.head.expire(pos=self.head.last_pos)
        for t in self.tail:
            t.expire(pos=t.last_pos)

    def update(self):
        self.time_alive += self.game.tick_delay
        self.turn()
        self.walk()

        if not self.in_valid_position(map):
            self.die()
            return

        element = self.game.element_at(*self.pos)
        if element is not None:
            element.on_snake_hit(self)

        self.head.clear_map_pos(pos=self.head.last_pos)
        if self.is_alive:
            self.head.set_map_pos()

        for part in self.tail:
            part.clear_map_pos(pos=part.last_pos)
            if self.is_alive:
                part.set_map_pos()

    @property
    def tail_length(self):
        return len(self.tail)

    @property
    def length(self):
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
        values = {
            'id': self.elem_id,
            'type': self.elem_type,
            'x': self.pos_x,
            'y': self.pos_y,
            'dir': self.direction,
            'length': self.length,
            'alive': self.is_alive,
            'bind': self.bind.name
        }

        state = pd.Series(data=values)

        return state

    def keyboard_direction(self, event):
        direction = event.keysym.lower()
        self.next_dir = direction
