
import numpy
import socket
import json
from struct import *

class SendSignals(OVBox):
    def __init__(self):
        OVBox.__init__(self)
        self.socket = None
        self.address = None
        self.port = None
        self.samplingRate = None
        self.channelNum = None
        self.dimensionSizes = None
        self.signalsNum = 0

    def initialize(self):
        self.address = self.setting["Address"]
        self.port = int(self.setting["Port"])
        self.signalsNum = len(self.input)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def process(self):
        for i in range(self.signalsNum):
            while self.input[i]:
                chunk = self.input[i].pop()
                if(type(chunk) == OVSignalHeader):
                    self.samplingRate  = chunk.samplingRate
                    self.channelNum = chunk.dimensionSizes[0]
                    self.dimensionSizes = chunk.dimensionSizes
                elif(type(chunk) == OVSignalBuffer):
                    numpyBuffer = numpy.array(chunk).reshape(self.channelNum * self.dimensionSizes[1])
                    data_list = numpyBuffer.tolist()
                    data_list.append(i) # label
                    packed_data = ""
                    for d in data_list:
                        packed_data += pack('f', d)
                    self.socket.sendto(packed_data, (self.address, self.port))
                    # print "send signal %d" % i
                else:
                    pass #for OVSignalEnd

    def uninitialize(self):
        self.socket.close()

box = SendSignals()
