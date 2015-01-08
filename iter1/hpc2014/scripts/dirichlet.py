import numpy as np
import numpy.random as npr
import matplotlib.pyplot as pl
from matplotlib.colors import Normalize
import matplotlib.colors as mcolors

N = 1000000

def make_colormap(seq):
    """Return a LinearSegmentedColormap
    seq: a sequence of floats and RGB-tuples. The floats should be increasing
    and in the interval (0,1).
    """
    cdict = {
    	'red':	((0.0, 0.0, 0.0),                
                (1.0, 0.97, 0.97)),

        'green': ((0.0, 0.29, 0.29),
                   (1.0, 0.64, 0.64)),

         'blue':  ((0.0, 0.53, 0.53),                   
                   (1.0, 0.11, 0.11))
        }
    return mcolors.LinearSegmentedColormap('CustomMap', cdict)

def plot_dir(alpha):
	d = npr.dirichlet(alpha, N)

	c = np.cos(np.pi/6)
	t = np.array([[-c, -0.5], [c,  -0.5], [0, 1]])

	dt = d.dot(t)	
	h = np.histogram2d(dt[:, 0], dt[:, 1], bins=300)

	sx = []
	sy = []
	sc = []
	msc = np.max(h[0])
	for i, x in enumerate(h[1][:-1]):
		for j, y in enumerate(h[2][:-1]):			
			if h[0][i, j] > 0:
				sx.append(x)
				sy.append(y)
				sc.append(h[0][i, j]/msc)

	c = mcolors.ColorConverter().to_rgb
	rvb = make_colormap([c('red'), c('violet'), 0.33, c('violet'), c('blue'), 0.66, c('blue')])	

	# pl.scatter(sx, sy, c=sc, marker='o', s=5, lw=0, cmap=pl.cm.get_cmap('rainbow'), alpha=0.3)
	pl.scatter(sx, sy, c=sc, marker='o', s=5, lw=0, cmap=rvb, alpha=0.3)

	pl.xlim(-1.0, 1.0)
	pl.ylim(-0.75, 1.25)
	pl.xlabel("$\\alpha={0}$".format(tuple(alpha)), fontsize='large')
	ax = pl.gca()
	ax.set_frame_on(False)
	ax.xaxis.set_ticks([])
	ax.xaxis.set_ticklabels([])
	ax.axes.get_yaxis().set_visible(False)


pl.subplot(2, 2, 1)
plot_dir([1,1,1])
pl.subplot(2, 2, 2)
plot_dir([10,10,10])
pl.subplot(2, 2, 3)
plot_dir([0.8,0.8,0.8])
pl.subplot(2, 2, 4)
plot_dir([1,1,5])

pl.show()
