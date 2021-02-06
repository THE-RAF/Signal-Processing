from copy import deepcopy

import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import savgol_filter


def differentiate(dataset):
	derivatives = []

	for i in range(1, len(dataset)):
		point = dataset[i]
		dy_dx = (point[1] - dataset[i-1][1]) / (point[0] - dataset[i-1][0])
		derivatives.append(dy_dx)

	derivative_dataset = np.column_stack((dataset[1:][:,0], np.array(derivatives)))

	return derivative_dataset

def get_peak_intervals(smooth_diff_dataset):
	smooth_diff_dataset_xs = smooth_diff_dataset[:,0]
	smooth_diff_dataset_ys = smooth_diff_dataset[:,1]

	peak_intervals = []
	
	max_y = -np.inf
	min_y = np.inf

	for i in range(len(smooth_diff_dataset)):
		y = smooth_diff_dataset_ys[i]

		if y > max_y:
			max_y = y
			max_y_index = i

		else:
			if y < min_y:
				min_y = y
				min_y_index = i

			else:
				if max_y_index < min_y_index:
					peak_intervals.append([max_y_index, min_y_index])
					max_y = -np.inf
					min_y = np.inf

	return peak_intervals

def find_peaks(dataset, threshold, normalize=False, savgol_window=9, savgol_order=1, savgol_iterations=2, return_sm_diff_dataset=False):
	'''
	Dataset format: 2D-np.array
	'''
	
	diff_dataset = differentiate(dataset)

	smooth_diff_dataset = savgol_filter(diff_dataset[:,1], savgol_window, savgol_order)
	
	for iteration in range(savgol_iterations - 1):
		smooth_diff_dataset = savgol_filter(smooth_diff_dataset, savgol_window, savgol_order)

	if return_sm_diff_dataset:
		smooth_diff_dataset_for_plot = deepcopy(smooth_diff_dataset)
		smooth_diff_dataset_for_plot = np.column_stack((diff_dataset[:,0], smooth_diff_dataset_for_plot))

	if normalize:
		smooth_diff_dataset = (smooth_diff_dataset - smooth_diff_dataset.min()) / (smooth_diff_dataset.max() - smooth_diff_dataset.min())

	smooth_diff_dataset = np.column_stack((diff_dataset[:,0], smooth_diff_dataset))

	peak_intervals = get_peak_intervals(smooth_diff_dataset)

	peaks = []

	for interval in peak_intervals:
		if (smooth_diff_dataset[interval[0]][1] - smooth_diff_dataset[interval[1]][1]) > threshold:
			max_y = -np.inf

			for i in range(interval[0]+1, interval[1]+1):
				if dataset[:,1][i] > max_y:
					max_y = dataset[:,1][i]
					max_x = dataset[:,0][i]

			peaks.append([max_x, max_y])

	if return_sm_diff_dataset:
		return np.array(peaks), smooth_diff_dataset_for_plot

	else:
		return np.array(peaks)
