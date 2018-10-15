## IMPORTS ##
import abc


## SERIAL CONSTANTS ##
RED = 41
GREEN = 42
BLUE = 44
WHITE = 47


## SERIAL FUNCTIONS ##
def clearScreen():
    print('\x1B[2J')
def setBlack():
    print('\x1b[0m \x1B[?25l')
def setColour(colour):
    print('\x1b[0m \x1b[' + str(colour) + ';30m')
def drawBlock(x, y):
    print('\x1B[' + str(y) + ';' + str(x) + 'H ')  


## CLASSES ##
class Object:
    __metaclass__ = abc.ABCMeta
    
    # Constructor
    def __init__(self, top_pixel, colour):
        self._top_pixel = top_pixel
        self._colour = colour
    
    # Accessors
    def getTopPixel(self):
        return self._top_pixel
        
    @abc.abstractmethod
    def getPixels(self):
        pass
        
    @abc.abstractmethod
    def draw(self):
        pass
        
    @abc.abstractmethod
    def redraw(self):
        pass
       
        
class MovableObject(Object):
    __metaclass__ = abc.ABCMeta

    # Constructor
    def __init__(self, start_pixel, colour, ceiling_bound):
        Object.__init__(self, start_pixel, colour)
        self._ceiling_bound = ceiling_bound
        self._previous_pixel = start_pixel
    
    # Accessors
    @abc.abstractmethod
    def moveUp(self):
        pass
    
    @abc.abstractmethod
    def moveDown(self):
        pass


class Ball(MovableObject):
    
    # Constructor
    def __init__(self, pixel, colour, ceiling_bound, wall_bound,
        paddle_bound):
        MovableObject.__init__(self, pixel, colour, ceiling_bound)
        self._wall_bound = wall_bound
        self._direction = (1,-1)
        self._hit_paddle_bound = (paddle_bound[0] + 1,
            paddle_bound[1] - 1)
        
    def __repr__(self):
        return ("Ball at position " + self._top_pixel)
        
    # Accessors
    def __nearBoundry(self, axis, bound):
        if self._top_pixel[axis] <= bound[0] or self._top_pixel[axis] >= bound[1]:
            return True
        else:
            return False
            
    def __nearWall(self):
        return self.__nearBoundry(0, self._wall_bound)
        
    def __nearCeiling(self):
        return self.__nearBoundry(1, self._ceiling_bound)
        
    def nearPaddle(self):
        if self._top_pixel[0] <= self._hit_paddle_bound[0]:
            return 0
        elif self._top_pixel[0] >= self._hit_paddle_bound[1]:
            return 1
        else:
            return -1
            
    def getPixels(self):
        return [self._top_pixel]
    
    def draw(self):
        setColour(self._colour)
        drawBlock(*self._top_pixel)
        
    def redraw(self, clipping=[]):
        if not self._previous_pixel in clipping:
            setBlack()
            drawBlock(*self._previous_pixel)
        if not self._top_pixel in clipping:
            self.draw()
            
    # Mutators
    def __bounceWall(self):
        assert (self._top_pixel[0] <= self._wall_bound[0] or self._top_pixel[0] >= self._wall_bound[1])
        self._direction = (self._direction[0] * -1, self._direction[1])
    
    def __bounceCeiling(self):
        assert (self._top_pixel[1] <= self._ceiling_bound[0] or self._top_pixel[1] >= self._ceiling_bound[1])
        self._direction = (self._direction[0], self._direction[1] * -1)
        
    def movePhysics(self):
        if self.__nearCeiling():
            self.__bounceCeiling()
        if self.__nearWall():
            self.__bounceWall()
        self._previous_pixel = self._top_pixel
        self._top_pixel = (self._top_pixel[0] + self._direction[0], self._top_pixel[1] + self._direction[1])
        
    def moveUp(self):
        self._previous_pixel = self._top_pixel
        self._top_pixel = (self._top_pixel[0], self._top_pixel[1] - 1)
        
    def moveDown(self):
        self._previous_pixel = self._top_pixel
        self._top_pixel = (self._top_pixel[0], self._top_pixel[1] + 1)

    def bounceOffPaddle(self):
        assert(self.nearPaddle() != -1)
        self._direction = (self._direction[0] * -1, self._direction[1])
        
    def reposition(self, position):
        self._previous_pixel = self._top_pixel
        self._top_pixel = position
        
    def changeTrajectory(self, direction):
        self._direction = direction
        
        
class Score(Object):
    
    SCORES_TEMPLATE = {0:[(0,0),(0,1),(0,2),(0,3),(0,4),(1,0),(1,4),(2,0),(2,1),(2,2),(2,3),(2,4)],
                       1:[(2,0),(2,1),(2,2),(2,3),(2,4)],
                       2:[(0,0),(0,2),(0,3),(0,4),(1,0),(1,2),(1,4),(2,0),(2,1),(2,2),(2,4)],
                       3:[(0,0),(0,2),(0,4),(1,0),(1,2),(1,4),(2,0),(2,1),(2,2),(2,3),(2,4)],
                       4:[(0,0),(0,1),(0,2),(1,2),(2,0),(2,1),(2,2),(2,3),(2,4)],
                       5:[(0,0),(0,1),(0,2),(0,4),(1,0),(1,2),(1,4),(2,0),(2,2),(2,3),(2,4)],
                       6:[(0,0),(0,1),(0,2),(0,3),(0,4),(1,0),(1,2),(1,4),(2,0),(2,2),(2,3),(2,4)],
                       7:[(0,0),(1,0),(2,0),(2,1),(2,2),(2,3),(2,4)],
                       8:[(0,0),(0,0),(0,1),(0,2),(0,3),(0,4),(1,0),(1,2),(1,4),(2,0),(2,1),(2,2),(2,3),(2,4)],
                       9:[(0,0),(0,1),(0,2),(0,4),(1,0),(1,2),(1,4),(2,0),(2,1),(2,2),(2,3),(2,4)]}
                       
    WINNING_SCORE = 9
    
    # Constructor
    def __init__(self, top_pixel, colour):
        Object.__init__(self, top_pixel, colour)
        self._current_score = 0
        self._previous_score = 0
        
        self._scores = {}
        for key in Score.SCORES_TEMPLATE:
            self._scores[key] = []
            for pixel in Score.SCORES_TEMPLATE[key]:
                self._scores[key].append((pixel[0] + top_pixel[0], pixel[1] + top_pixel[1]))
                
    # Accessors
    def getPixels(self):
        return self._scores[self._current_score]
        
    def draw(self):
        setColour(self._colour)
        for pixel in self._scores[self._current_score]:
            drawBlock(pixel[0], pixel[1])
            
    def redraw(self):
        setBlack()
        for pixel in list(set(self._scores[self._previous_score]) - set(self._scores[self._current_score])):
            drawBlock(pixel[0], pixel[1])
        setColour(self._colour)
        for pixel in list(set(self._scores[self._current_score]) - set(self._scores[self._previous_score])):
            drawBlock(pixel[0], pixel[1])
                       
    def isVictory(self):
        if self._current_score == Score.WINNING_SCORE:
            return True
        else:
            return False
            
    # Mutators
    def increment(self):
        assert(self._current_score < 9)
        self._previous_score = self._current_score
        self._current_score += 1
                       
    def reset(self):
        self._previous_score = self._current_score
        self._current_score = 0
        
        
class Paddle(MovableObject):
    # Constructor
    def __init__(self, top_pixel, colour, ceiling_bound, leftORright,
        size):
        MovableObject.__init__(self, top_pixel, colour, ceiling_bound)
        self._leftORright = leftORright
        self._size = size
        self._bottom_pixel = (top_pixel[0], top_pixel[1] + self._size - 1)
        self._previous_bottom_pixel = self._bottom_pixel
    
    # Accessors
    def getServePixel(self):
        if self._leftORright == 0:
            return (self._top_pixel[0] + 1, (self._top_pixel[1] + self._bottom_pixel[1]) // 2)
        elif self._leftORright == 1:
            return (self._top_pixel[0] - 1, (self._top_pixel[1] + self._bottom_pixel[1]) // 2)
        else:
            raise ValueError("Invalid left or right value")
            
    def ballInFront(self, pixel):
        return (self._top_pixel[1] <= pixel[1] <= self._bottom_pixel[1])
        
    def getPixels(self):
        return [(self._top_pixel[0], y)\
            for y in range(self._top_pixel[1], self._bottom_pixel[1] + 1)]
    
    def draw(self):
        setColour(self._colour)
        for y_offset in range(self._size):
            drawBlock(self._top_pixel[0], self._top_pixel[1] + y_offset)
            
    def redraw(self):
        setBlack()
        if self._top_pixel[1] < self._previous_pixel[1]:
            drawBlock(*self._previous_bottom_pixel)
            setColour(self._colour)
            drawBlock(*self._top_pixel)
        elif self._top_pixel[1] > self._previous_pixel[1]:
            drawBlock(*self._previous_pixel)
            setColour(self._colour)
            drawBlock(*self._bottom_pixel)
            
    # Mutators
    def __updateBottomPixels(self):
        self._previous_bottom_pixel = self._bottom_pixel
        self._bottom_pixel = (self._top_pixel[0], self._top_pixel[1] + self._size - 1)
        
    def moveUp(self):
        if self._ceiling_bound[0] != self._top_pixel[1]:
            self._previous_pixel = self._top_pixel
            self._top_pixel = (self._top_pixel[0], self._top_pixel[1] - 1)
            self.__updateBottomPixels()
        
    def moveDown(self):
        if self._ceiling_bound[1] != self._top_pixel[1]:
            self._previous_pixel = self._top_pixel
            self._top_pixel = (self._top_pixel[0], self._top_pixel[1] + 1)
            self.__updateBottomPixels()
      
            
class Net(Object):
    # Constructor
    def __init__(self, top_pixel, colour, length):
        Object.__init__(self, top_pixel, colour)
        self._pixels = [(top_pixel[0], y) for y in range(3, length, 4)]\
            + [(top_pixel[0], y+1) for y in range(3, length, 4)]
            
    # Accessors
    def getPixels(self):
        return self._pixels
            
    def draw(self):
        setColour(self._colour)
        for pixel in self._pixels:
            drawBlock(*pixel)
            
    def redraw(self):
        self.draw()


class Player:
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, symbol_id):
        self._id = symbol_id
        
    @abc.abstractmethod
    def makeMove(self):
        pass
