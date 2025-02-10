import numpy as np
import pandas as pd

# Ranges
speed = np.linspace(0.5, 3.0, 10)
lum = np.lib(1, 5, 10)

# All combos of speed and luminance
speed_in, lum_in = np.meshgrid(speed, lum)
speed_in = speed_in.flatten()
lum_in = lum_in.flatten()

# Define Outputs
A_step = 0.03 + 0.01 * speed_in - 0.002 * lum_in
B_step = 0.02 + 0.008 * lum_in + 0.005 * speed_in

data = {'Speed Input': speed_in,
        'Luminance Input': lum_in,
        'A-step': A_step,
        'B-step': B_step,
}

df = pd.DataFrame(data)
print(df.head())

df.to_csv('rotation_dataset.csv', index=False)