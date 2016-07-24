# coding=utf-8
from numpy.random import *
from copy import deepcopy

class Stimulator(OVBox):
    def __init__(self):
        OVBox.__init__(self)
        self.baseLabel = None
        self.baseCode = None
        self.triggerLabel = None
        self.triggerCode = None
        self.isWorking = False
        self.interStimulusInterval = 300
        self.stimulusLength = 100
        self.interPatternInterval = 3000
        self.patterns = [1, 2, 3, 4, 5, 6]
        self.answers = [1, 2, 3, 4, 5, 6]
        self.repetitions = 10
        self.currentPatterns = []
        self.currentRepetition = 0
        self.currentTrial = 0
        self.currentAnswer = None
        self.time = None
        self.status = None
        self.debug = False

    def initialize(self):
        self.baseLabel = self.setting['BaseStimulation']
        self.triggerLabel = self.setting['TriggerStimulation']
        self.baseCode = OpenViBE_stimulation[self.baseLabel]
        self.triggerCode = OpenViBE_stimulation[self.triggerLabel]
        self.outputStimulus = self.output[0]
        self.outputTargetLabel  = self.output[1]
        self.outputAnswerLabel  = self.output[2]

    def resetTimer(self):
        self.time = self.getCurrentTime()

    def start(self):
        self.status = "PatternInterval"
        self.currentPatterns = deepcopy(self.patterns)
        self.currentTrial = 0
        self.nextTrial()

        self.outputStimulus.append(OVStimulationHeader(0., 0.))
        self.isWorking = True
        self.resetTimer()
        print "start"

    def end(self):
        self.sendExperimentStop()
        end = self.getCurrentTime()
        self.outputStimulus.append(OVStimulationEnd(end, end))
        self.outputTargetLabel.append(OVStimulationEnd(end, end))
        self.outputAnswerLabel.append(OVStimulationEnd(end, end))

        self.isWorking = False
        print "end"

    def stimulusInterval(self):
        if self.debug:
            print "StimulusInterval"
        self.status = "Stimulus"

    def patternInterval(self):
        if self.debug:
            print "PatternInterval"
        self.status = "Stimulus"

    def nextRepetition(self):
        self.currentPatterns = deepcopy(self.patterns)
        self.currentRepetition += 1
        self.status = "StimulusInterval"

    def nextTrial(self):
        self.currentTrial += 1
        if self.currentTrial > len(self.answers):
            self.status = "End"
        else:
            self.currentAnswer = self.answers[self.currentTrial - 1]
            self.sendAnswerLabel(self.currentAnswer)
            self.currentRepetition = 1
            self.status = "PatternInterval"

    def stimulus(self):
        stimulus = self.currentPatterns.pop(randint(len(self.currentPatterns)))
        self.sendStimulus(stimulus)
        self.sendTargetLabel(stimulus, self.currentAnswer)

        if len(self.currentPatterns) == 0:
            self.nextRepetition()
            if self.currentRepetition > self.repetitions:
                self.status = "prepareNextTrial"
        else:
            self.status = "StimulusInterval"

    def sendStimulus(self, stimulus):
        stimSet = OVStimulationSet(self.getCurrentTime(), self.getCurrentTime()+1./self.getClock())
        stimSet.append(OVStimulation(stimulus + self.baseCode, self.getCurrentTime(), self.stimulusLength / 1000.))
        self.outputStimulus.append(stimSet)

    def sendTargetLabel(self, stimulus, answer):
        if stimulus == answer:
            label = OpenViBE_stimulation["OVTK_StimulationId_Target"]
        else:
            label = OpenViBE_stimulation["OVTK_StimulationId_NonTarget"]

        stimSet = OVStimulationSet(self.getCurrentTime(), self.getCurrentTime()+1./self.getClock())
        stimSet.append(OVStimulation(label, self.getCurrentTime(), self.stimulusLength / 1000.))
        self.outputTargetLabel.append(stimSet)

    def sendAnswerLabel(self, answer):
        stimSet = OVStimulationSet(self.getCurrentTime(), self.getCurrentTime()+1./self.getClock())
        stimSet.append(OVStimulation(answer + self.baseCode, self.getCurrentTime(), self.stimulusLength / 1000.))
        self.outputAnswerLabel.append(stimSet)

    def sendExperimentStop(self):
        experimentStopCode = OpenViBE_stimulation["OVTK_StimulationId_ExperimentStop"]
        stimSet = OVStimulationSet(self.getCurrentTime(), self.getCurrentTime()+1./self.getClock())
        stimSet.append(OVStimulation(experimentStopCode, self.getCurrentTime(), self.stimulusLength / 1000.))
        self.outputAnswerLabel.append(stimSet)

    def work(self):
        interval_time = (self.getCurrentTime() - self.time) * 1000 # ms
        previousStatus = self.status
        if self.status == "Stimulus":
            self.stimulus()
        elif self.status == "PatternInterval":
            if interval_time > self.interPatternInterval:
                self.patternInterval()
        elif self.status == "StimulusInterval":
            if interval_time > self.interStimulusInterval + self.stimulusLength:
                self.stimulusInterval()
        elif self.status == "prepareNextTrial":
            if interval_time > self.interPatternInterval:
                self.nextTrial()
        elif self.status == "End":
            if interval_time > self.interPatternInterval:
                self.end()
        if self.status != previousStatus:
            self.resetTimer()

    def checkTrigger(self):
        while self.input[0]:
            chunk = self.input[0].pop()
            if(type(chunk) == OVStimulationSet):
                for stimulation in chunk:
                    if stimulation.identifier == self.triggerCode:
                        self.start()

    def process(self):
        if self.isWorking:
            self.work()
        else:
            self.checkTrigger()
        return

box = Stimulator()
