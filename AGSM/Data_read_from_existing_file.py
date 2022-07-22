import sys
sys.path.append("../")
from tmsi.TMSiSDK.file_readers import Poly5Reader
import numpy as np

class Data_read_from_poly5:

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
        
        path: a path to desired poly5 file, when left empty a browsing tab will open
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
