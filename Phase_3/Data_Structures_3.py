#Pfizer I Hardly Know Her!
from random import randrange

class Process:
    def __init__(self, name, arrival, cycles, IOfreq, IOduration):
        self.name = name
        self.arrival = arrival
        self.endCycle = 0
        self.cycles = cycles
        self.cyclesCompleted = 0
        self.IOfreq = IOfreq
        self.IOduration = IOduration
        self.IOcounter = 0
        self.color = [randrange(0,200),randrange(0,200),randrange(0,200)]

    def IOCompleted(self):
        '''For each IO event '''
        if self.IOduration == self.IOcounter:
            self.IOcounter=0
            return True
        return False
    
    def IOneeded(self):
        '''For each IO event '''
        if self.IOfreq == self.IOcounter and self.IOfreq != 0:
            self.IOcounter=0
            return True
        return False
    
    def processCompleted(self):
        '''For the entire process '''
        return self.cycles == self.cyclesCompleted

    def __str__(self):
        return self.name


######################   Shortest Process Next   ######################
class SPNQueue:
    def __init__(self,context):
        self.cpu = 0
        self.readyQ = []
        self.IOwaitingArea = []
        self.cycle = -1
        self.numProcesses = 0
        self.context = context
        self.contextCounter = 0
        self.contextFinished = True
        self.finishedProcesses = []

    def popTop(self):
        return self.readyQ.pop(0) 

    def insertAndSort(self, process):
        self.readyQ.append(process)
        #bubble sort the values
        for i in range(len(self.readyQ)-1):
            for j in range(len(self.readyQ)-i-1):
                if (self.readyQ[j].cycles - self.readyQ[j].cyclesCompleted) > \
                (self.readyQ[j+1].cycles - self.readyQ[j+1].cyclesCompleted):
                    temp = self.readyQ[j]
                    self.readyQ[j] = self.readyQ[j+1]
                    self.readyQ[j+1] = temp
    
    def nextCycle(self, arrivalList):
        self.cycle += 1
                       
        #check for new process and add it if necesary
        if len(arrivalList[self.cycle]) > 0:
            for process in arrivalList[self.cycle]:
                self.numProcesses += 1
                self.insertAndSort(process)

        #check if the cpu needs to move somewhere else
        if self.cpu != 0:
            self.cpu.cyclesCompleted += 1
            if self.cpu.IOfreq != 0:
                self.cpu.IOcounter += 1
            if self.cpu.processCompleted():
                #get rid of it
                self.cpu.endCycle = self.cycle
                self.finishedProcesses.append(self.cpu)
                self.cpu = 0
                self.contextFinished = False
            elif self.cpu.IOneeded():
                #put it in the I/O waiting area
                self.cpu.IOcounter = 0
                self.IOwaitingArea.append(self.cpu)
                self.cpu = 0
                self.contextFinished = False

        #increment everything in the I/O waiting area
        for process in self.IOwaitingArea:
            process.IOcounter += 1
            if process.IOCompleted():
                process.IOcounter = 0
                self.IOwaitingArea.remove(process)
                self.insertAndSort(process)

        #update the contextSwitch
        if not self.contextFinished:
            if self.contextCounter >= self.context:
                self.contextFinished = True
                self.contextCounter = -1
            self.contextCounter += 1

        #check if anyone needs to be moved into the cpu
        if self.cpu == 0 and len(self.readyQ) > 0 and self.contextFinished:
            self.cpu = self.popTop()
            
        

######################   Shortest Remaining Time   ######################
class SRTQueue:
    def __init__(self,context):
        self.cpu = 0
        self.readyQ = []
        self.IOwaitingArea = []
        self.cycle = -1
        self.numProcesses = 0
        self.context = context
        self.contextCounter = 0
        self.contextFinished = True
        self.finishedProcesses = []

    def popTop(self):
        return self.readyQ.pop(0) 

    def insertAndSort(self, process):
        self.readyQ.append(process)
        #bubble sort the values
        for i in range(len(self.readyQ)-1):
            for j in range(len(self.readyQ)-i-1):
                if (self.readyQ[j].cycles - self.readyQ[j].cyclesCompleted) > \
                (self.readyQ[j+1].cycles - self.readyQ[j+1].cyclesCompleted):
                    temp = self.readyQ[j]
                    self.readyQ[j] = self.readyQ[j+1]
                    self.readyQ[j+1] = temp
    
    def nextCycle(self, arrivalList):
        self.cycle += 1

        #check if the cpu needs to move somewhere else
        if self.cpu != 0:
            self.cpu.cyclesCompleted += 1
            if self.cpu.IOfreq != 0:
                self.cpu.IOcounter += 1
            if self.cpu.processCompleted():
                #get rid of it
                self.cpu.endCycle = self.cycle
                self.finishedProcesses.append(self.cpu)
                self.cpu = 0
                self.contextFinished = False
            elif self.cpu.IOneeded():
                #put it in the I/O waiting area
                self.cpu.IOcounter = 0
                self.IOwaitingArea.append(self.cpu)
                self.cpu = 0
                self.contextFinished = False

        #increment everything in the I/O waiting area
        for process in self.IOwaitingArea:
            process.IOcounter += 1
            if process.IOCompleted():
                process.IOcounter = 0
                self.IOwaitingArea.remove(process)
                self.insertAndSort(process)
                
        #check for new process and switch it into the cpu if it is faster than the current process
        if len(arrivalList[self.cycle]) > 0:
            for process in arrivalList[self.cycle]:
                self.numProcesses += 1
                if self.cpu != 0:
                    if (process.cycles - process.cyclesCompleted) < (self.cpu.cycles - self.cpu.cyclesCompleted):
                        self.insertAndSort(process)
                        self.insertAndSort(self.cpu)
                        self.cpu = 0
                        self.contextFinished = False
                    else:
                        self.insertAndSort(process)
                else:
                    self.insertAndSort(process)

        #update the contextSwitch
        if not self.contextFinished:
            if self.contextCounter >= self.context:
                self.contextFinished = True
                self.contextCounter = -1
            self.contextCounter += 1

        #check if anyone needs to be moved into the cpu
        if self.cpu == 0 and len(self.readyQ) > 0 and self.contextFinished:
            self.cpu = self.popTop()



def formatArrivalTime(processes):
    lastArrival = 0
    for process in processes:
        if process.arrival > lastArrival:
            lastArrival = process.arrival

    arrivalList = []
    for i in range(lastArrival+1):
        arrivalList.append([])

    for process in processes:
        arrivalList[process.arrival].append(process)

    return arrivalList


        

#preemtive context switch
    #bug

##    def getSmallestReadyProcess(self):
##        smallestTimeLeft = self.readyQ[0].cycles - self.readyQ[0].cyclesCompleted
##        returnProcess = 0
##        for i in range(len(self.readyQ)):
##            processTimeLeft = self.readyQ[i].cycles - self.readyQ[i].cyclesCompleted
##            if processTimeLeft < smallestTimeLeft:
##                smallestTimeLeft = processTimeLeft
##                returnProcess = i
##        return self.readyQ.pop(returnProcess)


