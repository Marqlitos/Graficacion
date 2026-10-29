import numpy as np
from matplotlib import pyplot as plt

def show_3d(vector: np.ndarray) ->None:
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(vector[:,0], vector[:,1], vector[:,2], marker="o", s=100, color= "green")
    ax.set_xlabel("x", fontsize=16)
    ax.set_ylabel("y", fontsize=16)
    ax.set_zlabel("z", fontsize=16)
    plt.show()

if __name__ == "__main__":
    vector = np.random.randint(0, 100, (100, 3))
    show_3d(vector)
    