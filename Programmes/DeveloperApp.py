import tkinter as tk
from tkinter import ttk
import json
import re
import subprocess


from _Email import send_email
from tkinter import messagebox




class Porn(tk.Tk):
    '''
GUI Class

Args:

    name: str: The name of the window

    size: str: The size of the window
'''

    def __init__(self, name: str, size: str) -> None:

        super().__init__()

        self.title(name)

        if not self._sanitychecker('screen size', size):

            raise ValueError('Invalid screen size')

        self.geometry(size)

    
    # Frames

    def Kiss(self) -> None:
        '''
Creates the first frame.
        '''

        # Destroy the current main frame
        for widget in self.winfo_children():
            widget.destroy()

        seductiveFace = ttk.Frame(self) # Create the first frame

        heading_label = ttk.Label(seductiveFace, text="Welcome", font=("Helvetica", 45)) # Create heading label
        heading_label.pack(pady=20) # Pack the heading label


        # First line buttons

        chest = ttk.Frame(seductiveFace) # Create a frame for first line buttons
        chest.pack(pady=10)

        boob = ttk.Button(chest, text="Maintenance", command=self.BreastLicking_) # Create a button for clearing log files
        boob.pack(side=tk.LEFT, padx=10)

        nipple = ttk.Button(chest, text="Log Files Access", command=self.NippleSucking_) # Create a button for log files access
        nipple.pack(side=tk.LEFT, padx=10)

        belly = ttk.Button(chest, text="Remote Desktop Access", command=self.BellyButton_) # Create a button for remote desktop access
        belly.pack(side=tk.TOP, anchor='center')

        # Second line buttons

        thigh = ttk.Frame(seductiveFace) # Create a frame for second line buttons
        thigh.pack(pady=10)

        ass = ttk.Button(thigh, text="Cleaning", command=self.ButtKiss_) # Create a button to get recommendation on how to free up space
        ass.pack(side=tk.LEFT, padx=10)

        pussy = ttk.Button(thigh, text="Settings", command=self.Oral_) # Create a button for settings
        pussy.pack(side=tk.LEFT, padx=10)

        thigh.pack(side=tk.TOP, anchor='center', pady=30)

        seductiveFace.pack(fill=tk.BOTH, expand=True)


        self.mainloop()


    def BreastLicking_(self):
        '''
Creates a frame to choose which log files must be emptied. 
        '''

        # Destroy the current main frame
        for widget in self.winfo_children():
            widget.destroy()

        chest = ttk.Frame(self)
        boob = ttk.Frame(chest) 
        boob.pack(pady=10)

        # Create heading label for maintenance
        cleavage = ttk.Label(boob, text="Maintenance", font=("Helvetica", 20))
        cleavage.pack(pady=10)

        # Create description label
        breast = ttk.Label(boob, text="Select file(s) you want to empty:")
        breast.pack(pady=5)

        # Create checkboxes
        aeroholeValue = tk.BooleanVar()
        aerohole = ttk.Checkbutton(boob, text="Scripts.log", variable=aeroholeValue)
        aerohole.pack(pady=2)

        nipplesValue = tk.BooleanVar()
        nipples = ttk.Checkbutton(boob, text="transfered.log", variable=nipplesValue)
        nipples.pack(pady=2)

        # Create buttons
        kiss = ttk.Button(boob, text="Back", command=self.Kiss)
        kiss.pack(pady=10)

        lick = ttk.Button(boob, text="Clear", command=lambda: self._BreastLick(aeroholeValue.get(), nipplesValue.get()))
        
        boob.pack(side=tk.TOP, anchor='center', pady=20)

        chest.pack(fill=tk.BOTH, expand=True)


    
    def NippleSucking_(self):
        '''
Creates a frame to send log files.
        '''

        # Destroy the current main frame
        for widget in self.winfo_children():
            widget.destroy()

        boob = ttk.Frame(self)

        # Create heading and instructions
        braless = ttk.Label(boob, text="Log File Access", font=("Helvetica", 20))
        braless.pack(pady=10)

        nipplethroughclothing = ttk.Label(boob, text="Select file(s) you want to send:")
        nipplethroughclothing.pack(pady=5)

        # Checkboxes for log files
        nipplesValues = {}
        logs = ['Scripts.log', 'transfered.log', 'CleanerRecommendation.list']
        for log in logs:
            nipplesValues[log] = tk.BooleanVar()
            ttk.Checkbutton(boob, text=log, variable=nipplesValues[log]).pack(pady=2)

        nipple = ttk.Frame(boob)

        # Buttons for actions
        kiss = ttk.Button(nipple, text="Back", command=self.Kiss)
        kiss.pack(side=tk.LEFT, padx=10, pady=20)
        
        suck = ttk.Button(nipple, text="Send", command=lambda: self._NippleSuck(nipplesValues))
        suck.pack(side=tk.LEFT, padx=10, pady=20)

        nipple.pack(side=tk.TOP, anchor='center', pady=20)

        boob.pack(fill=tk.BOTH, expand=True)
        

    def BellyButton_(self):
        '''
Creates a frame for managing VNC Remote Desktop Access.
        '''

        # Destroy the current main frame
        for widget in self.winfo_children():
            widget.destroy()

        belly = ttk.Frame(self)

        pornstar = ttk.Frame(belly)

        # Create heading and instructions
        stomach = ttk.Label(belly, text="VNC Remote Desktop Access", font=("Helvetica", 20))
        stomach.pack(pady=10)

        info_label = ttk.Label(belly, text="Generate and manage VNC sessions for remote access.")
        info_label.pack(pady=5)

        # Create dynamic button for VNC state
        if self.is_vnc_on(): self.bellybutton = ttk.Button(pornstar, text="Turn off", command=self._Bellybutton)

        else: self.bellybutton = ttk.Button(pornstar, text="Turn on", command=self._Bellybutton)
        self.bellybutton.pack(side=tk.LEFT, pady=20)

        moaning = ttk.Button(pornstar, text="Back", command=self.Kiss)

        moaning.pack(side=tk.LEFT, pady=10)

        pornstar.pack(side=tk.TOP, anchor='center', pady=20)

        belly.pack(fill=tk.BOTH, expand=True)


    def ButtKiss_(self):
        '''
        Creates a frame for recommendation on how to free up space.
        '''

        # Destroy the current main frame
        for widget in self.winfo_children():
            widget.destroy()

        ass = ttk.Frame(self)

        moan = ttk.Frame(ass)

        # Configuration Heading
        cheek = ttk.Label(ass, text="Cleaning Recommendation", font=("Helvetica", 20))
        cheek.pack(pady=10)

        try:
            with open('~/Developer/Softwares/My work/IoT/TorrentialPi/Status_and_Logs/CleanerRecommendation.list', 'r') as file:
                prostate = file.read()
        except FileNotFoundError:
            prostate = "Recommendation list not found."

        # Display the updated recommendations
        asskiss = ttk.Label(ass, text=prostate, font=("Helvetica", 16))
        asskiss.pack(pady=10)

        # Refresh button
        spank = ttk.Button(moan, text="Refresh", command=self._spanking)
        spank.pack(side=tk.LEFT, pady=20)

        fuck = ttk.Button(moan, text="Back", command=self.Kiss)
        fuck.pack(side=tk.LEFT, pady=20)

        moan.pack(side=tk.TOP, anchor='center', pady=20)

        ass.pack(fill=tk.BOTH, expand=True)

    def Oral_(self):
        # Destroy the current main frame
        for widget in self.winfo_children():
            widget.destroy()

        settings_frame = ttk.Frame(self)
        settings_frame.pack(fill=tk.BOTH, expand=True)

        info_label = ttk.Label(settings_frame, text="To edit settings, modify settings.json directly.", font=("Helvetica", 16))
        info_label.pack(pady=20)  # Correctly pack the label

        back_button = ttk.Button(settings_frame, text="Back", command=self.Kiss)
        back_button.pack(pady=10)



    # Helper functions

    def _sanitychecker(self, type: str, value) -> bool:

        match type:

            case 'screen size':

                return bool(re.match(r'\d+x\d+', value))
            
            case _:

                raise ValueError('Invalid object checking type')



    def _BreastLick(self, scripts: bool, transfered: bool) -> None:
        '''
Clears the selected log files.
        '''

        # log files
        scripts_log = '~/Developer/Softwares/My work/IoT/TorrentialPi/Status_and_Logs/Scripts.log'
        transfered_log = '~/Developer/Softwares/My work/IoT/TorrentialPi/Status_and_Logs/transfered.log'

        if messagebox.askyesno("Confirm", f"Are you sure you want to clear these files?"):

            if scripts:

                with open(scripts_log, 'w') as file:

                    file.write('')

                    print('Scripts.log cleared')

            if transfered:

                with open(transfered_log, 'w') as file:

                    file.write('')

                    print('transfered.log cleared')

            messagebox.showinfo("Sucess", "Log files cleared successfully!")




    def _NippleSuck(self, nipplesValue) -> None:
        '''
Sends the selected log files.
        '''

        # log files
        scripts_log = '~/Developer/Softwares/My work/IoT/TorrentialPi/Status_and_Logs/Scripts.log'
        transfered_log = '~/Developer/Softwares/My work/IoT/TorrentialPi/Status_and_Logs/transfered.log'
        cleaner_recommendation = '~/Developer/Softwares/My work/IoT/TorrentialPi/Status_and_Logs/CleanerRecommendation.list'

        # Send the selected log files
        
        nipples = []

        if nipplesValue['Scripts.log'].get():

            nipples.append(scripts_log)

        if nipplesValue['transfered.log'].get():
                
            nipples.append(transfered_log)

        if nipplesValue['CleanerRecommendation.list'].get():
                
            nipples.append(cleaner_recommendation)

        
        
        if len(nipples): 
            
            if messagebox.askyesno("Confirm", f"Are you sure you want to send these files?"):

                #send_email(nipples)

                print('Email sent successfully!')

                messagebox.showinfo("Sucess", "Log files sent successfully!")

    def is_vnc_on(self):
        # Check if VNC service is running
        result = subprocess.run(['systemctl', 'is-active', 'vncserver'], capture_output=True, text=True)
        return result.stdout.strip() == 'active'

    def _Bellybutton(self):
        
        if messagebox.askyesno("Confirm", f"Are you sure you want to turn {'off' if self.is_vnc_on() else 'on'} VNC?"):
        
            if self.is_vnc_on():
                subprocess.run(['systemctl', 'stop', 'vncserver'])
                self.vnc_button.config(text="Turn on" if self.is_vnc_on() else "Turn off")
            else:
                subprocess.run(['systemctl', 'start', 'vncserver'])
                self.vnc_button.config(text="Turn on" if self.is_vnc_on() else "Turn off")

        else: messagebox.showinfo("Cancelled", "VNC operation cancelled.")


    def _spanking(self):
        '''
        Refreshes the cleaning recommendation.
        '''

        subprocess.run(['~/Developer/Softwares/My work/IoT/TorrentialPi/Scripts/CleanerScript.sh'])

        self.ButtKiss_()



app = Porn("Dev app", "600x300")
app.Kiss()
