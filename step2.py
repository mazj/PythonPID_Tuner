import pandas as pd
from scipy import signal
import matplotlib.pyplot as plt
import ClassHolder

class rough_model(object):
    def __init__(self):
        pass

    def __call__(self,filename):
        #Calculation Variables
        deltaT=0.1 #assume 100ms interval
        twosecwindow=int(2/deltaT)
        onesecwindow=int(1/deltaT)
        hihilimit=1.05
        lololimit=0.95
        hilimit=1.02
        lowlimit=0.98
        settlingwindow=5
        window=int(settlingwindow/deltaT)
        
        df = pd.read_csv(filename, sep=';')
        
        #Find relevant columns
        CV_cols = [col for col in df.columns if 'CV' in col.upper()]
        PV_cols = [col for col in df.columns if 'PV' in col.upper()]

        #Creat DataFrames
        df['CV'] = df[CV_cols[0]]
        df['PV'] = df[PV_cols[0]]

        #Find basic parameters
        i_start=df[df['CV']!=0].first_valid_index()
        AvgAti=df['PV'].iloc[i_start:i_start+twosecwindow:1].mean(axis = 0)
        StartPV=df['PV'].iloc[i_start]
        InitCV=df['CV'].iloc[0]
        StartCV=df['CV'].iloc[i_start]

        #DeadTime
        RangeU=AvgAti*hihilimit
        RangeL=AvgAti*lololimit
        #Find DeadTime
        for x in range(i_start,(len(df['PV'])-window)):
            if(df['PV'].iloc[x:x+twosecwindow:1].mean(axis = 0)>RangeU):
             ClassHolder.process.mDeadTime=(x-i_start)*deltaT
             break

        #Gain
        j=df['PV'].idxmax()
        max_peak=df['PV'].max()
        max = df['PV'].iloc[j-onesecwindow:j+onesecwindow:1].mean(axis = 0)
        ClassHolder.process.mGain=(max-AvgAti)/(StartCV-InitCV)

        #Time Constant
        tc_value=0.63*(max-AvgAti)+AvgAti
        tc_upp=tc_value*1.01
        tc_low=tc_value*0.99

        #Find Time Constant
        z=df[df['PV']>=(max*0.5)].first_valid_index()                
        for x in range(z,(len(df['PV'])-window)):
            if(df['PV'].iloc[x-twosecwindow:x+twosecwindow:1].mean(axis = 0)>tc_value):
             ClassHolder.process.mTau=((x-i_start)*deltaT)-ClassHolder.process.mDeadTime
             break
            else:
             ClassHolder.process.mTau=-1
                     
        #Find Tune
        roughmodel=ClassHolder.process.mGain,ClassHolder.process.mTau, ClassHolder.process.mDeadTime
        tuner=ClassHolder.tunefinder()
        tuner.calc(roughmodel) #tunefinder
       
        #Setup System Model
        num = [ClassHolder.process.mGain]
        den = [ClassHolder.process.mTau,1]
        sys1 = signal.TransferFunction(num,den)
  
        #Find Step Response based on Rough Model
        t1,y1 = signal.step(sys1, N=int(df['PV'].count()/10))
        t1=t1[::10]
        y1=y1[::10]

        #Rescale
        plotpv=df['PV'].iloc[::10].reset_index(drop=True)
        plotcv=df['CV'].iloc[::10].reset_index(drop=True)

        #plot 
        plt.figure()
        plt.xlim(0,df['PV'].count()*0.11)
        plt.plot(plotpv, color="blue", linewidth=3, label='Actual Data')
        plt.plot(t1+(i_start/10+(ClassHolder.process.mDeadTime)),(StartCV*y1)+AvgAti,color="red",linewidth=3,label='Model')
        plt.plot(plotcv, color="green", linewidth=3, label='Step')
        plt.hlines(AvgAti, 0, i_start/10+ClassHolder.process.mDeadTime,colors='red', linestyles='solid',linewidth=3,label='')
        plt.ylabel('Engineering Units')
        plt.xlabel('Seconds')
        plt.suptitle("Rough Model v Actual Data")
        plt.title(f"ModelGain: {round(ClassHolder.process.mGain,2)}   ModelTc: {round(ClassHolder.process.mTau,2)}   ModelDT: {round(ClassHolder.process.mDeadTime,2)}")
        plt.legend(loc='best')
