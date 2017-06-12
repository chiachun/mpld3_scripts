import numpy as np
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
import glob
import os


image_dir = '/home/chiachun/cave/places365/images'
bottleneck_dir = '/home/chiachun/cave/places365/bottlenecks/'
bottlename = 'avgpool'

label_names = os.listdir(bottleneck_dir+bottlename)


xs = []


nsample = 10
for i in range(365):
    label_name = label_names[i]
    paths = glob.glob('%s/%s/%s/*.txt' % (bottleneck_dir, bottlename,label_name))
    
    for path in paths[:nsample]:
       # print path
        x = np.loadtxt(path,delimiter=',')
        np.expand_dims(x,axis=0)
        xs.append(x)
        
X = np.vstack(xs)

pca = PCA(n_components=50)
pca.fit(X)
xpca = pca.transform(X)

model = TSNE(n_components=2)
xp = model.fit_transform(xpca)

x0s =[]; x1s=[]; 
s0s= []; s1s=[]; 
for i in range(365):
    i1 = i*nsample
    i2 = (i+1)*nsample
    x0 = xp[i1:i2,0].mean()
    x1 = xp[i1:i2,1].mean()
    s0 = xp[i1:i2,0].std()/nsample
    s1 = xp[i1:i2,1].std()/nsample
    x0s.append(x0)
    x1s.append(x1)
    s0s.append(s0)
    s1s.append(s1)

import pandas as pd

df = pd.DataFrame({"label":label_names,
                   "x0":x0s,"x1":x1s,
                   "sig0": s0s, "sig1":s1s})

    

df.to_csv("places365_tsne2_n10_pca50.csv")
