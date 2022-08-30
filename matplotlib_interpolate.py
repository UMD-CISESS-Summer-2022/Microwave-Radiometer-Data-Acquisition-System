import numpy as np
import scipy.interpolate
import matplotlib.pyplot as plt

def main():
    x = np.array([0, 0, 2, 2])
    y = np.array([0, 2, 0, 2])
    a = np.array([23.4, 23.7, 23.4, 23.7])
    xi, yi = np.mgrid[x.min():x.max():500j, y.min():y.max():500j]

    a_orig = normal_interp(x, y, a, xi, yi)
    a_rescale = rescaled_interp(x, y, a, xi, yi)

    plot(x, y, a, a_orig, 'Not Rescaled')
    plot(x, y, a, a_rescale, 'Rescaled')
    plt.show()

def normal_interp(x, y, a, xi, yi):
    rbf = scipy.interpolate.Rbf(x, y, a)
    ai = rbf(xi, yi)
    return ai

def rescaled_interp(x, y, a, xi, yi):
    a_rescaled = (a - a.min()) / a.ptp()
    ai = normal_interp(x, y, a_rescaled, xi, yi)
    ai = a.ptp() * ai + a.min()
    return ai

def plot(x, y, a, ai, title):
		fig, ax = plt.subplots()
		print(np.shape(ai))
		im = ax.imshow(ai,
                   extent=[x.min(), x.max(), y.min(), y.max()])
    # ax.scatter(x, y, c=a)
		ax.set(xlabel='X', ylabel='Y', title=title)
		fig.colorbar(im)

main()   