BLOCK_SIZE = 10
DEFAULT_COLOR = "#aaaaaa"

SNAKE_SIZE = BLOCK_SIZE
FOOD_SIZE = BLOCK_SIZE
WALL_SIZE = BLOCK_SIZE

FOOD_COLOR = "#006600"
HEAD_COLOR = "#804d00"
TAIL_COLOR = "#e68a00"
WALL_COLOR = "0000000"


class Element(object):
    def __init__(
            self,
            game,
            pos_x, pos_y,
            elem_type="element",
            size=BLOCK_SIZE,
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
        self.game.show_element(self)

    def on_snake_hit(self, snake):
        pass

    @property
    def pos(self):
        return self.pos_x, self.pos_y

    @property
    def state(self):
        return {
            self.elem_type: {
                "id": self.elem_id,
                "pos": self.pos,
            }
        }


class Food(Element):
    def __init__(
            self,
            game,
            pos_x, pos_y,
            size=FOOD_SIZE,
            color=FOOD_COLOR):

        super().__init__(
            game,
            pos_x, pos_y,
            elem_type="food",
            size=size,
            color=color
        )
        self.elem_id = self.game.new_elem_id()

    def on_snake_hit(self, snake):
        snake.eat(self)


class Wall(Element):
    def __init__(
            self,
            game,
            pos_x, pos_y,
            size=WALL_SIZE,
            color=WALL_COLOR):
        super().__init__(
            game,
            pos_x, pos_y,
            elem_type="wall",
            size=size,
            color=color
        )

    def on_snake_hit(self, snake):
        snake.die()


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
            self.pos_x -= 1

        if direction == 'right':
            self.pos_x += 1

        if direction == 'up':
            self.pos_y -= 1

        if direction == 'down':
            self.pos_y += 1


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
        self.game.add_food('random_pos')
        self.game.score += 1

        self.tail.append(
            SnakeTail(
                self,
                self.tail[self.tail_length - 1]
            )
        )

    def in_valid_position(self, map):

        min_x, max_x = self.game.x_range
        min_y, max_y = self.game.y_range

        out_of_bounds = (
            (self.pos_x > max_x or self.pos_x < min_x) or
            (self.pos_y > max_y or self.pos_y < min_y)
        )

        return not out_of_bounds

    def die(self):
        self.is_alive = False

    def update(self):
        if self.is_alive:
            self.time_alive += self.game.tick_delay
            self.walk()

        if not self.in_valid_position(map):
            print('out')
            self.die()
            return

        element = self.game.element_at(self.pos_x, self.pos_y)
        if element is not None:
            element.on_snake_hit(self)

        self.turn()

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
            self.elem_type: {
                "id": self.elem_id,
                "bind": self.bind,
                "pos": self.pos,
                "lenght": self.lenght,
                "direction": self.direction,
                "turns": self.turns,
                "time_alive": self.time_alive,
                "is_alive": self.is_alive
            }
        }

    def keyboard_direction(self, event):
        direction = event.keysym.lower()
        self.next_dir = direction
