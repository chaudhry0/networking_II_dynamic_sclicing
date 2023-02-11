import tkinter as tk
import threading
import subprocess
import ryu_slice

class RyuController(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.start()

    def run(self):
        print("Running function from gui_app")
        subprocess.run(["ryu-manager", "--observe-links", "ryu_slice.py"])

class TrafficSlicingGui(tk.Tk):
    def __init__(self, traffic_slicing_app, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.traffic_slicing_app = traffic_slicing_app
        self.title("Traffic Slicing Application")
        self.geometry("500x500")
        
        self.normal_button = tk.Button(self, text="Normal", command=self.normal)
        self.normal_button.pack()

        self.emergency_button = tk.Button(self, text="Emergency", command=self.emergency)
        self.emergency_button.pack()

        self.administration_normal_button = tk.Button(self, text="Administration Normal", command=self.administration_normal)
        self.administration_normal_button.pack()

        self.administration_emergency_button = tk.Button(self, text="Administration Emergency", command=self.administration_emergency)
        self.administration_emergency_button.pack()
        
        self.stop_button = tk.Button(self, text="Stop", command=self.stop_application)
        self.stop_button.pack()
        
    def normal(self):
        self.traffic_slicing_app.normal()
        #self.start_application()
        
    def emergency(self):
        self.traffic_slicing_app.emergency()
        #self.start_application()
        
    def administration_normal(self):
        self.traffic_slicing_app.administration_normal()
        #self.start_application()
        
    def administration_emergency(self):
        self.traffic_slicing_app.administration_emergency()
        #self.start_application()
        
    def start_application(self):
        print("TrafficSlicingGui start_application")
        self.thread = threading.Thread(target=self.traffic_slicing_app.run)
        self.thread.start()
        
    def stop_application(self):
        print("TrafficSlicingGui stop_application")
        self.traffic_slicing_app.stop()
        self.thread.join()
        
        
def main():
    #traffic_slicing_app = TrafficSlicing()
    #app = TrafficSlicingGui(traffic_slicing_app)
    #app.mainloop()
    print("main")
    ryu_controller = RyuController()
    print("ryu_controller", ryu_controller)
    app = TrafficSlicingGui(ryu_controller)
    print("app", app)
    app.mainloop()

if __name__ == "__main__":
    main()