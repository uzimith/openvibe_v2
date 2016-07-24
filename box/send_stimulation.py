import socket

class SendStimulation(OVBox):
    def __init__(self):
        OVBox.__init__(self)
        self.address = None
        self.port = None
        self.socket = None

    def initialize(self):
        self.address = self.setting["Address"]
        self.port = int(self.setting["Port"])
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def process(self):
        while self.input[0]:
            chunk = self.input[0].pop()
            if(type(chunk) == OVStimulationSet):
                for stimulation in chunk:
                    self.socket.sendto(str(stimulation.identifier - OpenViBE_stimulation["OVTK_StimulationId_Label_00"]), (self.address, self.port))
            else:
                pass #for OVSignalEnd

    def uninitialize(self):
        self.socket.close()

box = SendStimulation()
