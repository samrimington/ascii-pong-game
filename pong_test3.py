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

# Bounce ball across screen, update score when it hits paddle boundries
my_ball = Ball((9, 4), BLUE, CEILINGBOUND, WALLBOUND, PADDLEBOUND)
my_scores = [Score((29, 2), RED), Score((47, 2), GREEN)]
my_ball.draw()
my_scores[0].draw()
my_scores[1].draw()

while True:
	while my_ball.nearPaddle() == -1:
		my_ball.movePhysics()
		my_ball.redraw(list(set(my_scores[0].getPixels())\
			| set(my_scores[1].getPixels())))
		time.sleep(PERIOD)
	if my_scores[my_ball.nearPaddle()].isVictory():
		my_scores[my_ball.nearPaddle()].reset()
	else:
		my_scores[my_ball.nearPaddle()].increment()
	my_scores[my_ball.nearPaddle()].redraw()
	my_ball.bounceOffPaddle()
	my_ball.movePhysics()
	my_ball.redraw()
	time.sleep(PERIOD)