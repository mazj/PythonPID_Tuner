"""
   
   Updated and maintained by destination0b10unknown@gmail.com

   Copyright 2022 destination2unknown
   
 """
import step1
import step2
import step3
import step4
import ClassHolder

import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo

import matplotlib.pyplot as plt
from scipy.optimize import minimize
from scipy import signal
import os
import pandas as pd

def updatefiletext():
    lbl[0]=Label(root, text=rawfile.filename).grid(row=0,column=1,columnspan=5,padx=5,pady=1,sticky="NESW")

def updatemodeltext():    
    
    lbl[1]=tk.Label(root, text="Model Gain:").grid(row=1,column=1,columnspan=2,padx=1,pady=1,sticky=E)
    lbl[2]=tk.Label(root, text="Model TimeConstant (s):").grid(row=2,column=1,columnspan=2,padx=1,pady=1,sticky=E)
    lbl[3]=tk.Label(root, text="Model DeadTime (s):").grid(row=3,column=1,columnspan=2,padx=1,pady=1,sticky=E)
    lbl[4]=tk.Label(root, text=round(ClassHolder.process.mGain,2)).grid(row=1,column=3,padx=1,pady=1,sticky="NESW")
    lbl[5]=tk.Label(root, text=round(ClassHolder.process.mTau,2)).grid(row=2,column=3,padx=1,pady=1,sticky="NESW")
    lbl[6]=tk.Label(root, text=round(ClassHolder.process.mDeadTime,2)).grid(row=3,column=3,padx=1,pady=1,sticky="NESW")
    lbl[7]=tk.Label(root, text="                ").grid(row=4,column=1)
    lbl[8]=tk.Label(root, text="                ").grid(row=4,column=2)
    lbl[9]=tk.Label(root, text="                ").grid(row=4,column=3)
    lbl[10]=tk.Label(root, text="                ").grid(row=4,column=4)
    lbl[11]=tk.Label(root, text="PID Gains").grid(row=5,column=1)
    lbl[12]=tk.Label(root, text="Kp").grid(row=5,column=2,sticky="NESW")
    lbl[13]=tk.Label(root, text="Ki (1/s)").grid(row=5,column=3,sticky="NESW")
    lbl[14]=tk.Label(root, text="Kd (s)").grid(row=5,column=4,sticky="NESW")
    lbl[15]=tk.Label(root, text="CHR Method").grid(row=6,column=1,sticky="NESW")
    lbl[16]=tk.Label(root, text="IMC Method").grid(row=7,column=1,sticky="NESW")
    lbl[17]=tk.Label(root, text="AIMC Method").grid(row=8,column=1,sticky="NESW")
    lbl[18]=tk.Label(root, text=round(ClassHolder.tunefinder.CHRKp,4)).grid(row=6,column=2,padx=4,pady=4,sticky="NESW")
    lbl[19]=tk.Label(root, text=round(ClassHolder.tunefinder.CHRKi,4)).grid(row=6,column=3,padx=4,pady=4,sticky="NESW")
    lbl[20]=tk.Label(root, text=round(ClassHolder.tunefinder.CHRKd,4)).grid(row=6,column=4,padx=4,pady=4,sticky="NESW")
    lbl[21]=tk.Label(root, text=round(ClassHolder.tunefinder.IMCKp,4)).grid(row=7,column=2,padx=4,pady=4,sticky="NESW")
    lbl[22]=tk.Label(root, text=round(ClassHolder.tunefinder.IMCKi,4)).grid(row=7,column=3,padx=4,pady=4,sticky="NESW")
    lbl[23]=tk.Label(root, text=round(ClassHolder.tunefinder.IMCKd,4)).grid(row=7,column=4,padx=4,pady=4,sticky="NESW")
    lbl[24]=tk.Label(root, text=round(ClassHolder.tunefinder.AIMCKp,4)).grid(row=8,column=2,padx=4,pady=4,sticky="NESW")
    lbl[25]=tk.Label(root, text=round(ClassHolder.tunefinder.AIMCKi,4)).grid(row=8,column=3,padx=4,pady=4,sticky="NESW")
    lbl[26]=tk.Label(root, text=round(ClassHolder.tunefinder.AIMCKd,4)).grid(row=8,column=4,padx=4,pady=4,sticky="NESW")
    
    plt.show()

# create the root window
root = tk.Tk()
root.title('PID Tuner Based on a FOPDT Model')
root.resizable(True, True)
root.geometry('550x300')

lbl=[]
for i in range(0,30):
    lbl.append(Label(root,text=""))

rawfile=step1.openfile()
open_button = ttk.Button(
    root,
    text='Step 1: Open CSV File    ',
    command=lambda :[rawfile(),updatefiletext()]    
)
open_button.grid(row=0,column=0,padx=5,pady=4,sticky=E)

step2model=step2.rough_model()
rough_model = ttk.Button(
    root,
    text='Step 2: Estimate Model ',
    command=lambda :[step2model(rawfile.filename),updatemodeltext()]     
)
rough_model.grid(row=1,column=0,padx=5,pady=4,sticky=E)

step3model=step3.fine_model()
refine_button = ttk.Button(
    root,
    text='Step 3: Refine Model     ',
    command=lambda :[step3model.refine(rawfile.filename),updatemodeltext()]    
)
refine_button.grid(row=2,column=0,padx=5,pady=4,sticky=E)

pidsim_button = ttk.Button(
    root,
    text='Step 4: Run PID Sim       ',
    command=lambda :[step4.pidsim()]   
)
pidsim_button.grid(row=3,column=0,padx=5,pady=4,sticky=E)

# run the gui
root.mainloop()
