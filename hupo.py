import numpy as np
import matplotlib.pyplot as plt

fig, axes = plt.subplots(1,2)

x = np.arange(0.0, 2.0, 0.02)
y1 = np.sin(2*np.pi*x)
y2 = np.exp(-x)
l1, = axes[0].plot(x, y1, 'rs-', label='line1')
l2, = axes[0].plot(x, y2, 'go' , label = 'line2')

y3 = np.sin(4*np.pi*x)
y4 = np.exp(-2*x)
l3, l4 = axes[1].plot(x, y3, 'yd-', x, y4, 'k^')

#fig.legend((l1, l2), ('Line 1', 'Line 2'), 'upper left')
print(type(l1))