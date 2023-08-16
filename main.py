import datetime
import threading

import customtkinter as ct

import speedtest

ct.set_appearance_mode("dark")
ct.set_default_color_theme("blue") 

class App(ct.CTk):
   def __init__(self):
      super().__init__()
      self.title("Speed Test")
      self.geometry("500x300")
      self.resizable(0,0,)
      self.initialize_gui()

   def initialize_gui(self):

      self.s = speedtest.Speedtest(secure=True)

      self.progress = ct.CTkProgressBar(self,orientation= "horizontal",determinate_speed= .05,progress_color= "#7b241c")
      self.progress.place(x = 0,y = 200)
      self.progress.set(0)
      self.progress.start()

      self.progress_up = ct.CTkProgressBar(self,orientation= "horizontal",determinate_speed= .05,progress_color= "#7b241c")
      self.progress_up.place(x = 270,y = 200)
      self.progress_up.set(0)
      self.progress_up.start()



      self.label_downspeed = ct.CTkLabel(self,text = "Starting...",font=("Arial",32),text_color= "#7b241c")
      self.label_downspeed.place(x = 0,y = 0)
      
      self.label_upspeed = ct.CTkLabel(self,text = "Starting...",font=("Arial",32),text_color= "#7b241c")
      self.label_upspeed.place(x = 270,y = 0)
      

      self.time_down = threading.Thread(target= self.updated_down)
      self.stop_thread_down = False
      self.time_down.start()

      self.time_up = threading.Thread(target= self.updated_up)
      self.stop_thread_up = False
      self.time_up.start()

      self.protocol("WM_DELETE_WINDOW",lambda: self.stop(None))
      
   def stop(self,event):
      self.stop_thread_up = True
      self.stop_thread_down = True
      self.destroy()


   def updated_up(self):
      while True:
         if self.stop_thread_up:
            break

         upspeed = round((round(self.s.upload()) / 1048576), 2)
         
         self.progress.configure(determinate_speed = 0.1)
         self.progress_up.stop()
         self.progress_up.set(0)
         self.progress_up.start()
         


         self.label_upspeed.configure(text = f"UpSpeed: \n \n{upspeed} Mb/s")

   def updated_down(self):
      while True:
         
         if self.stop_thread_down:
            break
         
         downspeed = round((round(self.s.download()) / 1048576), 2)
         self.progress.configure(determinate_speed = 0.11)
         self.progress.stop()
         self.progress.set(0)
         self.progress.start()
         

         self.label_downspeed.configure(text = f"DownSpeed: \n \n{downspeed} Mb/s")
         
app = App()
app.mainloop()