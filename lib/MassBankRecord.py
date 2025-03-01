import numpy as np
import os

class MassBankRecord:
  def __init__(self, mz_step):
    self.peaks = []
    self.accession = ''
    self.formula = ''
    self.mz_step = mz_step


  def read(self, text):
    lines = text.split('\n')
    peak_reading = False

    tmp_peaks = []
    intensities = []
    for line in lines:
      if line.startswith('ACCESSION:'):
        self.accession = line.split(':')[1]
      elif line.startswith('CH$FORMULA:'):
        self.formula = line.split(':')[1]
      elif not peak_reading and line.startswith('PK$PEAK:'):
        peak_reading = True
      elif peak_reading and line.startswith('//'):
        peak_reading = False
      if peak_reading:
        tokens = line.strip().split()
        if len(tokens) == 3:
          peak = (float(tokens[0]), int(tokens[2]))
          tmp_peaks.append(peak)
          intensities.append(peak[1])

    for peak in tmp_peaks:
      self.peaks.append((peak[0], peak[1]))


  def get_accession(self):
    return self.accession


  def get_formula(self):
    return self.formula


  def get_dict(self):
    map = {
        'accession': self.accession,
        'formula': self.formula,
    }

    for peak in self.peaks:
      idx = round(peak[0] / self.mz_step)
      key = f'peak_{idx}'
      if key in map:
        map[key] += peak[1]
      else:
        map[key] = peak[1]

    return map
  

  @staticmethod
  def get_records(dir, mz_step):
    records = []

    for root, dirs, files in os.walk(dir):
      for file in files:
        if file.endswith('.txt'):
          path = root + '/' + file
          with open(path, 'r') as f:
            text = f.read()
            record = MassBankRecord(mz_step)
            record.read(text)
            records.append(record)

    return records