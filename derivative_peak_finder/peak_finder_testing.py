import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
from matplotlib import style
style.use('seaborn')

from derivative_peak_finder import find_peaks


def read_and_format_data(filename):
	with open(filename, 'rb') as file:
		spectrum = file.readlines()

	spectrum = [line.strip() for line in spectrum]
	spectrum = spectrum[20:]
	spectrum = [str(line)[2:-1].split(r'\t') for line in spectrum]

	if True:
		spectrum = [[line[0].replace(',', '.'), line[1]] for line in spectrum]

	return np.array(spectrum).astype(float)


file = 'example_spectrum.txt'
spectrum = read_and_format_data(file)

peaks, smooth_diff_dataset = find_peaks(dataset=spectrum, threshold=250, return_sm_diff_dataset=True)

plt.scatter(peaks[:,0], peaks[:,1], s=30)
plt.plot(spectrum[:,0], spectrum[:,1], linewidth=0.8, color='k')
# plt.plot(smooth_diff_dataset[:,0], smooth_diff_dataset[:,1], linewidth=0.8, color='r')
plt.show()
