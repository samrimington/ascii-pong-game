from pong_logic import *
import time

PERIOD = 1/60.0
WINDOWWIDTH = 80
WINDOWHEIGHT = 20
WALLBOUND = (1, WINDOWWIDTH)
CEILINGBOUND = (1, WINDOWHEIGHT)
PADDLEDISTANCE = 2
PADDLEBOUND = (WALLBOUND[0] + PADDLEDISTANCE,
	WALLBOUND[1] - PADDLEDISTANCE)

PADDLESIZE = 3
LARGEPADDLESIZE = 6

clearScreen()

# Draw two paddles and move them a bit
my_paddles = [Paddle((PADDLEBOUND[0], 8), WHITE, CEILINGBOUND, 0, PADDLESIZE),
	Paddle((PADDLEBOUND[1], 14), RED, CEILINGBOUND, 1, PADDLESIZE)]
my_paddles[0].draw()
my_paddles[1].draw()
for _ in range(7):
	time.sleep(0.5)
	my_paddles[0].moveDown()
	my_paddles[1].moveUp()
	my_paddles[0].redraw()
	my_paddles[1].redraw()
time.sleep(5)