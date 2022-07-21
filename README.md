# EMG_dataread
The following package was created to analyse information recieved from EMGs during AGSM training,
the repository contains TMSi repository, this is necessary to read the relevent files as the package cannot just be installed using pip

![alt text](https://github.com/mayahar/EMG_dataread/blob/main/Workflow_examples\Figure_3.png

Anti-G Straining Maneuver - or AGSM is a technic involving muscle tonus and a breathing technic, 
that in their combination raise the blood presure in the brain, in order to compansate for the higher gravity acceleration.

In days to come this package will also to analyse the breathing part and integrate the two, but not today.

The package works on poly5 or xdf files extracted from an EMG session

the main three modules currently existing are:
1. Data viewer that creates a plot from all electrodes
2. Data filters designated to work with EMG under the AGSM conditions
3. Measurments tools for AGSM technic quality