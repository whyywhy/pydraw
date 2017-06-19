import pygame

class pybutton(object):
    bounds = (60,60,100,36)
    needs_redraw = True#aww they haven't had their first draw yet :)
    pressed = False
    pressable = True
    toggle = False
    text = ""
    color = (200,200,200)#RGB
    button_group = -1
    def __init__(me,rect,color,text,button_group=-1,toggle=False, pressed = False):
        me.bounds = rect
        me.color = color
        me.text = text
        me.button_group = button_group
        me.toggle = toggle
        me.pressed = pressed
    def has_point(me, point):
        result =  ( point[0] > me.bounds[0] and point[1] > me.bounds[1] and point[0] < (me.bounds[0] + me.bounds[2]) and point[1] < (me.bounds[1] + me.bounds[3]))
        return result
    def draw(me, screen, force = False):
        if force == False and not me.needs_redraw:
            return
        pygame.draw.rect(screen, me.color, me.bounds)
        if me.pressed:
            font_color = [255,255,255]
        else:
            font_color = [0,0,0]
        try:
            font = pygame.font.Font(None,24)
            scrtext = font.render(me.text, True, font_color)
            screen.blit(scrtext, [me.bounds[0]+6, me.bounds[1]+4])
        except Exception as message:
            raise SystemExit(message)
            print ('Font Error, saw it coming'+str(message))
        me.needs_redraw = False
    def press(me):
        if me.pressable:
            last_pressed = me.pressed
            if me.toggle:
                me.pressed = not me.pressed
            else:
                me.pressed = True
            if not last_pressed == me.pressed:
                me.needs_redraw = True

class pycolorbutton(pybutton):
    pressable = False
    def scroll_mouse(me, mouse, point):
        old_color = me.color
        red = me.color[0]
        green = me.color[1]
        blue = me.color[2]
        #print ("Scroll mouse on " + me.text + ", direction:"+str(mouse)+", point :"+str(point))
        x_dist = point[0] - me.bounds[0]
        third_width = me.bounds[2]/3
        if (x_dist < third_width):
            if red + mouse < 255 and red + mouse >= 0:
                red += mouse
        elif x_dist >= third_width and x_dist < (third_width * 2):
            if green + mouse < 255 and green + mouse >= 0:
                green += mouse
        else:             
            if blue + mouse < 255 and blue + mouse >= 0:
                blue += mouse
        me.color = [red, green, blue]
        me.needs_redraw = True
        print ("Width:"+str(me.bounds[2])+", third:"+str(third_width)+", dist:"+str(x_dist)+"old color:"+str(old_color)+", new color:"+str(me.color))

class spinnerbutton(pycolorbutton):
    value = 0
    
    def __init__(me,rect,color,text,value,min = 5, max=1000):
        me.bounds = rect
        me.color = color
        me.text = text
        me.value = value
        me.min = min
        me.max = max
    def scroll_mouse(me, mouse, point):
        if mouse > 0:
            if me.value + mouse <= me.max:
                me.value += mouse
            else:
                me.value = me.max
        else:
            if me.value + mouse >= me.min:
                me.value += mouse
            else:
                me.value = me.min
        me.needs_redraw = True
        #print ("Spinner "+me.text+" now has the value "+str(me.value))
    def draw(me, screen, force = False):
        if force == False and not me.needs_redraw:
            return
        pygame.draw.rect(screen, me.color, me.bounds)
        if me.pressed:
            font_color = [255,255,255]
        else:
            font_color = [0,0,0]
        try:
            font = pygame.font.Font(None,14)
            scrtext = font.render(me.text+": "+ str(me.value), True, font_color)
            screen.blit(scrtext, [me.bounds[0]+6, me.bounds[1]+4])
        except Exception as message:
            raise SystemExit(message)
            print ('Font Error, saw it coming'+str(message))
        me.needs_redraw = False
                
        
class palettebutton(pybutton):
    palette_size=32
    tile_size=10
    rows=20
    cols=20
    color = [80,80,80]# dark grey
    colors = []
    text = "Palette"

    def generate_palette(me):
        #using cubic root it will generate the closest palette to the given palette size
        step_size = int(me.palette_size ** (1. / 3))#cubic root
        print ("palette size:"+str(me.palette_size)+", stepsize:"+str(step_size))
        for i in range (0, step_size):#r loop
            for t in range (0, step_size):#g loop
                for q in range (0, step_size):#b loop
                    if i == t and t == q:#this is a greyscale, stick it at the start
                        me.colors.insert(0,[255-int(i * (256 /step_size)), 255-int(t * (256 /step_size)), 255-int(q * (256 /step_size))])
                    else:
                        me.colors.append([255-int(i * (256 /step_size)), 255-int(t * (256 /step_size)), 255-int(q * (256 /step_size))])
                        

        #set new palette size
        me.colors.insert(0,[0,0,0])
        me.palette_size = len(me.colors)
        print ("generated :"+str(me.palette_size)+" colors.")
        me.do_layout()
    def __init__(me,rect,palette_size=32,tile_size=10):
        me.bounds = rect
        if(palette_size<2):
            palette_size = 2
        me.palette_size = palette_size
        me.tile_size = tile_size
        me.generate_palette()
    def do_layout(me):
        #we can grow the tilesize to the max that will fit in the bounds
        tilesize = me.tile_size
        print ("Do layout : Begin with tile size "+str(tilesize)+" and cols / rows :"+str(me.cols),str(me.rows))
        print ("Bounds :"+str(me.bounds))
        while True:
            x_tiles=int(me.bounds[2]/tilesize)
            y_tiles=int(me.bounds[3]/tilesize)
            if x_tiles * y_tiles >= me.palette_size:
                tilesize += 1
                #print ("Trying tilesize "+str(tilesize)+" with cols, rows:"+str(x_tiles),str(y_tiles))
            else:
                break#when we break, we've gone over the limit, so go back one:
                
        tilesize -= 1    
        x_tiles=int(me.bounds[2]/tilesize)
        y_tiles=int(me.bounds[3]/tilesize)
            
        me.tile_size = tilesize
        me.rows = y_tiles
        me.cols = x_tiles
        print ("Do layout : Now I have tile size "+str(tilesize)+" and cols / rows :"+str(me.cols),str(me.rows))
    def draw(me,screen, force=False):
        if force == False and not me.needs_redraw:
            return
        me.needs_redraw = False
        #use rows, cols and tilesize
        for i in range (0,me.cols):
            for t in range (0,me.rows):
                index = (t * me.cols) + i
                rect = [me.bounds[0] + (i * me.tile_size),me.bounds[1] + (t * me.tile_size),me.tile_size,me.tile_size]
                if index < len(me.colors):
                    pygame.draw.rect(screen, me.colors[index], rect)
                else:
                    break
    def get_color_at(me, point):#
        print ("get color at :"+str(point))
        #work out index from grid :
        x_grid = int((point[0] - me.bounds[0]) / me.tile_size)
        y_grid = int((point[1] - me.bounds[1]) / me.tile_size)
        index = int(x_grid + (y_grid * me.cols))
        if(index >= len(me.colors)):#exceeds index 
            return [200, 200, 200]#matches panel col
        else:
            print ("Clicked on color :"+str(me.colors[index]))
            return me.colors[index]
        