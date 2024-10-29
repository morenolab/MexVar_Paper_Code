import numpy as np
import pandas as pd

df = pd.DataFrame({
    'start': [10, 30, 50, 70],
    'end': [20, 40, 60, 80]
})
pos = 25

# encontrar el índice donde se debe insertar pos para mantener el orden
idx = np.searchsorted(df['start'], pos)

# encontrar el rango más cercano
if idx == 0:
    nearest_range = df.iloc[0]
elif idx == len(df):
    nearest_range = df.iloc[-1]
else:
    # comparar el rango en el índice idx y el índice anterior
    if abs(df.loc[idx, 'start'] - pos) < abs(df.loc[idx-1, 'end'] - pos):
        nearest_range = df.loc[idx]
    else:
        nearest_range = df.loc[idx-1]

print(nearest_range)
