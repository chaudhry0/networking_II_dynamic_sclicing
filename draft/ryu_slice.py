from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from tkinter import *
from tkinter import ttk



class TrafficSlicing(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(TrafficSlicing, self).__init__(*args, **kwargs)
        window=Tk()
        # add widgets here
        print ("Inizio")
        frm = ttk.Frame(window, padding=10)
        frm.grid()
        #ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
        #ttk.Button(frm, text="Quit", command=window.destroy).grid(column=0,row=0)
        
        
        
        window.title('Hello Python')
        window.geometry("500x200+10+20")
    
       # ttk.Button(frm, text="Quit", command=window.destroy).grid(column=0,row=3)
        
        #action when click the button b1
        def click1():
            print("NORMAL")
            self.slice_to_port = {
                1: {1:4, 4:1, 2:5, 5:2, 3:6, 6:3},
                2: {1: 2, 2: 1},
                3: {1: 2, 2: 1},
                4: {1:4, 4:1, 2:5, 5:2, 3:6, 6:3},

            }
        #action when click the button b2
        def click2():
            print("EMERGENCY")
            self.slice_to_port = {
                1: {1:5, 5:1, 2:4, 4:2, 3:6, 6:3},
                2: {1: 2, 2: 1},
                3: {1: 2, 2: 1},
                4: {1:5, 5:1, 2:4, 4:2, 3:6, 6:3},

            }
        #action when click the button b3
        def click3():
            print("ADMINISTRATION")
            self.slice_to_port = {
                1: {1:5, 5:1, 2:6, 6:2, 3:4, 4:3},
                4: {2:4, 4:2, 3:5, 5:3, 1:6, 6:1},
                2: {1: 2, 2: 1},
                3: {1: 2, 2: 1},            

            }
        #action when click the button b4
        def click4():
            print("ADMINISTRATION + EMERGENCY")
            self.slice_to_port = {
                1: {1:6, 6:1, 2:4, 4:2, 3:5, 5:3},
                4: {1:5, 5:1, 2:6, 6:2, 3:4, 4:3},
                2: {1: 2, 2: 1},
                3: {1: 2, 2: 1},

            }
        
        #add 4 buttons to the window
        b1=Button(window, text="NORMAL", width=15, height=2, command=click1)
        b2=Button(window, text="EMERGENCY", width=15, height=2, command=click2)
        b3=Button(window, text="ADMINISTRATION", width=20, height=2, command=click3)
        b4=Button(window, text="ADMINISTRATION+EMERGENCY", width=28, height=2, command=click4)
        
        b1.grid(row=0, column=0)
        b2.grid(row=0, column=1)
        b3.grid(row=1, column=0)
        b4.grid(row=1, column=1)
        
        
        window.mainloop()
        #out_port = slice_to_port[dpid][in_port] 
        """
        
        #NORMAL
        self.slice_to_port = {
            1: {1:4, 4:1, 2:5, 5:2, 3:6, 6:3},
            2: {1: 2, 2: 1},
            3: {1: 2, 2: 1},
            4: {1:4, 4:1, 2:5, 5:2, 3:6, 6:3},

        }
        """
        """
        #EMERGENCY
        self.slice_to_port = {
            1: {1:5, 5:1, 2:4, 4:2, 3:6, 6:3},
            2: {1: 2, 2: 1},
            3: {1: 2, 2: 1},
            4: {1:5, 5:1, 2:4, 4:2, 3:6, 6:3},

        }
        
        #ADMINISTRATION
        self.slice_to_port = {
            1: {1:5, 5:1, 2:6, 6:2, 3:4, 4:3},
            4: {2:4, 4:2, 3:5, 5:3, 1:6, 6:1},
            2: {1: 2, 2: 1},
            3: {1: 2, 2: 1},            

        }
              
        #ADMINISTRATION + EMERGENCY
        self.slice_to_port = {
            1: {1:6, 6:1, 2:4, 4:2, 3:5, 5:3},
            4: {1:5, 5:1, 2:6, 6:2, 3:4, 4:3},
            2: {1: 2, 2: 1},
            3: {1: 2, 2: 1},
            
        }
        """ 
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
