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

# Rotate through scores
DELAY = 0.5
my_scores = (Score((29, 2), RED), Score((47, 2), GREEN))
my_scores[0].draw()
my_scores[1].draw()
while True:
	if my_scores[0].isVictory():
		time.sleep(DELAY)
		my_scores[0].reset()
		my_scores[0].redraw()
	if my_scores[1].isVictory():
		time.sleep(DELAY)
		my_scores[1].reset()
		my_scores[1].redraw()
	time.sleep(DELAY)
	my_scores[0].increment()
	my_scores[0].redraw()
	time.sleep(DELAY)
	my_scores[1].increment()
	my_scores[1].redraw()