from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER, DEAD_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.ofproto import ofproto_v1_3_parser
import ryu.ofproto.ofproto_v1_3_parser as ofparser
import ryu.ofproto.ofproto_v1_3 as ofp
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types
from ryu.topology import event
import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage
from tkinter.ttk import Button
from PIL import Image, ImageTk
import threading
import time
import requests




class TrafficSlicing(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(TrafficSlicing, self).__init__(*args, **kwargs)
        print("TrafficSlicing __init__")
        self.switches = []
        self.datapath_list = []
        self.dp = None
        self.interval = 360
        self.idleTimeout = 30
        self.hardTimeout = 60
        self.boolWindowsOpen = False
        self.boolDeleteFlows = False   
        self.boolFirstTimeOpen = True     
        self.current_scenario = 1
        self.images = []
        self.scale_factor = 3
        self.scenario_names = ["Normal", "Emergency", "Administration + Normal", "Administration + Emergency"]
        self.background_color = "#F7F7F7"

        
        def start(root, interval_entry):
            # close the window so the application can start
            self.interval = int(interval_entry.get())
            print("User chosen Interval: ", self.interval) 
            root.destroy()
            self.boolWindowsOpen = False
            print("windows_Opwn should be TRUE: ", self.boolWindowsOpen)
            time.sleep(2)
            if (self.boolDeleteFlows == True):
                for dp in self.datapath_list:
                    print("deleting all flows for datapath: ", dp.id)
                    self.remove_all_flows_from_sw(dp)
                time.sleep(1)            
                self.boolDeleteFlows = False

 

        def my_function():
            if(self.boolWindowsOpen == False):
              print("windows_Opwn should be FALSE: ", self.boolWindowsOpen)
              create_Window()
            
        
        def deleteFlows():
            print("deleteFlows Function called") 
            self.boolDeleteFlows = True
            print("boolDeleteFlows should be TRUE: ", self.boolDeleteFlows)
        
        def create_Window():
            self.boolWindowsOpen = True
            print("windows_Opwn should be TRUE: ", self.boolWindowsOpen)
            root = tk.Tk()
            
            #root.iconbitmap("images/logos_and_icons/logo.ico")
            ico = Image.open('images/logos_and_icons/logo.ico')
            photo = ImageTk.PhotoImage(ico)
            root.wm_iconphoto(False, photo)
            
            screen_width = root.winfo_screenwidth()  # Width of the screen
            screen_height = root.winfo_screenheight() # Height of the screen
            
            width = screen_width * (3/4) # Width 
            height = screen_height # Height
            
            root.geometry('%dx%d+%d+%d' % (width, height, (screen_width-width)/2, 0))
            
            #root.eval('tk::PlaceWindow . center')
            root.title("On Demand Network Slicing - Sleceted Scenario: ")
            root.configure(background=self.background_color)

            # Use a label as a header
            header = tk.Label(root, text="Select Scenario", font=("Helvetica", 22), bg=self.background_color)
            header.pack(pady=15)

            # Create a frame to contain the buttons
            frame = tk.Frame(root, bg=self.background_color)
            frame.pack(pady=10)

            # Create the buttons with a different font and padding
            normal_button = tk.Button(frame, text="Normal",  font=("Helvetica", 16), padx=20, pady=10, command=lambda: [self.select_case(1), update_interface()])
            normal_button.pack(side=tk.LEFT)

            emergency_button = tk.Button(frame, text="Emergency", font=("Helvetica", 16), padx=20, pady=10, command=lambda: [self.select_case(2), update_interface()])
            emergency_button.pack(side=tk.LEFT)

            administration_normal_button = tk.Button(frame, text="Admin + Normal", font=("Helvetica", 16), padx=20, pady=10, command=lambda: [self.select_case(3), update_interface()])
            administration_normal_button.pack(side=tk.LEFT)

            administration_emergency_button = tk.Button(frame, text="Admin + Emergency", font=("Helvetica", 16), padx=20, pady=10, command=lambda: [self.select_case(4), update_interface()])
            administration_emergency_button.pack(side=tk.LEFT)

            # Create a frame to contain the images
            images_frame = tk.Frame(root, bg=self.background_color)
            images_frame.pack(pady=15)

            # Create a button (LEFT) to navigate between the images
            back_button = tk.Button(images_frame, text="<", font=("Helvetica", 18), bg=self.background_color, command=lambda: [self.previous_scenario(image_label), update_interface()])
            back_button.pack(side=tk.LEFT)
            
            # Create a label to display the images
            image_label = tk.Label(images_frame, bg=self.background_color)
            image_label.pack(side=tk.LEFT, padx=15)

            # Load the images
            self.images = [
                PhotoImage(file="images/scenario1/Normal_Scenario.png").subsample(self.scale_factor),
                PhotoImage(file="images/scenario2/Emergency_Scenario.png").subsample(self.scale_factor),
                PhotoImage(file="images/scenario3/Administration_Scenario.png").subsample(self.scale_factor),
                PhotoImage(file="images/scenario4/Administration_with_Emergency_Scenario.png").subsample(self.scale_factor)
            ] 

            # Show the first image
            self.show_image(image_label, 0)

            # Create a button (RIGHT) to navigate between the images
            forward_button = tk.Button(images_frame, text=">", font=("Helvetica", 18), bg=self.background_color, command=lambda: [self.next_scenario(image_label), update_interface()])
            forward_button.pack(side=tk.LEFT, padx=20)

            # Create a label to display the current scenario
            #current_scenario_label = tk.Label(root, text="Current Scenario: Normal", font=("Helvetica", 12), bg=self.background_color)
            #current_scenario_label.pack(pady=5)

            # Use a label and entry for the interval
            interval_frame = tk.Frame(root, bg=self.background_color)
            interval_frame.pack(pady=5)

            interval_label = tk.Label(interval_frame, text="Interval (seconds) for next GUI WINDOW:", font=("Helvetica", 12), bg=self.background_color)
            interval_label.pack(side=tk.LEFT)
            interval_entry = tk.Entry(interval_frame, font=("Helvetica", 12), width=10)
            interval_entry.insert(0, "60")
            interval_entry.pack(side=tk.LEFT, padx=5)

            # Use a button to delete flows
            delete_button = tk.Button(root, text="Delete Flows", font=("Helvetica", 14), command=lambda: deleteFlows())
            delete_button.pack(pady=5)
            
            #Disable the delete button only for the first time
            if(self.boolFirstTimeOpen == True):
                delete_button.config(state="disabled")
                self.boolFirstTimeOpen = False

            # Use a button to start
            start_button = tk.Button(root, text="Start", font=("Helvetica", 14), command=lambda: start(root, interval_entry))
            start_button.pack(pady=5)

            # Use a label to display the selected scenario
            selected_scenario_label = tk.Label(root, text="Selected Scenario: ", font=("Helvetica", 10), bg=self.background_color)
            selected_scenario_label.pack(pady=5)

            # Function to update the selected scenario label
            def update_selected_scenario_label():
                selected_scenario_label.config(text="Selected Scenario: " + self.scenario_names[self.current_scenario - 1])

            # Create a function to update the interface with the selected scenario
            def update_interface():
                # Update the selected scenario label
                update_selected_scenario_label()

                # Show the correct image
                self.show_image(image_label, self.current_scenario)
                
                # select the correct case to update the self.slice_to_port
                self.select_case(self.current_scenario)

                # Disable the back button if we're on the first scenario
                if self.current_scenario == 1:
                    back_button.config(state=tk.DISABLED)
                else:
                    back_button.config(state=tk.NORMAL)

                # Disable the forward button if we're on the last scenario
                if self.current_scenario == len(self.images):
                    forward_button.config(state=tk.DISABLED)
                else:
                    forward_button.config(state=tk.NORMAL)
                
                #Disable the current selectd scenario button
                buttons = [normal_button, emergency_button, administration_normal_button, administration_emergency_button]
                for i in range(4):
                    if i == self.current_scenario - 1:
                        buttons[i].config(state=tk.DISABLED)
                    else:
                        buttons[i].config(state=tk.NORMAL)

                # Update the window title with the selected scenario
                root.title("On Demand Network Slicing - Selected Scenario: " + self.scenario_names[self.current_scenario - 1])

            # Call the function to update the interface with the initial scenario
            update_interface()

            # Confirm with the user before quitting the window
            def on_closing():
                if messagebox.askokcancel("Quit", "Do you want to quit?"):
                    root.destroy()
                    self.boolWindowsOpen = False
                    print("windows_Open should be False: ", self.boolWindowsOpen)

            root.protocol("WM_DELETE_WINDOW", on_closing)

            root.mainloop()    
        """
        self.images = [
            PhotoImage(file="images/scenario1.png"),
            PhotoImage(file="images/scenario2.png"),
            PhotoImage(file="images/scenario3.png"),
            PhotoImage(file="images/scenario4.png")
        ] 
        """
        """
        def create_Window():
            self.boolWindowsOpen = True 
            print("windows_Opwn should be TRUE: ", self.boolWindowsOpen)
            root = tk.Tk()
            root.title("Select Case")
            #root.configure(background='white')
            
            #display_frame = tk.Frame(root, bg='white')
            #display_frame.pack(fill=tk.BOTH, expand=True)
            
            # Use a label as a header
            header = tk.Label(root, text="Select Scenario", font=("Helvetica", 16))
            header.pack(pady=10)

        """
        """
            # Create a frame to contain the image
            image_frame = tk.Frame(root)
            image_frame.pack(pady=10)

            if self.current_scenario < len(self.images):
                image_label = tk.Label(image_frame, image=self.images[self.current_scenario])
                image_label.pack(side=tk.LEFT)
            else:
                image_label = tk.Label(image_frame, text="Error: No image available")
                image_label.pack(side=tk.LEFT)
        """
        """
            if self.current_scenario < len(self.images):
                image_label = tk.Label(image_frame, image=self.images[self.current_scenario])
                image_label.grid(row=0, column=0)
            else:
                # Handle the error case where self.current_scenario is out of range
                # You can display an error message or set the self.current_scenario to 0 or to the last element of the list
                image_label = tk.Label(image_frame, text="Error: No image available")
                image_label.grid(row=0, column=0)    
        """
        """
            # Create buttons to navigate between the images
            previous_button = tk.Button(image_frame, text="<", font=("Helvetica", 14), command=lambda: self.previous_scenario(image_frame))
            previous_button.pack(side=tk.LEFT, padx=10)

            next_button = tk.Button(image_frame, text=">", font=("Helvetica", 14), command=lambda: self.next_scenario(image_frame))
            next_button.pack(side=tk.LEFT, padx=10)
        """
        """
            # Create a frame to contain the buttons
            frame = tk.Frame(root, relief=tk.SUNKEN, bd=2)
            frame.pack(pady=10)

            # Create the buttons with a different font and padding
            normal_button = tk.Button(frame, text="Normal", font=("Helvetica", 14), padx=10, command=lambda: self.select_case(1))
            normal_button.pack(side=tk.LEFT, padx=10)

            emergency_button = tk.Button(frame, text="Emergency", font=("Helvetica", 14), padx=10, command=lambda: self.select_case(2))
            emergency_button.pack(side=tk.LEFT, padx=10)

            administration_normal_button = tk.Button(frame, text="Administration + Normal", font=("Helvetica", 14), padx=10, command=lambda: self.select_case(3))
            administration_normal_button.pack(side=tk.LEFT, padx=10)

            administration_emergency_button = tk.Button(frame, text="Administration + Emergency", font=("Helvetica", 14), padx=10, command=lambda: self.select_case(4))
            administration_emergency_button.pack(side=tk.LEFT, padx=10)

            # Create a frame to contain the images
            images_frame = tk.Frame(root)
            images_frame.pack(pady=10)

            # Create a label to display the images
            image_label = tk.Label(images_frame)
            image_label.pack(side=tk.LEFT)

            # Create a button to navigate between the images
            back_button = tk.Button(images_frame, text="<", font=("Helvetica", 14), command=lambda: self.previous_scenario(image_label))
            back_button.pack(side=tk.LEFT, padx=10)

            forward_button = tk.Button(images_frame, text=">", font=("Helvetica", 14), command=lambda: self.next_scenario(image_label))
            forward_button.pack(side=tk.LEFT, padx=10)

        """
            # Load the images            
        """
            self.images = [ImageTk.PhotoImage(Image.open("images/scenario1.png")),
                        ImageTk.PhotoImage(Image.open("images/scenario2.png")),
                        ImageTk.PhotoImage(Image.open("images/scenario3.png")),
                        ImageTk.PhotoImage(Image.open("images/scenario4.png"))]
        """
        """
            self.images = [
                PhotoImage(file="images/scenario1/Normal_Scenario.png").subsample(self.scale_factor),
                PhotoImage(file="images/scenario2/Emergency_Scenario.png").subsample(self.scale_factor),
                PhotoImage(file="images/scenario3/Administration_Scenario.png").subsample(self.scale_factor),
                PhotoImage(file="images/scenario4/Administration_with_Emergency_Scenario.png").subsample(self.scale_factor)
            ] 
            # Show the first image
            self.show_image(image_label, 0)

            # Use a label and entry for the interval
            interval_frame = tk.Frame(root)
            interval_frame.pack(pady=10)

            interval_label = tk.Label(interval_frame, text="Interval (seconds) for next GUI WINDOW:", font=("Helvetica", 14))
            interval_label.pack(side=tk.LEFT)

            interval_entry = tk.Entry(interval_frame, font=("Helvetica", 14), width=10)
            interval_entry.insert(0, "60")
            interval_entry.pack(side=tk.LEFT, padx=10)

            # Use a button to delete flows
            delete_button = tk.Button(root, text="Delete Flows", font=("Helvetica", 14), command=lambda: deleteFlows())
            delete_button.pack(pady=10)

            # Use a button to start
            start_button = tk.Button(root, text="Start", font=("Helvetica", 14), command=lambda: start(root, interval_entry))
            start_button.pack(pady=10)

            # Confirm with the user before quitting the window
            def on_closing():
                if messagebox.askokcancel("Quit", "Do you want to quit?"):
                    root.destroy()
                    self.boolWindowsOpen = False
                    print("windows_Open should be False: ", self.boolWindowsOpen)

            root.protocol("WM_DELETE_WINDOW", on_closing)

            root.mainloop()
        """           
        """
        def create_Window():
            self.boolWindowsOpen = True 
            print("windows_Opwn should be TRUE: ", self.boolWindowsOpen)
            root = tk.Tk()
            root.title("Select Case")

            # Use a label as a header
            header = tk.Label(root, text="Select Scenario", font=("Helvetica", 16))
            header.pack(pady=10)

            # Create a frame to contain the buttons
            frame = tk.Frame(root, relief=tk.SUNKEN, bd=2)
            frame.pack(pady=10)

            # Create the buttons with a different font and padding
            normal_button = tk.Button(frame, text="Normal", font=("Helvetica", 14), padx=10, command=lambda: self.select_case(1))
            normal_button.pack(side=tk.LEFT, padx=10)

            emergency_button = tk.Button(frame, text="Emergency", font=("Helvetica", 14), padx=10, command=lambda: self.select_case(2))
            emergency_button.pack(side=tk.LEFT, padx=10)

            administration_normal_button = tk.Button(frame, text="Administration + Normal", font=("Helvetica", 14), padx=10, command=lambda: self.select_case(3))
            administration_normal_button.pack(side=tk.LEFT, padx=10)

            administration_emergency_button = tk.Button(frame, text="Administration + Emergency", font=("Helvetica", 14), padx=10, command=lambda: self.select_case(4))
            administration_emergency_button.pack(side=tk.LEFT, padx=10)
            
            # Use a label and entry for the interval
            interval_frame = tk.Frame(root)
            interval_frame.pack(pady=10)

            interval_label = tk.Label(interval_frame, text="Interval (seconds) for next GUI WINDOW:", font=("Helvetica", 14))
            interval_label.pack(side=tk.LEFT)

            interval_entry = tk.Entry(interval_frame, font=("Helvetica", 14), width=10)
            interval_entry.insert(0, "60")
            interval_entry.pack(side=tk.LEFT, padx=10)
            
            # Use a button to delete flows
            delete_button = tk.Button(root, text="Delete Flows", font=("Helvetica", 14), command=lambda: deleteFlows())
            delete_button.pack(pady=10)
            
            # Use a button to start
            start_button = tk.Button(root, text="Start", font=("Helvetica", 14), command=lambda: start(root, interval_entry))
            start_button.pack(pady=10)
    
             # Confirm with the user before quitting the window
            def on_closing():
                if messagebox.askokcancel("Quit", "Do you want to quit?"):
                    root.destroy()
                    self.boolWindowsOpen = False
                    print("windows_Opwn should be TRUE: ", self.boolWindowsOpen)

            root.protocol("WM_DELETE_WINDOW", on_closing)

            root.mainloop()
                    
        
        def create_Window():
            self.boolWindowsOpen = True 
            print("windows_Opwn should be TRUE: ", self.boolWindowsOpen)
            root = tk.Tk()
            root.title("Select Case")

            frame = tk.Frame(root)
            frame.pack()

            normal_button = tk.Button(frame, text="Normal", command=lambda: self.select_case(1))
            normal_button.pack(side=tk.LEFT)

            emergency_button = tk.Button(frame, text="Emergency", command=lambda: self.select_case(2))
            emergency_button.pack(side=tk.LEFT)

            administration_normal_button = tk.Button(frame, text="Administration + Normal", command=lambda: self.select_case(3))
            administration_normal_button.pack(side=tk.LEFT)

            administration_emergency_button = tk.Button(frame, text="Administration + Emergency", command=lambda: self.select_case(4))
            administration_emergency_button.pack(side=tk.LEFT)
            
            interval_label = tk.Label(root, text="Interval (seconds) for next GUI WINDOW:")
            interval_label.pack()

            
            delete_button = tk.Button(root, text="Delete Flows", command=lambda: deleteFlows())
            delete_button.pack()
            
            interval_entry = tk.Entry(root)
            interval_entry.insert(0, "60")
            interval_entry.pack()
            
            start_button = tk.Button(root, text="Start", command=lambda: start(root, interval_entry))
            start_button.pack()
            
            def on_closing():
                if messagebox.askokcancel("Quit", "Do you want to quit?"):
                    root.destroy()
                    self.boolWindowsOpen = False
                    print("windows_Opwn should be TRUE: ", self.boolWindowsOpen)

            root.protocol("WM_DELETE_WINDOW", on_closing)

            root.mainloop()
        """
        
        create_Window()
        
        ### The program will wait here until the GUI window is closed
   
        def call_every_interval_seconds():
            print("call my_function from call_every_interval_seconds function")
            my_function()
            # Schedule the next call to this function after self.interval seconds
            timer = threading.Timer(self.interval, call_every_interval_seconds)
            timer.start()

        # Start the first timer to call the function after self.interval seconds
        timer = threading.Timer(self.interval, call_every_interval_seconds)
        timer.start()
        
        
        
            
        #call_every_interval_seconds()
        print("Line 99 before timer")

        
        
    def show_image(self, image_label, index):
        image_label.config(image=self.images[index - 1])
    
    def next_scenario(self, image_label):
        self.current_scenario = (self.current_scenario + 1) #% 5
        self.show_image(image_label, self.current_scenario)
        #image_label.config(image=self.images[self.current_scenario])

    def previous_scenario(self, image_label):
        self.current_scenario = (self.current_scenario - 1) #% 5
        self.show_image(image_label, self.current_scenario)
        #image_label.config(image=self.images[self.current_scenario]) 
       
    def print_slice_to_port(self):
        #print dict self.slice_to_port
        print("slice_to_port: ", self.slice_to_port)

    def normal(self):
        print("normal scenario has been selected")
        self.slice_to_port = {
            1: {1:4, 4:1, 2:5, 5:2, 3:6, 6:3},
            2: {1: 2, 2: 1},
            3: {1: 2, 2: 1},
            4: {1:4, 4:1, 2:5, 5:2, 3:6, 6:3},

        }
        self.print_slice_to_port()

    def emergency(self):
        print("emergency scenario has been selected")
        self.slice_to_port = {
            1: {1:5, 5:1, 2:4, 4:2, 3:6, 6:3},
            2: {1: 2, 2: 1},
            3: {1: 2, 2: 1},
            4: {1:5, 5:1, 2:4, 4:2, 3:6, 6:3},

        }
        self.print_slice_to_port()


    def administration_normal(self):
        print("administration_normal scenario has been selected")
        self.slice_to_port = {
            1: {1:5, 5:1, 2:6, 6:2, 3:4, 4:3},
            4: {2:4, 4:2, 3:5, 5:3, 1:6, 6:1},
            2: {1: 2, 2: 1},
            3: {1: 2, 2: 1},            

        }
        self.print_slice_to_port()


    def administration_emergency(self):
        print("administration_emergency scenario has been selected")
        self.slice_to_port = {
            1: {1:6, 6:1, 2:4, 4:2, 3:5, 5:3},
            4: {1:5, 5:1, 2:6, 6:2, 3:4, 4:3},
            2: {1: 2, 2: 1},
            3: {1: 2, 2: 1},
                    
        }
        self.print_slice_to_port()
            
    def select_case(self, case):
        options = {
            1: self.normal,
            2: self.emergency,
            3: self.administration_normal,
            4: self.administration_emergency
        }
        self.current_scenario = case
        return options.get(case, lambda: print("Invalid option"))()
    



    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # install the table-miss flow entry.
        match = parser.OFPMatch()
        actions = [
            parser.OFPActionOutput(ofproto.OFPP_CONTROLLER, ofproto.OFPCML_NO_BUFFER)
        ]
        self.add_flow(datapath, 0, match, actions, 0, 0)

    def add_flow(self, datapath, priority, match, actions, idleTimeout, hardTimeout):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

         # construct flow_mod message and send it.
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
        mod = parser.OFPFlowMod(
            datapath=datapath, idle_timeout=idleTimeout, hard_timeout=hardTimeout, priority=priority, match=match, instructions=inst
        )
        datapath.send_msg(mod)
        print("Adding flow to switch: ", datapath.id)
        #print("MOD", mod)

    def _send_package(self, msg, datapath, in_port, actions):
        data = None
        ofproto = datapath.ofproto
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        out = datapath.ofproto_parser.OFPPacketOut(
            datapath=datapath,
            buffer_id=msg.buffer_id,
            in_port=in_port,
            actions=actions,
            data=data,
        )
        datapath.send_msg(out)
        print("Sending packet to switch: ", datapath.id)
        #print("message type: ", msg.msg_type)
        #print("OUT", out)

      
    def remove_all_flows_from_sw(self, datapath):
        ofp = datapath.ofproto
        ofp_parser = datapath.ofproto_parser
        
        # Create a match object with no match fields
        match = ofp_parser.OFPMatch()
        
        # Create a flow mod message with command DELETE and match object
        mod = ofp_parser.OFPFlowMod(
            datapath=datapath, command=ofp.OFPFC_DELETE_STRICT,
            out_port=ofp.OFPP_ANY, out_group=ofp.OFPG_ANY,
            priority=1, match=match
        )
        
        # Send the flow mod message to the switch
        datapath.send_msg(mod)
        print("Removing all flows from switch: ", datapath.id)
        print("MOD", mod)
                
    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        in_port = msg.match["in_port"]
        dpid = datapath.id
        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocol(ethernet.ethernet)
        
        if(self.boolDeleteFlows == False and eth.ethertype != ether_types.ETH_TYPE_LLDP):
            
            out_port = self.slice_to_port[dpid][in_port]
            actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]
            match = datapath.ofproto_parser.OFPMatch(in_port=in_port)            

            self.add_flow(datapath, 1, match, actions, self.idleTimeout, self.hardTimeout)
            self._send_package(msg, datapath, in_port, actions)
        
        """
        if(self.boolDeleteFlows):
            print("packet in handler: boolDeleteFlows = True")
            for dp in self.datapath_list:
                print("deleting all flows for datapath: ", dp.id)
                self.remove_all_flows_from_sw(dp)            
            self.boolDeleteFlows = False
        else:
            out_port = self.slice_to_port[dpid][in_port]
            actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]
            match = datapath.ofproto_parser.OFPMatch(in_port=in_port)            

            self.add_flow(datapath, 1, match, actions)
            self._send_package(msg, datapath, in_port, actions)
        """

    @set_ev_cls(ofp_event.EventOFPFlowRemoved, MAIN_DISPATCHER)
    def flow_removed_handler(self, ev):
        print("FLOW REMOVED HANDLER")
        msg = ev.msg
        dp = msg.datapath
        ofp = dp.ofproto
        reason = msg.reason
        if reason == ofp.OFPRR_IDLE_TIMEOUT:
            reason = "idle timeout"
        elif reason == ofp.OFPRR_HARD_TIMEOUT:
            reason = "hard timeout"
        elif reason == ofp.OFPRR_DELETE:
            reason = "manually deleted"
        elif reason == ofp.OFPRR_GROUP_DELETE:
            reason = "group deleted"
        else:
            reason = "unknown"

        print("Flow removed: reason={}, match={}, duration={}, idle_timeout={}, hard_timeout={}, cookie={}, packet_count={}, byte_count={}".format(
            reason, msg.match, msg.duration_sec, msg.idle_timeout, msg.hard_timeout, msg.cookie, msg.packet_count, msg.byte_count))
        
    @set_ev_cls(event.EventSwitchEnter)
    def switch_enter_handler(self, ev):
        switch_dp = ev.switch.dp
        switch_dpid = switch_dp.id
        ofp_parser = switch_dp.ofproto_parser

        self.logger.info(f"Switch has been plugged in PID: {switch_dpid}")

        if switch_dpid not in self.switches:
            self.switches.append(switch_dpid)               
            self.datapath_list.append(switch_dp)
            
