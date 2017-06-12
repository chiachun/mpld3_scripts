import pandas as pd
import math
from pythonds.graphs import Graph

dfin = pd.read_csv('places365_tsne2_n100_pca50.csv',index_col=0)
recs = dfin.T.to_dict().items()
#points = zip(dfin['x0'], dfin['x1'])
#spreads = zip(dfin['sig0'], dfin['sig1'])

w = 7

def distance_square(p1,p2):
    return (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 


def dfs(v,tree):
    if v.getColor() == 'white':
        v.setColor('gray')
        tree.append(v.getId())
        for nextv in v.getConnections():
            if nextv.getColor() == 'white':
                dfs(nextv, tree)
    return tree

# construct graph of overlapping classes
graph = Graph()
labels = []
for _,rec1 in recs:
    for _,rec2 in recs:
 
        x1,y1,sigx1,sigy1 = rec1['x0'], rec1['x1'], rec1['sig0'], rec1['sig1']
        x2,y2,sigx2,sigy2 = rec2['x0'], rec2['x1'], rec2['sig0'], rec2['sig1']
        dx = abs(x2-x1)
        dy = abs(y2-y1)
        sigx = sigx2 + sigx1
        sigy = sigy2 + sigy1
        label1 = rec1['label']
        label2 = rec2['label']
        if dx < w*sigx and dy < w*sigy:
            graph.addEdge( (x1,y1,sigx1,sigy1,label1) , (x2,y2,sigx2,sigy2,label2) )
        elif (x1,y1,sigx1,sigy1,label1) not in graph.getVertices():
            graph.addVertex( (x1,y1,sigx1,sigy1,label1) )


            
for v in graph:
    v.setColor('white')

forest = []
n = 0
for v in graph:
    if v.getColor() == 'white':
        n = n + 1
        tree = []
        tree = dfs(v, tree)
        forest.append(tree)
    



from matplotlib.patches import Ellipse
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from numpy import random as rnd
from matplotlib import colors
import six
#colors_ = colors.ColorConverter.colors.keys()
#colors_.extend(['turquoise','lightgoldenrodyellow','lavender','maroon'])
colors_ = [rnd.rand(3) for i in range(len(forest))]
fig =plt.figure(figsize=(20,20),dpi=1080)
ax = fig.add_subplot(111,aspect='equal')

# merge labels in the same buckets into one label
for i,trees in enumerate(forest):
    color = colors_[i]
    for t in trees:
        avg0, avg1 = t[0], t[1]
        sig0, sig1 = t[2], t[3]
        e = Ellipse(np.array([avg0, avg1]), width=sig0*w*2, height=sig1*w*2)
        e.set_clip_box(ax.bbox)
        e.set_facecolor(color)
   #     e.set_linestyle('')
        e.set_alpha(0.5)
        ax.add_artist(e)
        ax.annotate(t[4], (avg0,avg1), fontsize=5, color=color)
ax.set_xlim(-2,2)
ax.set_ylim(-2,2)
plt.tight_layout()
plt.savefig('tsne_grouping.png')


