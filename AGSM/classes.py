import sys
sys.path.append("../")
from tmsi.TMSiSDK.file_readers import Poly5Reader
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal, optimize

class EMG:

    """" Creates an object of EMG data recieved from poly5 type file """

    def __init__(
            self,
            labels, 
            path=None):
        """
        Parameters
        ---
        labels: list
            A list that names each of the EMG electrodes by their order
            reference electordes should be named as "ref",
            usually the names will be the names of the muscle or body part the electrode was put on
        """

        self.data=Poly5Reader(path) #Create a tmsi object
        reference_elec = [i for i, s in enumerate(labels) if "ref" in s]
        
        if "ref" in labels:           
            self.labels = [value for value in labels if value != "ref"]
            #Remove reference electrodes
        else:
            self.labels = labels
        self.array = np.delete(self.data.samples, reference_elec,0)
        self.time_axis = np.divide(np.arange(0,self.data.num_samples),self.data.sample_rate)
    
    def high_pass_filter(self,label,filter=10,order=5):
        """
        This function adds a filter to the selected electrode, it changes the data in the object

        Parameters
        ---
        label: str
            A string that is in the labels list, refers to the relevent electride
        filter: int
        order: int
        """
        elec = list(self.labels).index(label)
        #Select the relevent row based in prefered muscle
        feq = self.data.sample_rate
        cutoff = filter/(0.5*feq)
        b, a = signal.butter(order, cutoff, btype = "high", analog = False)
        y = signal.filtfilt(b, a, self.array[elec])

        self.array[elec] = y

    def rms(self,width=20):
        """
        This function is applied on all the electrodes, for each window it replaces its
        values with the rms of the window, it changes the data in the object

        Parameters
        ---
        width: int
            The amount of sampels wanted in each window
        """
        for muscle in self.labels:
            elec = list(self.labels).index(muscle)
            mat = np.reshape(self.array[elec],(self.data.num_samples//width,width))
            for row in range(0,self.data.num_samples//width):
                mat[row] = np.sqrt(mat[row].dot(mat[row])/mat[row].size)
            self.array[elec] = np.reshape(mat,(1,self.data.num_samples))
    
    def all_electrodes_plot(self):
        """
        This function creates a plot that represent all the eletrodes in the array
        """        
        fig, axes = plt.subplots(np.size(self.labels),sharex=True,sharey=True)
        for read in range(0,np.size(self.labels)):
            axes[read].plot(self.time_axis,self.array[read])
            axes[read].set_title(self.labels[read])

        fig.add_subplot(1, 1, 1, frame_on=False)
        plt.tick_params(labelcolor="none", bottom=False, left=False)

        plt.xlabel("Time (sec)")
        plt.ylabel("Power (mV)")

        plt.show()

    def power_applied(self,time_frames,label):
        """
        This function sums the power applied in each trial for specific electrode, 
        it also creates a relexation measurments that showes the level at which the subject
        relexed their muscles during the trial time period

        Parameters
        ---
        time_frame: tuples list
            Each tuple represents a trial, 
            the first element in each tuple should state the strating time of the trial,
            and the second one should state the trial duration, both in seconds
        label: str
            A string that is in the labels list, refers to the relevent electride

        Returns
        ---
        powers: list
            A list of power sum applied in each trial
        relaxation: list
            A list of relaxation levels in each trial
        """
        elec = list(self.labels).index(label)
        powers = []
        relaxation = []
        for trial in time_frames:
            initial = self.time_axis.index(trial[0])
            powers.append(sum(self.array[elec][initial:initial+trial[1]]))
            optimize.curve_fit(self.time_axis[initial:initial+trial[1]],self.array[elec][initial:initial+trial[1]],1)
        return powers,relaxation

    def check_appropriate_power(self,powers,Precentegas=[50,100],error=0.2):
        """
        This function examens wether the force applied in different trials 
        matches in their proportions

        Parameters
        ---
        power: list
            a list of powers applied in each trial, recieved from power_applied function
        precentages: list
            a list of tonus precenteges told the subjects to apply in each trial
        """
        ratio = powers[0]/powers[1]
        desired_ratio = Precentegas[0]/Precentegas[1]
        if desired_ratio+error>=ratio and desired_ratio-error<=ratio:
            return "Good job!"
        else:
            return "The force applied in the trials did not match the desired G"