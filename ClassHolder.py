from scipy.integrate import odeint

class process(object):
    mGain=1.1
    mTau=58.765
    mDeadTime=7.89
    def __init__(self):
        pass

def _clamp(value, limits):
    lower, upper = limits
    if value is None:
        return None
    elif (upper is not None) and (value > upper):
        return upper
    elif (lower is not None) and (value < lower):
        return lower
    return value

class PID(object):
    
    def __init__(
        self,
        Kp=1.0,
        Ki=0.1,
        Kd=0.01,
        setpoint=50,
        output_limits=(0, 100),
   
    ):

        self.Kp, self.Ki, self.Kd = Kp, Ki, Kd
        self.setpoint = setpoint

        self._min_output, self._max_output = 0, 100

        self._proportional = 0
        self._integral = 0
        self._derivative = 0

        self.output_limits = output_limits
        self._last_eD =0
        self._lastCV=0
        self._d_init=0
        
        self.reset()


    def __call__(self,PV=0,SP=0):
            # PID calculations            
            #P term
            e = SP - PV        
            self._proportional = self.Kp * e

            #I Term
            if self._lastCV<100 and self._lastCV >0:        
                self._integral += self.Ki * e

            #D term
            eD=-PV 
            self._derivative = self.Kd*(eD - self._last_eD)
            #init D term 
            if self._d_init==0:
                self._derivative=0
                self._d_init=1
                
            #Controller Output
            CV = self._proportional + self._integral + self._derivative
            CV = _clamp(CV, self.output_limits)

            # update stored data for next iteration
            self._last_eD = eD
            self._lastCV=CV

            return CV
        

    @property
    def components(self):

        return self._proportional, self._integral, self._derivative

    @property
    def tunings(self):

        return self.Kp, self.Ki, self.Kd

    @tunings.setter
    def tunings(self, tunings):        
        self.Kp, self.Ki, self.Kd = tunings
    
    @property
    def output_limits(self): 
        return self._min_output, self._max_output

    @output_limits.setter
    def output_limits(self, limits):
        
        if limits is None:
            self._min_output, self._max_output = 0, 100
            return

        min_output, max_output = limits

        self._min_output = min_output
        self._max_output = max_output

        self._integral = _clamp(self._integral, self.output_limits)
        

    def reset(self):
        #Reset
        self._proportional = 0
        self._integral = 0
        self._derivative = 0
        self._integral = _clamp(self._integral, self.output_limits)
        self._last_eD=0
        self._lastCV=0
        self._last_eD =0
        
class FOPDTModel(object):
    
    def __init__(self, PlantParams, ModelData):
                
        self.t, self.CV= PlantParams
        self.Gain, self.TimeConstant, self.DeadTime, self.Bias = ModelData


    def calc(self,PV,ts):
                       
        if (self.t-self.DeadTime) <= 0:
            um=0
        else:
            um=self.CV[self.t-int(self.DeadTime)]

        dydt = (-(PV-self.Bias) + self.Gain * um)/self.TimeConstant
        return dydt

    def update(self,PV, ts):
        
        y=odeint(self.calc,PV,ts)   

        return y[-1]

class tunefinder(object):
    CHRKp,CHRKi, CHRKd=0.1,0.01,0.001
    IMCKp,IMCKi,IMCKd=0.2,0.02,0.002
    AIMCKp,AIMCKi, AIMCKd=0.3,0.03,0.003

    def __init__(self):
        self.Gain, self.TimeConstant, self.DeadTime = 1.1,55.555,6.66
            
    def calc(self,ModelData):
        self.Gain, self.TimeConstant, self.DeadTime = ModelData
        if (self.TimeConstant<=0):
            self.TimeConstant=1
        if (self.DeadTime<=0):
            self.DeadTime=1
           
        ###############
        #Tuning Methods
        ###############

        #################       
        #CHR Method
        #
        #CHRKp
        num=0.35*self.TimeConstant 
        den=self.Gain*self.DeadTime
        tunefinder.CHRKp=num/den

        #CHRKi
        ti=1.2*self.TimeConstant
        tunefinder.CHRKi=tunefinder.CHRKp/ti

        #CHRKd
        td=0.5*self.DeadTime
        tunefinder.CHRKd=(tunefinder.CHRKp*td)/60
        ################
                
        #IMC_Kp
        lmda=2.1*self.DeadTime
        num= self.TimeConstant+0.5*self.DeadTime
        den=self.Gain*(lmda)
        tunefinder.IMCKp = num/den

        #IMC_Ki
        ti=self.TimeConstant+0.5*self.DeadTime
        tunefinder.IMCKi = tunefinder.IMCKp / ti
    
        #IMC_Kd
        num=self.TimeConstant*self.DeadTime
        den=2*self.TimeConstant+self.DeadTime
        td=num/den
        tunefinder.IMCKd = (td*tunefinder.IMCKp)/60
         
        #################
        #AIMC
        #AIMC Kp
        L=max(0.1*self.TimeConstant,0.8*self.DeadTime)
        tunefinder.AIMCKp=self.TimeConstant/(self.Gain*(self.DeadTime+L))
        
        #AIMC Ki
        ti=self.TimeConstant/(1.03-0.165*(self.DeadTime/self.TimeConstant))
        tunefinder.AIMCKi =tunefinder.AIMCKp/self.TimeConstant

        #AIMC Kd
        tunefinder.AIMCKd=(self.DeadTime/2)/60