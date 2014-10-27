import numpy as np
import pylab as pl

N = 440
M = 6

def main():
	print "Customers data set plots"
	x, y = read_data("customers.csv", N, M)
	fig = pl.gcf()
	fig.set_size_inches(20, 20)
	for k in xrange(M):
		for l in xrange(k, M):
			ax = pl.subplot(M, M, k * M + l + 1)
			pl.scatter(x[:, k], x[:, l], s=5, c=map(lambda c: ["r", "g", "b"][c - 1], y), linewidths=0)
			ax.set_xticklabels([])
			ax.set_yticklabels([])
	# pl.show()
	pl.savefig('cfig.png', dpi=100)


def read_data(cust_path, n=178, m=13):
	print "Reading data from %s" % cust_path
	x = np.zeros((n, m))
	y = np.zeros(n, dtype=int)	
	with open(cust_path) as cust_file:
		i = 0
		for line in cust_file:
			parts = line.strip().split(",")
			y[i] = int(parts[1])
			x[i] = map(lambda p: float(p), parts[2:])
			i += 1
	return np.log1p(x), y

if __name__ == '__main__':
	main()	
