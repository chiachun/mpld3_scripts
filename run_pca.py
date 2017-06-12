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


nsample = 500
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
xp = pca.transform(X)

