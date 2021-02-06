import numpy as np
import random
from matplotlib import pyplot as plt

# fixed bin size
bins = np.arange(-10000, 10000, 100) # fixed bin size

plt.xlim([min(y), max(y)])
plt.title('Distribuição de y (cm)')
plt.xlabel('Y (bin size = 100cm)')
plt.ylabel('contagem')
plt.hist(y, bins=bins, alpha=0.5)
plt.show()