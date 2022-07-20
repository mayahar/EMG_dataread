from classes import *

subject  = EMG("C:/Users/Maya/Python/EMG_DATAREAD/data/2022/5855471/Muscle Raw.poly5")
#subject.all_electrodes_plot()

for muscle in subject.labels:
    subject.high_pass_filter(muscle)
subject.high_pass_filter("Stomach",70)
#subject.all_electrodes_plot()

subject.rms()
subject.all_electrodes_plot()