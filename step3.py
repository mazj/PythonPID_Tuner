"""
   
   Updated and maintained by destination0b10unknown@gmail.com

   Copyright 2022 destination2unknown
   
 """
import pandas as pd
from scipy import signal
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import ClassHolder
import numpy as np

class fine_model(object):
    def __init__(self):
        pass

    def refine(self,filename):
        #Read File 
        df = pd.read_csv(filename, sep=';')

        #Find CV and PV Columns
        CV_cols = [col for col in df.columns if 'CV' in col.upper()]
        PV_cols = [col for col in df.columns if 'PV' in col.upper()]
        df['CV'] = df[CV_cols[0]]
        df['PV'] = df[PV_cols[0]]

        #Find Step Size
        CVStep=df['CV'].max()-df['CV'].min()
        indexofstart=int(df['CV'].idxmax()/10) #start of step
        bias=df['PV'].iloc[int(indexofstart/2):indexofstart:1].mean(axis = 0)

        #Model
        def fopdt_func(t_fopdt, K=1, tau=1, deadtime=0):
            deadtime = max(0,deadtime)
            tau = max(0,tau)
            return np.array([K*(1-np.exp(-(t_fopdt-deadtime)/tau)) if t_fopdt >= deadtime else 0 for t_fopdt in t_fopdt])

        #Difference between model and actual
        def err(Xe,te,ye):
            Ke,tau,DeadTime = Xe
            z = CVStep*fopdt_func(te,Ke,tau,DeadTime)+bias
            iae = sum(abs(z-ye))*(max(te)-min(te))/len(te)
            return iae

        #Trim Timescale
        actualPV=df['PV'].iloc[(indexofstart*10)-1::10].reset_index(drop=True)
        actualCV=df['CV'].iloc[(indexofstart*10)-1::10].reset_index(drop=True)
        t=actualPV.index.values

        #Model Starting Point
        ModelValues = ClassHolder.process.mGain,ClassHolder.process.mTau, ClassHolder.process.mDeadTime

        #minimize difference between model and actual
        bounds = [(None, None), (0, None), (0,None)]
        Gain,Tau,DeadTime = minimize(err,ModelValues,args=(t, actualPV.values),bounds=bounds, method='Nelder-Mead').x

        #Update holder class
        ClassHolder.process.mGain,ClassHolder.process.mTau, ClassHolder.process.mDeadTime=Gain,Tau,DeadTime

        #Get data to plot new model 
        ymodel=CVStep*fopdt_func(t,ClassHolder.process.mGain,ClassHolder.process.mTau, ClassHolder.process.mDeadTime)+bias
        
        #Plot
        plt.figure()
        plt.plot(actualPV,color="blue",linewidth=3,label='Actual Data')
        plt.plot(actualCV,color="green",linewidth=3,label='Step')
        plt.plot(ymodel,color="red",linewidth=3,label='Model')
        plt.xlabel('Seconds')
        plt.ylabel('Engineering Units')
        plt.suptitle('Refined Model v Actual Data')
        plt.title(f"ModelGain: {round(ClassHolder.process.mGain,2)}   ModelTc: {round(ClassHolder.process.mTau,2)}   ModelDT: {round(ClassHolder.process.mDeadTime,2)}")
        plt.legend(loc='best')

        #Update model details and find tune values
        finemodel=ClassHolder.process.mGain,ClassHolder.process.mTau, ClassHolder.process.mDeadTime
        tuner=ClassHolder.tunefinder()
        tuner.calc(finemodel) #tunefinder
