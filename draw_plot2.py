from matplotlib.patches import Ellipse
import matplotlib.pyplot as plt
from numpy import random as rnd
fig =plt.figure(figsize=(10,10),dpi=400)
ax = fig.add_subplot(111,aspect='equal')

import pandas as pd
dfin = pd.read_csv('places365_tsne2.csv',index_col=0)
avg0s = dfin['x0'] 
avg1s = dfin['x1']
sig0s = dfin['sig0']
sig1s = dfin['sig1']
colors = [rnd.rand(3) for i in range(len(dfin))]
label_names=dfin.label.tolist()

for i in range(365):
    avg0 = avg0s[i]
    avg1 = avg1s[i]
    sig0 = sig0s[i]
    sig1 = sig1s[i]
    e = Ellipse(np.array([avg0, avg1]), width=sig0*2, height=sig1*2)
    e.set_clip_box(ax.bbox)
    e.set_facecolor(colors[i])
    e.set_alpha(0.5)
    ax.add_artist(e)
    dx = rnd.rand()/10+0.1
    dy = rnd.rand()/10+0.1
    ax.annotate(label_names[i],(avg0+dx,avg1+dy),fontsize=2,color=colors[i])
ax.set_xlim(-15,15)
ax.set_ylim(-20,20)
plt.tight_layout()
plt.savefig('scene_inception5h_tsne2.png')
