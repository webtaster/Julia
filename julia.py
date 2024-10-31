#!/usr/bin/python

# Very simple Mandlebrot/Julia plotting in Python.

# Needed with Python 2 only.  Expected behaviour of '/'.  See pep 238
#from __future__ import division

from graphics import *

# tkColors.py must be in the current working directory
from tkColors import tkColors

###############################################################################

def iterate(maxitr, z, c):

   # Apply the function, usually z = z*z +c, recursively to the given complex
   # point z.  Check to see if the result tends towards zero (making the initial
   # z a member of the set) or tends towards infinity.   

   # Assume the function is stable (tends towards zero) unless the subsequent
   # loop proves otherwise
   stable = True


   for a in range(1, maxitr):


      # Calculate the next value of z.  This is the central equation that
      # produces the fractal.
      z  = z*z + c

      size = abs(z)

      # Series has gone unstable.
      if size > stability_threshold:
         stable = False
         break

      if size < zero_threshold:
         #print "Stable break after", a
         break


   # Series is stable (tends towards zero) after all iterations.  Plot it
   # as a black point.
   if stable:

      # Slight optimization, don't plot black points, as the backgound is black.  Just
      # leave them unplotted.
      pass
      #win.plot(disp_x, disp_y, 'black')
   else:
      # Colour unstable area according to the number of iterations before instability


      # This is a bit random but clear
      color = tkColors[(a+25) % 750]
      #color = tkcolors[(int(a*10)+1) % 750]
      #color = tkColors[a % 750]

      # Uncomment for a nice graded monochome rendering
      #color = color_rgb(a*4, a*4, a*4)

      win.plot(disp_x, disp_y, color)


   return a

###############################################################################



# Size of grapics window, in pixels
height  = 800 
width   = 1000


# Set the initial zoom factor so that plotting from -2 to 2 in the x direction
# fills the graphic window horizontally
x_range_size = 4

# Magnification factor to map the mathematical space onto the graphics window.
# We will divide the screen cordinates by this later on to get the mathematical
# numbers to process.  This default zoom value fits a whole julia or mandlebrot set
# comfortably into the graphics window, sized as above.  Initially about 250, 
# magnifying the range of interest (about -2 to 2) into the graphics window 
# sized roughly as the above height and width.
zoom = width/x_range_size


################################################################################### 
# The following 5 settings are editable: zoom (again), x and y offset, 'julia'
# and c.  Changing them will produce different and interesting fractal images.
###################################################################################

# Set a greater zoom here, to view details.
zoom = 200

# Offset value.  Controls which part of the set to draw when zoomed in.  The
# centre of the graphics window corresponds to this setting.  This is a 
# mathematical value, obviously, (and not a direct screen coordinate) 
x_offset = 0
y_offset = 0

#x_offset = -0.127
#y_offset = 0.986
#x_offset = -0.09759759759759731
#y_offset = 0.8735919899874842



# Set to True for a Julia set, False for Mandlebrot
julia = True

# Applies to Julia sets only.  The value of the constant.  A setting
# of (-1, 0) (that is to say, -1+j0) draws the classic Julia shape.
# Try other values too.
c = complex(-1, 0)
#c = complex(-0.512511498387847167, 0.521295573094847167)


################################
# End of frequently edited bits
################################


#
# The following parameters rarely need adjustment
#

# Stability threshold.  Any comlex value with a size graater than this will
# be considered to indiacte an unstable (or becoming ever larger) point/series. 
stability_threshold = 2

# A complex value with a size less than this will be taken to indiacte that
# the series is tending towards zero, getting smaller, or remaining stable.
zero_threshold = 0.01

# Max iterations of the complex function to determine each point's stability/instability
maxitr  = 100


###############################################################################

# Set up the graphics window.

# Create graphics window
win = GraphWin(sys.argv[0], width, height, autoflush=False)

win.setBackground("black")

# Set the origin to the mid point of the window.
win.setCoords(-width/2, -height/2, width/2, height/2)

# Draw axis lines.
x_axis = Line(Point(-width/2, -y_offset*zoom), Point(width/2, -y_offset*zoom))
y_axis = Line(Point(-x_offset*zoom, -height/2), Point(-x_offset*zoom, height/2))
y_axis.draw(win)
x_axis.draw(win)


###############################################################################


# Generate a set of pixel coordinates to plot.  Mathematically, we will plot
# from about -2 to 2 in each direction, and magnifying the results to the size
# of the graphics window.  "step" can be made 2 here for a much faster but lower
# quality plot, useful for testing.
step = 1
x_vals  = [x for x in range(int(-width/2), int(width/2), step)]
y_vals  = [y for y in range(int(-height/2), int(height/2), step)]


#print("min x", x_vals[0]/zoom + x_offset)
#print("max x", x_vals[-1]/zoom + x_offset)

#print("min y", y_vals[0]/zoom + y_offset)
#print("max y", y_vals[-1]/zoom + y_offset)

print("Type:", f"Type: Julia, c = {c}" if julia else "Mandlebrot")
print("zoom factor", zoom)



###############################################################################
# Plot the fractal

most_iterations = 0

# Loop through all pixels in the complex plane, iterate on each with the 
# fractal function, check for stability/instability, tendancy towards zero
# or infinity.

for disp_y in y_vals:

   # Convert displayed y coordinate (and later x) into a proportional number
   # in the range of interest, (ie. about -2 to 2, usually).  Achieve this by 
   # dividing by the zoom factor.   Allow a preset offset, too.
   # Do this outside the x loop for slight optimization.
   y = disp_y/zoom + y_offset


   for disp_x in x_vals:


      # Convert displayed x coordinate into a corresponding point within
      # the complex plain of interest
      x = disp_x/zoom + x_offset

      stable = True
      z = complex(x,y)

      # For julia sets, c is the same for all points in the plane.  For 
      # Mandlebrot, c follows z.
      if not julia:
         c = z
      
      # Put the initial complex point through successive iterations of the
      # series equation.
      iterations = iterate(maxitr, z, c=c)

      # Keep track of the largest number of iterations needed to make any
      # complex argument unstable.
      if iterations > most_iterations:
         most_iterations = iterations

   # Update the window for every horizontal line drawn, so that plotting 
   # progress can be seen by the user.
   win.update()


print("most iterations", most_iterations)
print("Done\n")


# Retain the image on screen, and print coordinates at which the user clicks
# the mouse.  This information is useful for feeding back into the editable
# settings, to subsequent more nteresting plots, "browse" the set or hunt
# for well known features.

print("Click the mouse for information on a point, or ctrl-c to end\n")


while True:
   pt = win.getMouse() # Pause to view result
   x_pixel = pt.getX()
   y_pixel = pt.getY()
   x = x_pixel/zoom + x_offset
   y = y_pixel/zoom + y_offset
   print("x_offset =", x)
   print("y_offset =", y)
   # For testing
   #print("x_pixel", x_pixel)
   #print("y_pixel", y_pixel)
   print()



win.close()






