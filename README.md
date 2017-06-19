"# pydraw" 
Python drawing application
Uses pygame library, install it with (for windows users) :
py -m pip install pygame --user
this assumes you have added python path variables when you installed it.#
About Pydraw :
===============
This project is an art program that lets you draw with gradients. The gradient code has been implemented in the Draw function and the Floodfill function. It will use a gradient from the Left colour to the Right colour. You can select a new colour by clicking the palette with left or right button. (The palette is dynamically generated, and can be made larger or smaller by changing the palette_size variable in the code.)

You can set the brush size and gradient length (how fast it changes) by rolling the mouse wheel over one of the 2 text boxes.

The Random option only works for draw. It will continually pick a random colour to change to while you are drawing.

The fill option will do a radial flood fill from the point you clicked. It can be used to quickly produce pseudo-3D effects. (e.g. draw a circle, then fill it using white/blue gradient for a 3d blue sphere)

The load and save options are rudimentary but functional, using a pre-set filename "Image1.bmp". 

