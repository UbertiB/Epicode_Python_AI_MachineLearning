
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import seaborn as sns
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D


matrix=np.random.rand(5,5)
plt.figure(figsize=(6,5))
sns.heatmap(matrix,annot=True,cmap="coolwarm",center=0.5)
plt.title("Heatmap con colormap avanzata")
plt.show()

x=np.linspace(-5,5,50)
y=np.linspace(-5,5,50)
X,Y=np.meshgrid(x,y)
Z=np.sin(np.sqrt(X**2+Y**2))

fig=plt.figure(figsize=(7,11))
ax=fig.add_subplot(111,projection="3d")
surf=ax.plot_surface(X,Y,Z,cmap="viridis")
fig.colorbar(surf)
plt.title("Superficie 3D")
plt.show()

