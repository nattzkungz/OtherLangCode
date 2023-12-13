import matplotlib.pyplot as plt
import pandas as pd

# Read the data from the csv file
data = pd.read_excel('/Users/thanakrittr/Downloads/vibrPrj.xlsx', sheet_name='XL 2', usecols='<varying')
df = data.iloc[<start>:<stop>]
x_axis = df.iloc[:, 0]
y_axis = df.iloc[:, 1]

xData = [_ for _ in x_axis]
yData = [_ for _ in y_axis]

plt.plot(xData, yData, 'r', color='blue')
plt.xlabel('Time (s), Start @ <starting point>')
plt.ylabel('Amplitude')
plt.title('Experiment (kd = 0.05, kp = 1)', fontweight='bold')
plt.show()
