# PythonPID_Tuner



Step 1: Takes a Process Reaction Curve in csv format - assumes data at 100ms interval (column names CV and PV)

Step 2: Makes a rough estimate for a FOPDT model and calculates Tuning values

Step 3: Trys to refine the model to minimize the error between the model and the actual data, and re-calculates Tuning values

Step 4: Runs a PID Simulation with the three sets of tuning parameters against the model 

Note: 

Kd is turned down due to the effect the D-Term can have in a noisy system

Tuning methods are readily avaliable online 

	

![Step0](https://user-images.githubusercontent.com/92536730/148578341-e6574036-1f94-4b2c-ad7a-79c428ca9a41.JPG)


![Step1](https://user-images.githubusercontent.com/92536730/148578368-5b86cdeb-3bce-469c-8304-ee2eb0b81783.JPG)


![Step2](https://user-images.githubusercontent.com/92536730/148644015-785abf6a-2961-4181-a32d-e776b3940ff2.jpg)


![Step3](https://user-images.githubusercontent.com/92536730/148644018-53b9a6e0-ceda-466b-88ee-265f975caca8.JPG)


![Step4](https://user-images.githubusercontent.com/92536730/148644020-0cf9129d-d142-44a4-95f8-52f248dca1cf.JPG)
