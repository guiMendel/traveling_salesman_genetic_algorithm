# import matplotlib.pyplot as plt
# import json
# import time

# x = [1, 2, 1]
# y = [1, 2, 3]

# plt.plot(x, y, color='black', linestyle='dashed', linewidth = 2, marker='o', markerfacecolor='green', markersize=10)
# plt.plot(y, x, color='red', linestyle='dashed', linewidth = 2, marker='o', markerfacecolor='green', markersize=10)
# plt.show()

import time
import numpy
import matplotlib.pyplot as plt


fig = plt.figure( 1 )
ax = fig.add_subplot( 111 )
ax.set_title("My Title")

im = ax.imshow( numpy.zeros( ( 256, 256, 3 ) ) ) # Blank starting image
fig.show()
im.axes.figure.canvas.draw()

tstart = time.time()
for a in range( 100 ):
  data = numpy.random.random( ( 256, 256, 3 ) ) # Random image to display
  ax.set_title( str( a ) )
  im.set_data( data )
  im.axes.figure.canvas.draw()
  time.sleep(0.5)

print ( 'FPS:', 100 / ( time.time() - tstart ) )