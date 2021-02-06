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


class SpreadsheetHandler:
	def __init__(self, files, tolerance=0.2, peak_threshold=250):
		self.files = files
		self.tolerance = tolerance

		self.farm_data = read_and_format_data(files[0])
		self.coform_data = read_and_format_data(files[1])
		self.cocrystal_data = read_and_format_data(files[2])

		self.farm_peaks = find_peaks(dataset=self.farm_data, threshold=peak_threshold)
		self.coform_peaks = find_peaks(dataset=self.coform_data, threshold=peak_threshold)
		self.cocrystal_peaks = find_peaks(dataset=self.cocrystal_data, threshold=peak_threshold)

	def get_all_peaks(self):
		all_detected_peaks = np.sort(list(self.farm_peaks[:,0]) + list(self.coform_peaks[:,0]) + list(self.cocrystal_peaks[:,0]) + [35])
	
		all_true_peaks = []

		current_peak = all_detected_peaks[0]
		for peak_index in range(len(all_detected_peaks)):
			peak = all_detected_peaks[peak_index]

			if peak - current_peak > self.tolerance:
				last_peak = all_detected_peaks[peak_index - 1]
				all_true_peaks.append(current_peak + (last_peak - current_peak) / 2)
				current_peak = all_detected_peaks[peak_index]

		return all_true_peaks

	def build_spreadsheet(self):
		all_peaks = self.get_all_peaks()
		
		spreadsheet = {
		self.files[0][:-4]: ['-' for _ in range(len(all_peaks))],
		self.files[1][:-4]: ['-' for _ in range(len(all_peaks))],
		self.files[2][:-4]: ['-' for _ in range(len(all_peaks))],
		'exclusive_peak': ['-' for _ in range(len(all_peaks))]
		}
		
		peak_lists = [self.farm_peaks, self.coform_peaks, self.cocrystal_peaks]

		for peak_list_index, peak_list in enumerate(peak_lists):
			for peak in peak_list[:,0]:

				for i, estimated_peak in enumerate(all_peaks):
					if abs(estimated_peak - peak) < self.tolerance:
						spreadsheet[self.files[peak_list_index][:-4]][i] = peak
						break

		for i in range(len(all_peaks)):
			farm_peak = spreadsheet[self.files[0][:-4]][i]
			coform_peak = spreadsheet[self.files[1][:-4]][i]
			cocrystal_peak = spreadsheet[self.files[2][:-4]][i]

			if farm_peak == '-' and coform_peak == '-':
				spreadsheet['exclusive_peak'][i] = '***'

				if cocrystal_peak == '-':
					spreadsheet['exclusive_peak'][i] = 'x'

		df = pd.DataFrame(spreadsheet)
		df = df.drop(df[df['exclusive_peak']=='x'].index)
		
		df.to_excel(f'{self.files[0][:-4]}-{self.files[1][:-4]}-{self.files[2][:-4]}.xlsx', index=False)
