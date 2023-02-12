from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER, DEAD_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_0, ofproto_v1_0_parser
from ryu.ofproto import ofproto_v1_3
import ryu.ofproto.ofproto_v1_3_parser as ofparser
from ryu.topology import event
import tkinter as tk
import threading
import time
import requests
from ryu.lib import ofctl_v1_3




class TrafficSlicing(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(TrafficSlicing, self).__init__(*args, **kwargs)
        print("TrafficSlicing __init__")
        self.switches = []
        self.datapath_list = []
        self.dp = None
        self.interval = 5
        self.windowsOpen = False
        
        def start(root, interval_entry):
            # close the window so the application can start
            self.interval = int(interval_entry.get()) 
            root.destroy()
            self.windowsOpen = False
            print("windows_Opwn should be TRUE: ", self.windowsOpen)
 

        def my_function():
            if(self.windowsOpen == False):
              print("windows_Opwn should be FALSE: ", self.windowsOpen)
              create_Window()
            #time.sleep(10)
        
        def delete_all_flows():
            url = "http://localhost:8080/stats/flow/clear"
            response = requests.delete(url)
            if response.status_code == 200:
                print("All flows deleted successfully")
            else:
                print("Failed to delete flows. Response code:", response.status_code) 
                
        def delete_flows(self):
            ofp = self.dp.ofproto
            ofp_parser = self.dp.ofproto_parser
            match = ofparser.OFPMatch()
            instructions = []
            flow_mod = ofparser.OFPFlowMod(self.dp, cookie=0, cookie_mask=0, table_id=0,
                                            command=ofp.OFPFC_DELETE, out_port=ofp.OFPP_ANY,
                                            out_group=ofp.OFPG_ANY, priority=0, buffer_id=0xffffffff,
                                            match=match, instructions=instructions)
            self.dp.send_msg(flow_mod)
            print("Deleting all flows")
        
        def deleteFlows():
            print("deleteFlows")
            #ofctl = ofctl_v1_3.OFCtl13(self.dp)
            #ofctl.remove_table_flow(self.dp, table_id=0)
            print("Deleting all flows")
            print("dp: ", self.dp)
            delete_flows(self)
            #delete_all_flows()
            #for dp in self.datapath_list:                
            #    self.remove_flows(dp,0)  
                    
        
        def create_Window():
            self.windowsOpen = True 
            print("windows_Opwn should be TRUE: ", self.windowsOpen)
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
            interval_entry.pack()
            
            start_button = tk.Button(root, text="Start", command=lambda: start(root, interval_entry))
            start_button.pack()
            

            
            root.mainloop()
        
        #create_Window()
        
        #thread = threading.Thread(target=myThread)
        #thread.start()
        
        def call_every_interval_seconds():
            timer = threading.Timer(self.interval, call_every_interval_seconds)
            timer.start()
            my_function()

        timer = threading.Timer(self.interval, call_every_interval_seconds)
        timer.start()
        
        

       


    def normal(self):
        print("normal scenario has been selected")
        self.slice_to_port = {
            1: {1:4, 4:1, 2:5, 5:2, 3:6, 6:3},
            2: {1: 2, 2: 1},
            3: {1: 2, 2: 1},
            4: {1:4, 4:1, 2:5, 5:2, 3:6, 6:3},

        }

    def emergency(self):
        print("emergency scenario has been selected")
        self.slice_to_port = {
            1: {1:5, 5:1, 2:4, 4:2, 3:6, 6:3},
            2: {1: 2, 2: 1},
            3: {1: 2, 2: 1},
            4: {1:5, 5:1, 2:4, 4:2, 3:6, 6:3},

        }

    def administration_normal(self):
        print("administration_normal scenario has been selected")
        self.slice_to_port = {
            1: {1:5, 5:1, 2:6, 6:2, 3:4, 4:3},
            4: {2:4, 4:2, 3:5, 5:3, 1:6, 6:1},
            2: {1: 2, 2: 1},
            3: {1: 2, 2: 1},            

        }

    def administration_emergency(self):
        print("administration_emergency scenario has been selected")
        self.slice_to_port = {
            1: {1:6, 6:1, 2:4, 4:2, 3:5, 5:3},
            4: {1:5, 5:1, 2:6, 6:2, 3:4, 4:3},
            2: {1: 2, 2: 1},
            3: {1: 2, 2: 1},
                    
        }
            
    def select_case(self, case):
        options = {
            1: self.normal,
            2: self.emergency,
            3: self.administration_normal,
            4: self.administration_emergency
        }
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
        self.add_flow(datapath, 0, match, actions)

    def add_flow(self, datapath, priority, match, actions):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

         # construct flow_mod message and send it.
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
        mod = parser.OFPFlowMod(
            datapath=datapath, priority=priority, match=match, instructions=inst
        )
        datapath.send_msg(mod)

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

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        in_port = msg.match["in_port"]
        dpid = datapath.id

        out_port = self.slice_to_port[dpid][in_port]
        actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]
        match = datapath.ofproto_parser.OFPMatch(in_port=in_port)

        self.add_flow(datapath, 1, match, actions)
        self._send_package(msg, datapath, in_port, actions)

    def remove_flows(self, datapath, table_id):
            """Removing all flow entries."""
            parser = datapath.ofproto_parser
            ofproto = datapath.ofproto
            empty_match = parser.OFPMatch()
            instructions = []
            flow_mod = self.remove_table_flows(datapath, table_id,
                                            empty_match, instructions)
            print ("deleting all flow entries in table ", table_id)
            datapath.send_msg(flow_mod)
        
    def remove_table_flows(self, datapath, table_id, match, instructions):
            """Create OFP flow mod message to remove flows from table."""
            ofproto = datapath.ofproto
            flow_mod = datapath.ofproto_parser.OFPFlowMod(datapath,match,0,ofproto.OFPFC_DELETE,0,0,1,ofproto.OFP_NO_BUFFER,ofproto.OFPP_NONE,0,instructions)
            return flow_mod
        
    @set_ev_cls(event.EventSwitchEnter)
    def switch_enter_handler(self, ev):
        switch_dp = ev.switch.dp
        switch_dpid = switch_dp.id
        ofp_parser = switch_dp.ofproto_parser

        self.logger.info(f"Switch has been plugged in PID: {switch_dpid}")

        if switch_dpid not in self.switches:
            if(switch_dpid == 1 or switch_dpid == 4 ):
                self.switches.append(switch_dpid)               
            self.datapath_list.append(switch_dp)
            
    @set_ev_cls(ofp_event.EventOFPStateChange, [MAIN_DISPATCHER, DEAD_DISPATCHER])
    def state_change_handler(self, ev):
        datapath = ev.datapath
        if ev.state == MAIN_DISPATCHER:
            self.logger.debug('register datapath: %016x', datapath.id)
            print("register datapath: %016x", datapath.id)
            self.dp = datapath
            print("datapath: %016x", self.dp.id)
