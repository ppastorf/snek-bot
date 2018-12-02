#!/usr/bin/python3

'''
	human playable version for testing and stuff
'''

import snake

# main game object
game = snake.Game()

# binds keyboard controls
game.root.bind('<Left>', game.keyboardLeft)
game.root.bind('<Right>', game.keyboardRight)
game.root.bind('<Up>', game.keyboardUp)
game.root.bind('<Down>', game.keyboardDown)

game.play()