import ClassHolder
import numpy as np
import matplotlib.pyplot as plt

def runthesim(processmodel,tune):
    #unpack values 
    igain,itau,ideadtime=processmodel
    ikp,iki,ikd = tune

    #Setup data arrays
    SP = np.zeros(len(t)) 
    PV = np.zeros(len(t))
    CV = np.zeros(len(t))
    pterm = np.zeros(len(t))
    iterm = np.zeros(len(t))
    dterm = np.zeros(len(t))
    
    #defaults
    ibias=13.115
    startofstep=10

    #Packup data
    PIDGains=(ikp,iki,ikd)
    ModelData=(igain,itau,ideadtime,ibias)
    PlantParams=(t, CV)

    #PID Instantiation
    pid = ClassHolder.PID(ikp, iki, ikd, SP[0])
    pid.output_limits = (0, 100)
    pid.tunings=(PIDGains)

    #plant Instantiation
    plant=ClassHolder.FOPDTModel(PlantParams, ModelData)

    #Start Value
    PV[0]=ibias+noise[0]
    
    #Loop through timestamps
    for i in t:        
        if i<(len(t)-1):
            if i < startofstep:
                SP[i] = 0 
            elif (i > startofstep and i< rangesize/2):
                SP[i]= 50 
            else:
                SP[i]=40
            #Find current controller output
            CV[i]=pid(PV[i], SP[i])               
            ts = [t[i],t[i+1]]
            #Send step data
            plant.t,plant.CV=i,CV
            #Find calculated PV
            PV[i+1] = plant.update(PV[i],ts)
            PV[i+1]+=noise[i]
            #Limit PV
            if PV[i+1]>100:
                PV[i+1]=100
            if PV[i+1]<ibias:
                PV[i+1]=ibias
            #Store indiv. terms
            pterm[i],iterm[i],dterm[i]=pid.components
        else:
            #cleanup endpoint
            SP[i]=SP[i-1]
            CV[i]=CV[i-1]
            pterm[i]=pterm[i-1]
            iterm[i]=iterm[i-1]
            dterm[i]=dterm[i-1]
        itae = 0 if i < startofstep else itae+(i-startofstep)*abs(SP[i]-PV[i])
            
    #Display itae value    
    itae=(round(itae/len(t),2)) #measure PID performance
    dataout=SP,PV,CV,pterm,iterm,dterm,itae
    return dataout

def pidsim():
    processmodel=ClassHolder.process.mGain,ClassHolder.process.mTau, ClassHolder.process.mDeadTime
    CHRtune=ClassHolder.tunefinder.CHRKp,ClassHolder.tunefinder.CHRKi,ClassHolder.tunefinder.CHRKd
    IMCtune= ClassHolder.tunefinder.IMCKp,ClassHolder.tunefinder.IMCKi,ClassHolder.tunefinder.IMCKd
    AIMCtune=ClassHolder.tunefinder.AIMCKp,ClassHolder.tunefinder.AIMCKi,ClassHolder.tunefinder.AIMCKd

    #store pid data array from simulation
    CHR=runthesim(processmodel,CHRtune)
    IMC=runthesim(processmodel,IMCtune)
    AIMC=runthesim(processmodel,AIMCtune)

    #Unpack the data returned
    CHRSP,CHRPV,CHRCV,CHRpterm,CHRiterm,CHRdterm,CHRitae=CHR
    IMCSP,IMCPV,IMAIMCV,IMCpterm,IMCiterm,IMCdterm,IMCitae=IMC
    AIMCSP,AIMCPV,AIMCCV,AIMCpterm,AIMCiterm,AIMCdterm,AIMCitae=AIMC

    plt.figure()    
    plt.plot(t,CHRSP, color="goldenrod", linewidth=3, label='SP')
    plt.plot(t,CHRPV,color="darkgreen",linewidth=2,label='CHR PV')
    plt.plot(t,IMCPV,color="blue",linewidth=2,label='IMC PV')    
    plt.plot(t,AIMCPV, color="red", linewidth=2, label='AIMC PV')
 
    plt.ylabel('EU')    
    plt.xlabel('Seconds')
    plt.suptitle("PID Tune Comparison")        
    plt.title("CHR ITAE:%s      IMC ITAE:%s      AIMC ITAE:%s" % (CHRitae, IMCitae, AIMCitae),fontsize=10)
    plt.legend(loc='best')
    plt.show()

#EntryPoint
minsize=1800
maxsize=7200

#Find the size of the range needed
if (ClassHolder.process.mDeadTime+ClassHolder.process.mTau)*5 < minsize:
    rangesize = minsize
elif (ClassHolder.process.mDeadTime+ClassHolder.process.mTau)*5 >maxsize:
    rangesize = maxsize
else:
    rangesize = int((ideadtime+itau)*5)

#setup time intervals
t = np.arange(start=0, stop=rangesize, step=1)
#Random Noise between -0.1 and 0.1, same set used for each run. Created once at runtime.
noise= 0.2*np.random.rand(rangesize)
noise-=0.1
#noise=np.zeros(rangesize) #no noise