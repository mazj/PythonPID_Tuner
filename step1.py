"""
   
   Updated and maintained by destination0b10unknown@gmail.com

   Copyright 2022 destination2unknown
   
 """
from tkinter import filedialog as fd
import os

class openfile(object):
     def __init__(
        self,
        filepath=os.getcwd(), 
        filename=os.getcwd() + '\PRC.csv',
    ):
        self.filepath=filepath
        self.filename=filename
                
     def __call__(self):
            filetypes = (
                ('CSV files', '*.csv'),
                ('All files', '*.*')
            )
            oldfilename=self.filename
            self.filename= fd.askopenfilename(
                title='Open a file',
                initialdir=self.filepath,
                filetypes=filetypes)
            if self.filename=="":
                self.filename =oldfilename
            self.filepath=os.path.dirname(self.filename)