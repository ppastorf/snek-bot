#!/usr/bin/python3

import game.snake as sn

'''
	human playable version for testing and stuff
'''

game = sn.Game()

# binds keyboard controls
game.root.bind('<Left>', game.keyboardLeft)
game.root.bind('<Right>', game.keyboardRight)
game.root.bind('<Up>', game.keyboardUp)
game.root.bind('<Down>', game.keyboardDown)

game.play()