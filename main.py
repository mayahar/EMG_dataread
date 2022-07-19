import sys
sys.path.append("../")
from tmsi.TMSiSDK.file_readers import Poly5Reader
import numpy as np
import matplotlib.pyplot as plt

data=Poly5Reader("C:/Users/Maya/Python/Hackathon/data/2022/5855471/Muscle Raw.poly5")
reference_elec = [1,6,7]
array = np.delete(data.samples, reference_elec,0)
x = np.divide(np.arange(0,data.num_samples),data.sample_rate)
labels = ["Right Shin","Left Shin","Right Thigh","Left Thigh","Stomach"]


fig, axes = plt.subplots(data.num_channels-len(reference_elec),sharex=True,sharey=True)
for read in range(0,data.num_channels-len(reference_elec)):
    axes[read].plot(x,array[read])
    axes[read].set_title(labels[read])

fig.add_subplot(1, 1, 1, frame_on=False)
plt.tick_params(labelcolor="none", bottom=False, left=False)

plt.xlabel("Time (sec)")
plt.ylabel("Power (mV)")

plt.show()