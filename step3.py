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
        i=df['CV'].idxmax() #start of step
        bias=df['PV'].iloc[int(i/2):i:1].mean(axis = 0)

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
        t=df['PV'].index.values

        #Model Starting Point
        #X= K,tau,DeadTime
        ModelValues = ClassHolder.process.mGain,ClassHolder.process.mTau, ClassHolder.process.mDeadTime

        #Every tenth datapoint 100ms to seconds
        t=t[::10]

        #minimize difference between model and actual
        Gain,Tau,DeadTime = minimize(err,ModelValues,args=(t, df['PV'].iloc[::10].reset_index(drop=True))).x

        #Update holder class
        ClassHolder.process.mGain,ClassHolder.process.mTau, ClassHolder.process.mDeadTime=Gain,Tau/10,(DeadTime-i)/10

        #Get data to plot new model 
        ymodel=CVStep*fopdt_func(t/10,ClassHolder.process.mGain,ClassHolder.process.mTau, ClassHolder.process.mDeadTime)+bias
        ymodel=ymodel[:-int(i/10):] #i= start of step

        #Rescale
        plotpv=df['PV'].iloc[i::10].reset_index(drop=True)
        plotcv=df['CV'].iloc[i-1::10].reset_index(drop=True)

        #Plot
        plt.figure()
        plt.plot(plotpv,color="blue",linewidth=3,label='Actual Data')
        plt.plot(plotcv,color="green",linewidth=3,label='Step')
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
