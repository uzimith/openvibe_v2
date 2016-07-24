import socket

class Delay(OVBox):
    def __init__(self):
        OVBox.__init__(self)
        self.delay = 1

    def initialize(self):
        pass

    def sendDelay(self, code):
        now = self.getCurrentTime()
        stimSet = OVStimulationSet(now, now + self.delay + 1./self.getClock())
        stimSet.append(OVStimulation(code, now + self.delay, 0.))
        self.output[0].append(stimSet)
        pass

    def process(self):
        while self.input[0]:
            chunk = self.input[0].pop()
            if(type(chunk) == OVStimulationSet):
                for stimulation in chunk:
                    self.sendDelay(stimulation.identifier)
            else:
                pass #for OVSignalEnd

box = Delay()
