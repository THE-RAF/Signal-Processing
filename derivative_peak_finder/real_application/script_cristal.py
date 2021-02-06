from spreadsheet_generator import SpreadsheetHandler


'''[Fármaco, Coformador, Tentativa de co-cristal]'''
files = ['CETOMP_3meses.txt', 'SACARINA.txt', 'CET_SMPT_SAC_5.txt']

handler = SpreadsheetHandler(files, tolerance=0.2, peak_threshold=250)
handler.build_spreadsheet()
