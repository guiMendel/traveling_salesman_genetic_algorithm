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
from random import random

x_values = [1, 2, 3]
y_values = [1, 2, 3]

fig = plt.figure(figsize=[15, 6])
map = fig.add_subplot(121)
map.set_xticks([])
map.set_yticks([])
map.set_title('Mapa de Rotas')


curve = fig.add_subplot(122)

map.plot(x_values, y_values, color=(random(), random(), random(), 0.5), linestyle='dashed', linewidth=2)
y_values.reverse()
map.plot(x_values, y_values, color=(.1,.1,.1), linestyle='dashed', linewidth=2, alpha=0.3)

curve.set_title('Evolução dos Custos')
curve.plot([20, 19, 16, 16, 13, 11, 10, 9.6, 9.4, 8])

plt.show()

# y = [1, 4, 9, 16, 25,36,49, 64]
# x1 = [1, 16, 30, 42,55, 68, 77,88]
# x2 = [1,6,12,18,28, 40, 52, 65]
# fig = plt.figure()
# ax = fig.add_axes([0,0,1,1])
# l1 = ax.plot(x1,y,'ys-') # solid line with yellow colour and square marker
# l2 = ax.plot(x2,y,'go--') # dash line with green colour and circle marker
# ax.legend(labels = ('tv', 'Smartphone'), loc = 'lower right') # legend placed at lower right
# ax.set_title("Advertisement effect on sales")
# ax.set_xlabel('medium')
# ax.set_ylabel('sales')
# plt.show()