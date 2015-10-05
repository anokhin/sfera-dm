import matplotlib.pyplot as plt
import sklearn.datasets as sd
import numpy as np
import sklearn.cluster as sc

if __name__ == "__main__":
	plt.figure(figsize=(10, 8))
	# plt.subplots_adjust(bottom=.05, top=.9, left=.05, right=.95)

	plt.subplot(221)
	plt.title("2 clusters")
	X1, Y1 = sd.make_blobs(n_samples=1000, n_features=2, centers=2, cluster_std=2.5, random_state=42)
	y = sc.KMeans(2).fit_predict(X1)
	plt.scatter(X1[:, 0], X1[:, 1], marker='o', c=y, lw=1)
	plt.xticks([])
	plt.yticks([])
	
	plt.subplot(222)
	plt.title("10 clusters")	
	X1, Y1 = sd.make_blobs(n_samples=200, n_features=2, centers=10, cluster_std=1.0, random_state=42)
	y = sc.KMeans(8).fit_predict(X1)
	plt.scatter(X1[:, 0], X1[:, 1], marker='o', c=y, lw=1)
	plt.xticks([])
	plt.yticks([])

	plt.subplot(223)
	plt.title("Rectangles")
	x1, y1 = np.random.randint(0, 1000, 200), np.random.randint(0, 40, 200)
	x2, y2 = np.random.randint(0, 600, 150), np.random.randint(60, 100, 150)
	x3, y3 = np.random.randint(800, 1100, 40), np.random.randint(70, 90, 40)
	z = np.zeros((200 + 150 + 40, 2))
	z[:200, 0], z[:200, 1] = x1, y1
	z[200:350, 0], z[200:350, 1] = x2, y2
	z[350:, 0], z[350:, 1] = x3, y3
	y = sc.KMeans(2).fit_predict(z)
	plt.scatter(z[:, 0], z[:, 1], marker='o', c=y, lw=1)
	plt.xticks([])
	plt.yticks([])

	plt.subplot(224)
	plt.title("Concentric circles")
	x1, y1 = np.random.random_sample(1000)*2*3.1415, np.random.randint(100, 150, 1000)
	x2, y2 = np.random.random_sample(200)*2*3.1415, np.random.randint(0, 50, 200)
	z = np.zeros((1200, 2), dtype=float)
	z[:1000, 0], z[:1000, 1] = x1, y1
	z[1000:, 0], z[1000:, 1] = x2, y2
	
	z1 = np.zeros((1200, 2))
	z1[:, 0], z1[:, 1] = z[:, 1] * np.cos(z[:, 0]), z[:, 1] * np.sin(z[:, 0])
	y = sc.KMeans(2).fit_predict(z1)
	plt.scatter(z1[:, 0], z1[:, 1], marker='o', c=y, lw=1)
	plt.xticks([])
	plt.yticks([])	

	plt.show()