from random import randint
from math import sqrt
debug = False
# Define the colors we will use in RGB format
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
L_GREY= (200, 200, 200)
GREY =  (125, 125, 125)
D_GREY= ( 80,  80,  80)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)
YELLOW = (255, 255,  0)
class gradient(object):
    rstep = 0.0
    gstep = 0.0
    bstep = 0.0
    pos = 0
    reverse = False
    random = True
    last_color = BLACK
    #astep = 0.0
	

    def __init__(me,start=BLACK,end=WHITE,steps=40,reversing=False,random=True):
        me.start = start
        me.end = end
        me.steps = steps
        me.pos = 0
        me.reversing = reversing
        me.random = random
        me.get_color_steps()
        
    def get_color_at(me, Position):
        if me.reversing:		
            iMid = int(me.steps/2)
            Position = Position % me.steps
            if Position>iMid:			
                Position = (iMid - (Position-iMid))*2;
            else:
                Position = Position * 2;
        else:
            if Position> me.steps: 
                Position = me.steps
                
        iRed = me.start[0]+int((Position*me.rstep));
        iGreen = me.start[1]+int((Position*me.gstep));		
        iBlue = me.start[2]+int((Position*me.bstep));
		#iAlpha = clStart.getAlpha()+(int)((float)Position*fAlpha);
        return (iRed,iGreen,iBlue,255)

    def get_color_at_points(me, x1,y1,x2,y2):
	
		#use distance from source as 'Position' of gradient
        height = int(sqrt((abs(x1-x2)** 2)+(abs(y1-y2)** 2)))
        clNew = me.get_color_at(height)
        #int[] fill =  new int[] {clNew.getRed(), clNew.getGreen(), clNew.getBlue(), clNew.getAlpha()}; 
        return clNew;

    def get_color_steps(me):
        me.rstep = (me.end[0] - me.start[0]) / float(me.steps)
        me.gstep = (me.end[1] - me.start[1]) / float(me.steps)
        me.bstep = (me.end[2] - me.start[2]) / float(me.steps)
        #me.astep = float(me.start[3] - me.end[3]) / float(me.steps)
        
    def set_step(me,step):
        me.steps = steps
        me.get_color_steps()
    def set(me,start=BLACK,end=WHITE,steps=40,reversing=False,random=True):
        me.start = start
        me.end = end
        me.steps = steps
        me.pos = 0
        me.reversing = reversing
        me.random = random
        me.get_color_steps()

    def get_next_color(me):
        if me.reverse:
            if me.pos > 1:
                me.pos -= 2
            else:
                me.pos = 0
                me.reverse = False
                if me.random:
                    me.get_random_colors()
        else:
            if me.pos < me.steps:
                if me.reversing:
                    me.pos += 2
                else:
                    me.pos += 1
            else:
                if me.reversing:
                    me.reverse = True
                elif me.random:
                    me.get_random_colors()

        result = [int(me.start[0] + (me.pos * me.rstep)),
            int(me.start[1] + (me.pos * me.gstep)),
            int(me.start[2] + (me.pos * me.bstep))]
        me.last_color = result
        return result

    def reset(me):
        me.pos = 0
        me.reverse = False
    def __repr__(me):
        return ("Start:"+str(me.start)+", End:"+str(me.end)+", Pos:"+str(me.pos)+", Steps:"+str(me.steps)+", Reversing:"+str(me.reversing))
    def get_random_colors(me):
        me.pos = 0
        me.start = me.end
        me.end = me.get_random_color()
        #me.step = randint(30,80)
        me.get_color_steps()
    def get_random_color(self):
        return [randint(0,255),randint(0,255),randint(0,255)]
    def dark_to_light(self, first, second):
        if(first[0]+first[1]+first[2]) > (second[0] + second[1] + second[2]):
            return [second, first]
        else:
            return [first, second]

    def light_to_dark(self, first, second):
        if(first[0]+first[1]+first[2]) > (second[0] + second[1] + second[2]):
            return [first, second]
        else:
            return [second, first]
#end class Gradient