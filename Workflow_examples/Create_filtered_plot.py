from AGSM.classes import EMG

subject  = EMG()
subject.all_electrodes_plot()

for muscle in subject.labels:
    subject.high_pass_filter(muscle)
subject.high_pass_filter("Stomach",70)
#The filter needed to compensate for hearbits interfering with the signal
subject.all_electrodes_plot()

subject.rms()
subject.all_electrodes_plot()