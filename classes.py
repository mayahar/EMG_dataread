import sys
sys.path.append("../")
from tmsi.TMSiSDK.file_readers import Poly5Reader
import numpy as np
import matplotlib.pyplot as plt

class EMG:
    def __init__(self,path=None,reference_elec = [1,6,7], labels = ["Right Shin","Left Shin","Right Thigh","Left Thigh","Stomach"]):
        self.data=Poly5Reader(path)
        self.reference_elec = reference_elec
        self.labels = labels

    def all_electrodes_plot(self):
        array = np.delete(self.data.samples, self.reference_elec,0)
        x = np.divide(np.arange(0,self.data.num_samples),self.data.sample_rate)
        fig, axes = plt.subplots(self.data.num_channels-len(self.reference_elec),sharex=True,sharey=True)
        for read in range(0,self.data.num_channels-len(self.reference_elec)):
            axes[read].plot(x,array[read])
            axes[read].set_title(self.labels[read])

        fig.add_subplot(1, 1, 1, frame_on=False)
        plt.tick_params(labelcolor="none", bottom=False, left=False)

        plt.xlabel("Time (sec)")
        plt.ylabel("Power (mV)")

        plt.show()