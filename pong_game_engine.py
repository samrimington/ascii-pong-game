## IMPORTS ##
from pong_logic import *
import time

## CONSTANTS ##
PERIOD = 1/45.0
DELAY = 1
WINDOWWIDTH = 80
WINDOWHEIGHT = 20
PADDLESIZE = 3
LARGEPADDLESIZE = 6
NUMBEROFSERVESPERPLAYER = 5

WALLBOUND = (1, WINDOWWIDTH)
CEILINGBOUND = (1, WINDOWHEIGHT)
PADDLEDISTANCE = 2
PADDLEBOUND = (WALLBOUND[0] + PADDLEDISTANCE,
	WALLBOUND[1] - PADDLEDISTANCE)
PADDLESTART = WINDOWHEIGHT / 2

## MAIN CODE ##
clearScreen()

serving_paddle = 0

# Arena objects
players = {
	0 : Paddle((PADDLEBOUND[0], PADDLESTART), BLUE, CEILINGBOUND, 0, PADDLESIZE),
	1 : Paddle((PADDLEBOUND[1], PADDLESTART), RED, CEILINGBOUND, 1, PADDLESIZE)
		   }	
scores = [Score((29, 2), BLUE), Score((49, 2), RED)]
ball = Ball(players[serving_paddle].getServePixel(), GREEN, CEILINGBOUND,
	WALLBOUND, PADDLEBOUND)	
net = Net((40, 0), WHITE, WINDOWHEIGHT)

servings_count = 0
clipping = list(set(scores[0].getPixels()) | set(scores[1].getPixels())\
	| set(net.getPixels()))
	
def oppositeLeftOrRight(leftORright):
	if leftORright == 0:
		return 1
	else:
		return 0

def drawAll():
	players[0].draw()
	players[1].draw()
	scores[0].draw()
	scores[1].draw()
	net.draw()
	ball.draw()
        
def serveBall():
	if serving_paddle == 0:
		ball.changeTrajectory((1,-1))
	else:
		ball.changeTrajectory((-1,1))
	moveBall()
	
def moveBall():
	ball.movePhysics()
	ball.redraw(clipping)
	
def updateServings():
	global servings_count, serving_paddle
	servings_count += 1
	if servings_count % NUMBEROFSERVESPERPLAYER == 0:
		serving_paddle = oppositeLeftOrRight(serving_paddle)

def updateScore(leftORright):
	global clipping
	clipping = list(set(clipping) - set(scores[leftORright].getPixels()))
	scores[leftORright].increment()
	scores[leftORright].redraw()
	clipping = list(set(clipping) | set(scores[leftORright].getPixels()))
	
def newRound():
	updateServings()
	updateScore(oppositeLeftOrRight(ball.nearPaddle()))
	ball.reposition(players[serving_paddle].getServePixel())
	ball.redraw()
	      
def isWinner():
	return (scores[0].isVictory() or scores[1].isVictory())
        
drawAll()
while not isWinner():
	time.sleep(DELAY)
	serveBall()
	while True:
		while ball.nearPaddle() == -1:
			time.sleep(PERIOD)
			moveBall()
		if players[ball.nearPaddle()].ballInFront(ball.getTopPixel()):
			time.sleep(PERIOD)
			ball.bounceOffPaddle()
			moveBall()
		else:
			newRound()
			break
