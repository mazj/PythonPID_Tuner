# PythonPID_Tuner



Step 1: Takes a Process Reaction Curve in csv format - assumes data at 100ms interval (column names CV and PV)

Step 2: Makes a rough estimate for a FOPDT model and calculates Tuning values

Step 3: Trys to refine the model to minimize the error between the model and the actual data, and re-calculates Tuning values

Step 4: Runs a PID Simulation with the three sets of tuning parameters against the model 

![Step0](https://user-images.githubusercontent.com/92536730/148578341-e6574036-1f94-4b2c-ad7a-79c428ca9a41.JPG)


![Step1](https://user-images.githubusercontent.com/92536730/148578368-5b86cdeb-3bce-469c-8304-ee2eb0b81783.JPG)


![Step2](https://user-images.githubusercontent.com/92536730/148579011-145fefa0-05c1-46ff-8edf-13a28962557d.jpg)


![step3](https://user-images.githubusercontent.com/92536730/148579023-ddfcec74-3e3e-46ef-9273-46053aea091f.JPG)


![Step4](https://user-images.githubusercontent.com/92536730/148579043-30f1a9dc-c00f-4977-b847-dea3f477d5cf.JPG)

