import sys
sys.path.append("../")
from tmsi.TMSiSDK.file_readers import Poly5Reader
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

class EMG:
    def __init__(self,path=None, labels = ["Right Shin","ref","Left Shin","Right Thigh","Left Thigh","Stomach","ref","ref"]):
        self.data=Poly5Reader(path)
        reference_elec = [i for i, s in enumerate(labels) if "ref" in s]
        if "ref" in labels:           
            self.labels = [value for value in labels if value != "ref"]
        else:
            self.labels = labels
        self.array = np.delete(self.data.samples, reference_elec,0)
        self.time_axis = np.divide(np.arange(0,self.data.num_samples),self.data.sample_rate)
    
    def high_pass_filter(self,muscle,filter=10,order=5):
        elec = list(self.labels).index(muscle)
        feq = self.data.sample_rate
        cutoff = filter/(0.5*feq)
        b, a = signal.butter(order, cutoff, btype = "high", analog = False)
        y = signal.filtfilt(b, a, self.array[elec])

        self.array[elec] = y

    def rms(self,width=20):
        for muscle in self.labels:
            elec = list(self.labels).index(muscle)
            mat = np.reshape(self.array[elec],(self.data.num_samples//width,width))
            for row in range(0,self.data.num_samples//width):
                mat[row] = np.sqrt(mat[row].dot(mat[row])/mat[row].size)
            self.array[elec] = np.reshape(mat,(1,self.data.num_samples))
    
    def all_electrodes_plot(self,array=None):
        if array == None:
            array = self.array        
        x = self.time_axis
        fig, axes = plt.subplots(np.size(self.labels),sharex=True,sharey=True)
        for read in range(0,np.size(self.labels)):
            axes[read].plot(x,array[read])
            axes[read].set_title(self.labels[read])

        fig.add_subplot(1, 1, 1, frame_on=False)
        plt.tick_params(labelcolor="none", bottom=False, left=False)

        plt.xlabel("Time (sec)")
        plt.ylabel("Power (mV)")

        plt.show() 