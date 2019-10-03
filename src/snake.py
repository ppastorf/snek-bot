from random import randrange

X_SIZE = 400
Y_SIZE = 400
OFFSET = 10

DEFAULT_SIZE = 10
DEFAULT_COLOR = "#aaaaaa"

SNAKE_SIZE = DEFAULT_SIZE
FOOD_SIZE = DEFAULT_SIZE

FOOD_COLOR = "#006600"
HEAD_COLOR = "#804d00"
BODY_COLOR = "#e68a00"


class Element(object):
    def __init__(self, pos_x, pos_y,
                 color=DEFAULT_COLOR,
                 size=DEFAULT_SIZE):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.color = color
        self.size = size

    def show(self, canvas):
        canvas.create_rectangle(
            self.pos_x,
            self.pos_y,
            self.pos_x + self.size,
            self.pos_y + self.size,
            fill=self.color
        )

    @property
    def pos(self):
        return self.pos_x, self.pos_y


class Food(Element):
    def __init__(
            self,
            mapsize_x, mapsize_y,
            size=FOOD_SIZE, color=FOOD_COLOR):
        super().__init__(
            randrange(0, mapsize_x, size),
            randrange(0, mapsize_y, size),
            color=color
        )


class SnakeBody(Element):

    def __init__(self, last_part, size=SNAKE_SIZE, color=BODY_COLOR):
        super().__init__(
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

    def __init__(self, start_x, start_y, size=SNAKE_SIZE, color=HEAD_COLOR):
        super().__init__(
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
    def __init__(self, start_dir='left', lenght=1, size=SNAKE_SIZE):
        self.direction = start_dir
        self.head = SnakeHead()
        self.body = []

        for i in range(lenght):
            self.body.append(
                SnakeBody(self.head)
            )

    def show_body(self, canvas):
        for i in range(0, self.body_size):
            self.body[i].show(canvas)

    def show(self, canvas):
        self.head.show(canvas)
        self.show_body(canvas)

    def walk(self):
        self.head.walk(self.direction)

        for i in range(0, self.body_size):
            self.body[i].walk()

    def turn(self, new_dir):
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

    @property
    def pos_x(self):
        return self.head.pos_x

    @property
    def body_size(self):
        return len(self.body)

    @property
    def in_valid_position(self):
        return not (
            (self.pos_x >= X_SIZE - OFFSET or self.pos_x < OFFSET or
             self.pos_y >= Y_SIZE - OFFSET or self.pos_y < OFFSET) or
            (any([parts.pos == self.pos for parts in self.body]))
        )

    @property
    def eat(self):
        self.body.append(
            SnakeBody(self.body[self.body_size - 1])
        )

    @property
    def pos_y(self):
        return self.head.pos_y

    @property
    def pos(self):
        return self.head.pos
