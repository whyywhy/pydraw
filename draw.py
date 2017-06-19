# Import a library of functions called 'pygame'
import pygame
import os
import urllib#file load and save
from math import pi
from gradient import *
from pybutton import *
from pyselection import *

#debug flag to see printouts
debug = False
#FPS
FRAMES_PER_SECOND = 60
MOUSE_SCROLL_STEP = 10
#set window pos
x = 20
y = 30
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)

#some local vars
dragging = False
mouse_x = 0
mouse_y = 0
mouse_button_1 = False
mouse_button_2 = False
mouse_button_3 = False
mouse_wheel = 0
draw_color = BLACK
draw_mode = "Paint"
size = [0,0]
selection = pyselection()
#You can change these variables below
brush_size = 30
grad_length = 60
use_random = False
use_gradient = True
palette_size = 5#Generated palette will be the cube of this number+1, e.g. 5*5*5+1=126 or 2*2*2=9. must be >=2
draw_grad_right = gradient(WHITE, BLACK, 130, False, False)
draw_grad_left = gradient(YELLOW, RED, 50, False, False)

#drawing code
def draw_at_point(screen): 
    global draw_mode
    if mouse_x < 200:
        return
    if mouse_button_1:
        if use_gradient :
            draw_color = draw_grad_left.get_next_color()
        else:
            draw_color = buttons[2].color
        if draw_mode == "Paint":
            rect = [mouse_x - brush_size, mouse_y - brush_size, mouse_x + brush_size, mouse_x + brush_size]
            pygame.draw.circle(screen, draw_color, [mouse_x, mouse_y], brush_size) 
        elif draw_mode == "Rect" or draw_mode == "Oval":#share code for selection
            if dragging:
                selection.do_selection(screen, mouse_x, mouse_y)            
            else:
                selection.start_selection( mouse_x, mouse_y)
        elif draw_mode == "Fill":
            flood = flood_filler()
            if use_gradient:
                flood.gradientfloodfill(screen,draw_grad_left,[mouse_x,mouse_y],[200,0,size[0]-200,size[1]])
            else:
                flood.floodfill(screen,draw_color,[mouse_x,mouse_y],[200,0,size[0]-200,size[1]])
    elif mouse_button_3:
        if use_gradient :
            draw_color = draw_grad_right.get_next_color()
        else:
            draw_color = buttons[3].color
        rect = [mouse_x - brush_size, mouse_y - brush_size, mouse_x + brush_size, mouse_x + brush_size]
        if draw_mode == "Paint":
            rect = [mouse_x - brush_size, mouse_y - brush_size, mouse_x + brush_size, mouse_x + brush_size]
            pygame.draw.circle(screen, draw_color, [mouse_x, mouse_y], brush_size) 
        elif draw_mode == "Rect" or draw_mode == "Oval":#share code for selection
            if dragging:
                selection.do_selection(screen, mouse_x, mouse_y)            
            else:
                selection.start_selection( mouse_x, mouse_y)

def check_button_click():
    global draw_mode
    if not mouse_wheel == 0 and not mouse_button_1 and not mouse_button_3:
        return
    
    for button in buttons:
        if button.has_point([mouse_x,mouse_y]):
            #print ("You clicked "+button.text)
            if(button.text == "Palette"):
                col = button.get_color_at([mouse_x,mouse_y])
                if mouse_button_1:
                    buttons[2].color = col
                    buttons[2].needs_redraw = True
                elif mouse_button_3:
                    buttons[3].color = col
                    buttons[3].needs_redraw = True  
                do_gradient()
            elif button.text == "Save":
                #crop the toolbar out of the image. width = 200
                cropped = pygame.Surface((size[0]-200,size[1]))
                cropped.blit(screen, (0, 0), (200, 0, size[0], size[1]))
                pygame.image.save(cropped, "image1.bmp")
            elif button.text == "Load":
                #crop the toolbar out of the image. width = 200
                cropped = pygame.image.load("image1.bmp")
                screen.blit(cropped, (200,0))
            else:
                button.press()
                if button.button_group == 1:#used for paint modes
                    draw_mode = button.text
            for check in buttons:
                if not check == button and button.button_group >= 0 and check.button_group == button.button_group:
                    check.pressed = False
                    #print ("Disabled "+check.text+" which is same group as "+button.text)
            click_button(button)

def click_button(button):
    if button.text == "Random":
        global use_random
        use_random = button.pressed
        do_gradient()
        print ("random set to :"+str(use_random))
    elif button.text == "Gradient":
        global use_gradient
        use_gradient = button.pressed
        print ("gradient set to :"+str(use_gradient))


def check_mouse_scroll():
    #print ("check scroll")
    if buttons[2].has_point([mouse_x,mouse_y]):
        buttons[2].scroll_mouse(mouse_wheel, [mouse_x,mouse_y])
        do_gradient()
    elif buttons[3].has_point([mouse_x,mouse_y]):
        buttons[3].scroll_mouse(mouse_wheel, [mouse_x,mouse_y])
        do_gradient()
    elif buttons[10].has_point([mouse_x,mouse_y]):#brush
        buttons[10].scroll_mouse(mouse_wheel, [mouse_x,mouse_y])
        global brush_size
        brush_size = buttons[10].value
        
    elif buttons[11].has_point([mouse_x,mouse_y]):#grad len
        buttons[11].scroll_mouse(mouse_wheel, [mouse_x,mouse_y])
        global grad_length
        grad_length = buttons[11].value
        do_gradient()
def do_gradient():
    #so set our 2 gradients to the colors on Right and Left buttons (index 2 and 3)
    draw_grad_left.set(buttons[2].color, buttons[3].color, grad_length, False, use_random)
    draw_grad_right.set(buttons[3].color, buttons[2].color, grad_length, False, use_random)
    
# Set the height and width of the screen
pygame.init()
pygame.display.init()
#Declare GUI:
info = pygame.display.Info()
size = [int(info.current_w/2), int(info.current_h/2)]

buttons = []
buttons.append(pybutton((20,40,80,30),GREY,"Random",-1,True,use_random))
buttons.append(pybutton((120,40,80,30),GREY,"Gradient",-1,True,use_gradient))

buttons.append(pycolorbutton((20,90,80,30),YELLOW,"Left"))
buttons.append(pycolorbutton((120,90,80,30),RED,"Right"))


buttons.append(pybutton((20,140,80,30),GREY,"Paint",1, False, True))#last True sets it to Pressed
buttons.append(pybutton((120,140,80,30),GREY,"Fill",1))

buttons.append(pybutton((20,190,80,30),GREY,"Rect",1))
buttons.append(pybutton((120,190,80,30),GREY,"Oval",1))

buttons.append(pybutton((20,0,80,20),BLUE,"Load",40,1,500))
buttons.append(pybutton((120,0,80,20),RED,"Save",60,10,500))

buttons.append(spinnerbutton((20,225,80,20),WHITE,"Brush",40,1,500))
buttons.append(spinnerbutton((120,225,80,20),WHITE,"GradLen",60,10,500))

buttons.append(palettebutton((0,270,200,size[1]-230), (palette_size**3)+1, 10))
do_gradient()
info = pygame.display.Info()
size = [int(2*info.current_w/3), int(2*info.current_h/3)]
screen = pygame.display.set_mode(size, pygame.RESIZABLE)
# Clear the screen and set the screen background
screen.fill(WHITE)
#Draw toolbox panel:
pygame.draw.rect(screen, L_GREY, [0,0,200,size[1]])
 
pygame.display.set_caption("pygame Gradient Draw Tool by Joeri Beckers")
 
#Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()


while not done:
 
    # This limits the while loop to a max of 10 times per second.
    # Leave this out and we will use all CPU we can.
    clock.tick(FRAMES_PER_SECOND)
     
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop
        elif event.type == pygame.MOUSEMOTION:
            pos = pygame.mouse.get_pos()
            mouse_x = pos[0]
            mouse_y = pos[1]
            if dragging:
                draw_at_point(screen)
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            mouse_x = pos[0]
            mouse_y = pos[1]
            draw_grad_left.reset()
            draw_grad_right.reset()
            check_button_click()
            dragging=False
            had_rect = selection.is_showing#store this, need to know if we had a selection to draw oval / rect
            selection.do_selection(screen,mouse_x,mouse_y,True)#remove any selection we may have
            #case rect and oval, we can draw the selection here.
            #only if we have a selection
            if had_rect:
                if draw_mode == "Rect":
                    if mouse_button_1:
                        pygame.draw.rect(screen, buttons[2].color, selection.get_bounds())
                    elif mouse_button_3:
                        pygame.draw.rect(screen, buttons[3].color, selection.get_bounds())                
                elif draw_mode == "Oval":
                    if mouse_button_1:
                        pygame.draw.ellipse(screen, buttons[2].color, selection.get_bounds())
                    elif mouse_button_3:
                        pygame.draw.ellipse(screen, buttons[3].color, selection.get_bounds())                
            #redraw toolbox panel after drawing op, so we can disable it during for better performance
            pygame.draw.rect(screen, L_GREY, [0,0,200,size[1]])
            for button in buttons:        
                button.draw(screen,True)
            (mouse_button_1,mouse_button_2,mouse_button_3) = pygame.mouse.get_pressed()#do it at end, so we know which button WAS down
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            mouse_x = pos[0]
            mouse_y = pos[1]
            (mouse_button_1,mouse_button_2,mouse_button_3) = pygame.mouse.get_pressed()
            if event.button == 4:   
                mouse_wheel = MOUSE_SCROLL_STEP
                check_mouse_scroll()
            elif event.button == 5:   
                mouse_wheel = -MOUSE_SCROLL_STEP
                check_mouse_scroll()
            else:
                mouse_wheel = 0
            draw_at_point(screen)
            dragging=True 
    #GUI :

    #draw buttons if they changed:
    for button in buttons:        
        button.draw(screen)
    # All drawing code happens after the for loop and but
    # inside the main while done==False loop.
    # Go ahead and update the screen with what we've drawn.
    # This MUST happen after all the other drawing commands.
    pygame.display.flip()
 
# Be IDLE friendly
pygame.quit()