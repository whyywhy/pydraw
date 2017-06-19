import pygame
#import surfarray??
class pyselection(object):
    start = [0,0]
    end = [0,0]
    left = 0
    right = 0
    top = 0
    bottom = 0
    color = [0,0,0]
    is_showing = False
    
    def __init__(me):
        me.bounds = [0,0,0,0]
    def get_bounds(me):
        return [me.left,me.top,me.right-me.left,me.bottom-me.top]
    def check_bounds(me):
        me.left = min(me.start[0], me.end[0])
        me.right = max(me.start[0], me.end[0])
        me.top = min(me.start[1], me.end[1])
        me.bottom = max(me.start[1], me.end[1])
        #bounds = [left,top,left+right,top+bottom]
    def start_selection(me, mouse_x, mouse_y):
        me.start=[mouse_x,mouse_y]
        me.end=[mouse_x,mouse_y]
        me.check_bounds()
    def do_selection(me, screen, mouse_x, mouse_y, remove=False):
    #doto : add code to xor paint
        if me.is_showing:#remove old rect
            me.draw_xor_rect(screen)
            me.is_showing = False
            me.end = [mouse_x,mouse_y]
            me.check_bounds()
        #draw new rect
        if not remove:#use flag to remove selection
            me.draw_xor_rect(screen)
            me.is_showing = True
    def flip_pixel(me, screen, x, y):
    #todo : add checking for screen bounds or get IndexError (ValueError?)
        try:
            pixel = screen.get_at([x,y])
            pixel[0] = 255 - pixel[0]
            pixel[1] = 255 - pixel[1]
            pixel[2] = 255 - pixel[2]
            screen.set_at([x,y], pixel)
        except (ValueError, IndexError):
            print("Selection index out of bounds : x,y :"+str(x),str(y))
        
    def draw_xor_rect(me, screen):
        #make readable vars for our bounds
        for i in range(me.left, me.right):#top line
            me.flip_pixel(screen, i, me.top)
        for i in range(me.left, me.right):#bottom line
            me.flip_pixel(screen, i, me.bottom)
        for i in range(me.top+1, me.bottom - 1):#left line excludes top, bottom
            me.flip_pixel(screen, me.left, i)
        for i in range(me.top+1, me.bottom-1):#right line excludes top, bottom
            me.flip_pixel(screen, me.right, i)
class flood_filler(object):
    def __init__(me):
        pass
        #flood fill with normal color
    def floodfill(me, screen, color, point, bounds):
        target = screen.get_at(point)
        if target == color:
            return
        count = 0
        points = [point]#start a list, add our target point
        #print("flood fill bounds "+str(bounds)+" , point:"+str(point))
        while len(points)>0:
            pt = points.pop()
            #print ("I got point "+str(pt[0]),str(pt[1])+" and there's "+str(len(points))+" left.")
            if not (screen.get_at(pt) == target):
                print("Bad point found at:"+str(pt)+" , color :")
            else:
                fill_L = pt[0]-1
                while fill_L > bounds[0] and screen.get_at([fill_L,pt[1]]) == target:
                    fill_L -= 1
                fill_L += 1#back up one

                fill_R = pt[0]+1
                while fill_R < (bounds[0] + bounds[2]) and screen.get_at([fill_R,pt[1]]) == target:
                    fill_R += 1
                fill_L -= 1#back up one
                #now draw a line:
                count += 1
                #if count > 500:
                #    print("line "+str(fill_L),str(fill_R)+" at y : "+str(pt[1])+" ,points:"+str(len(points)))
                if count > 5000:
                    print("Exiting floodfill, count over 5000. points :"+str(len(points)))
                    return#in case of stuck loop
                
                added_last_up = False#flag saying we did not add the previous point
                added_last_down = False
                for i in range (fill_L,fill_R):
                    screen.set_at([i,pt[1]], color)#all drawing is done by this line
                    try:
                        if pt[1] > bounds[1] and screen.get_at([i,pt[1]-1]) == target:
                            if not added_last_up:
                                points.append([i, pt[1]-1])
                                #print ("added "+str(i),str(pt[1]-1))
                                added_last_up = True
                        else:
                            added_last_up = False#happens at end of loop, or if no match found above.
                    except (ValueError,IndexError):                        
                        print("Scan Up : Tried to access index : "+str(i),str(pt[1]-1))
                    
                    try:
                        if pt[1] < bounds[3]-1 and screen.get_at([i,pt[1]+1]) == target:
                            if not added_last_down:
                                points.append([i, pt[1]+1])
                                #print ("added "+str(i),str(pt[1]+1))
                                added_last_down = True
                        else:
                            added_last_down = False
                    except (ValueError,IndexError):
                        print("Scan Down: Tried to access index : "+str(i),str(pt[1]+1))
                    
    def gradientfloodfill(me, screen, gradient, point, bounds):
        target = screen.get_at(point)#the color we want to search and overwrite
        #we must never paint with the target color, it will cause infinite loop
        #so use a filler color when the gradient color is same as target
        #the filler is one point of difference in red, green and blue to the target.
        fill = [0,0,0,255]#alpha at 255
        if target[0]>128:
            fill[0] = target[0]-1
        else:
            fill[0] = target[0]+1
        if target[1]>128:
            fill[1] = target[1]-1
        else:
            fill[1] = target[1]+1
        if target[2]>128:
            fill[2] = target[2]-1
        else:
            fill[2] = target[2]+1
        fill=tuple(fill)#this makes a list [0,0,0,0] into a tuple (0,0,0,0) in format (Red,Green,Blue,Alpha) as used for colors
        count = 0
        points = [point]#start a list, add our target point
        #print("flood fill bounds "+str(bounds)+" , point:"+str(point)+"tar:"+str(target)+" ,fill:"+str(fill))
        while len(points)>0:
            pt = points.pop()
            #print ("I got point "+str(pt[0]),str(pt[1])+" and there's "+str(len(points))+" left.")
            thiscol = screen.get_at(pt)
            if not (thiscol == target):#this should not really happen... but it does ! why??
                print("Bad point found at:"+str(pt)+" , color :"+str(thiscol)+" ,target:"+str(target)+" ,fill:"+str(fill))
            else:
                fill_L = pt[0]-1
                while fill_L > bounds[0] and screen.get_at([fill_L,pt[1]]) == target:
                    fill_L -= 1
                fill_L += 1#back up one

                fill_R = pt[0]+1
                while fill_R < (bounds[0] + bounds[2]-1) and screen.get_at([fill_R,pt[1]]) == target:
                    fill_R += 1
                fill_L -= 1#back up one
                #now draw a line:
                count += 1    
                #if count > 2000:
                #    print("line "+str(fill_L),str(fill_R)+" at pt : "+str(pt)+" ,points:"+str(len(points)))
                if count > 5000:
                    print("Exiting floodfill, count over 5000. points :"+str(len(points)))
                    return#in case of stuck loop
                #each point we find is drawn as a horizontal line
                #so if we added the last point above (or below), we don't need to also add this one
                #as it is in the same line and will already have been drawn
                added_last_up = False#flag saying we did not add the previous point
                added_last_down = False
                for i in range (fill_L,fill_R+1):
                    color = gradient.get_color_at_points(point[0],point[1],i,pt[1])
                    #check that color is not target color, or we loop forever
                    #use filler if color == target
                    if color == target:
                        #print("used filler at point "+str(i),str(pt[1]))
                        color = fill
                    screen.set_at([i,pt[1]], color)#all drawing is done by this line
                    #if count > 2000:
                    #    print("drawing "+str(i),str(pt[1])+" , color:"+str(color)+" ,tar:"+str(target)+" ,count:"+str(count))
                    try:
                        if pt[1] > bounds[1] and screen.get_at([i,pt[1]-1]) == target:
                            if not added_last_up:
                                points.append([i, pt[1]-1])
                                #if count > 500:
                                #    print ("added "+str(i),str(pt[1]-1))
                                added_last_up = True
                        else:
                            added_last_up = False#happens at end of loop, or if no match found above.
                    except (ValueError,IndexError):                        
                        print("Scan Up : Tried to access index : "+str(i),str(pt[1]-1))
                    
                    try:
                        if pt[1] < bounds[3]-1 and screen.get_at([i,pt[1]+1]) == target:
                            if not added_last_down:
                                points.append([i, pt[1]+1])
                                #if count > 2000:
                                    #print ("added "+str(i),str(pt[1]+1))
                                added_last_down = True
                        else:
                            added_last_down = False
                    except (ValueError,IndexError):
                        print("Scan Down: Tried to access index : "+str(i),str(pt[1]+1))
                
