from flomaster import *
import pandas as pd
import os


df = pd.read_csv(os.path.join('data_samples', 'Iris.csv'))

fig = generate_flomaster_plot(df, x="PetalWidthCm", y="PetalLengthCm", plot_type='Distplot', x_axis="flower")
fig.show()