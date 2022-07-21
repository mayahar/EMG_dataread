import sys
sys.path.append("../")
from tmsi.TMSiSDK.file_readers import Poly5Reader
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal, optimize

class EMG:
    def __init__(self,path=None, labels = ["Right Shin","ref","Left Shin","Right Thigh","Left Thigh","Stomach","ref","ref"]):
        self.data=Poly5Reader(path) #Create a tmsi object
        reference_elec = [i for i, s in enumerate(labels) if "ref" in s]
        if "ref" in labels:           
            self.labels = [value for value in labels if value != "ref"]
            #Remove reference electrodes
        else:
            self.labels = labels
        self.array = np.delete(self.data.samples, reference_elec,0)
        self.time_axis = np.divide(np.arange(0,self.data.num_samples),self.data.sample_rate)
    
    def high_pass_filter(self,muscle,filter=10,order=5):
    #Add high pass filter for selected electrode
        elec = list(self.labels).index(muscle)
        #Select the relevent row based in prefered muscle
        feq = self.data.sample_rate
        cutoff = filter/(0.5*feq)
        b, a = signal.butter(order, cutoff, btype = "high", analog = False)
        y = signal.filtfilt(b, a, self.array[elec])

        self.array[elec] = y

    def rms(self,width=20):
    #Filter and smooth all electrodes by applying rms for selected window
        for muscle in self.labels:
            elec = list(self.labels).index(muscle)
            mat = np.reshape(self.array[elec],(self.data.num_samples//width,width))
            for row in range(0,self.data.num_samples//width):
                mat[row] = np.sqrt(mat[row].dot(mat[row])/mat[row].size)
            self.array[elec] = np.reshape(mat,(1,self.data.num_samples))
    
    def all_electrodes_plot(self):
    #Create a plot that represent all the eletrodes in the array        
        fig, axes = plt.subplots(np.size(self.labels),sharex=True,sharey=True)
        for read in range(0,np.size(self.labels)):
            axes[read].plot(self.time_axis,self.array[read])
            axes[read].set_title(self.labels[read])

        fig.add_subplot(1, 1, 1, frame_on=False)
        plt.tick_params(labelcolor="none", bottom=False, left=False)

        plt.xlabel("Time (sec)")
        plt.ylabel("Power (mV)")

        plt.show()

    def power_applied(self,time_frames,muscle):
    #Time frames shoud be a list of tupels - inital time and period
        elec = list(self.labels).index(muscle)
        powers = []
        relaxation = []
        for trial in time_frames:
            initial = self.time_axis.index(trial[0])
            powers.append(sum(self.array[elec][initial:initial+trial[1]]))
            optimize.curve_fit(self.time_axis[initial:initial+trial[1]],self.array[elec][initial:initial+trial[1]],1)
        return powers,relaxation

    def check_appropriate_power(self,powers,Precentegas=[50,100],error=0.2):
        ratio = powers[0]/powers[1]
        desired_ratio = Precentegas[0]/Precentegas[1]
        if desired_ratio+error>=ratio and desired_ratio-error<=ratio:
            return "Good job!"
        else:
            return "The force applied in the trials did not match the desired G"