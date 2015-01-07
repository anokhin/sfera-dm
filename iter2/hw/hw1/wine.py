import numpy as np
import pylab as pl

N = 178
M = 13

def main():
	print "Wine data set plots"
	x, y = read_data("wine.data.txt", N, M)
	fig = pl.gcf()
	fig.set_size_inches(20, 20)
	for k in xrange(M):
		for l in xrange(k, M):
			ax = pl.subplot(M, M, k * M + l + 1)
			pl.scatter(x[:, k], x[:, l], s=5, c=map(lambda c: ["r", "g", "b"][c - 1], y), linewidths=0)
			ax.set_xticklabels([])
			ax.set_yticklabels([])
	# pl.show()
	pl.savefig('wfig.png', dpi=100)


def read_data(wine_path, n=178, m=13):
	print "Reading data from %s" % wine_path
	x = np.zeros((n, m))
	y = np.zeros(n, dtype=int)	
	with open(wine_path) as wine_file:
		i = 0
		for line in wine_file:
			parts = line.strip().split(",")
			y[i] = int(parts[0])
			x[i] = map(lambda p: float(p), parts[1:])
			i += 1
	return x, y

if __name__ == '__main__':
	main()	
