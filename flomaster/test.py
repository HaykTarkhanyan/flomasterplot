from flomaster import *
import pandas as pd
import os

df = pd.read_csv(os.path.join('data_samples', 'Iris.csv'))

fig = generate_flomaster_plot(df, x="Species", y="PetalLengthCm", plot_type='Violin', x_axis="ytgfdv")
fig.show()