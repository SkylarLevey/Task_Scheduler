#Pfizer I Hardly Know Her!
from random import randrange

class Process:
    def __init__(self, name, arrival, cycles, IOfreq, IOduration, memory):
        self.name = name
        self.arrival = arrival
        self.endCycle = 0
        self.cycles = cycles
        self.cyclesCompleted = 0
        self.IOfreq = IOfreq
        self.IOduration = IOduration
        self.IOcounter = 0
        self.priority = 0
        self.color = [randrange(0,200),randrange(0,200),randrange(0,200)]
        self.memory = memory

    def setPriority(self, priority):
        self.priority = priority

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

class Memory:
    def __init__(self, capacity):
        self.capacity = capacity
        self.nextPointer = 0
        self.totalFreeMem = capacity
        self.memory = [0 for i in range(capacity)]

    #Find the next spot the process could fit and put it there
    def insert(self, process):
        lastEmpty = self.nextPointer
        current = self.nextPointer
        for i in range(self.capacity):
            if self.memory[current%self.capacity] == 0:
                if abs(lastEmpty - current) >= process.memory:
                    break
            else:
                lastEmpty = current
            current += 1
        for i in range(abs(lastEmpty - current)):
            self.memory[(i+lastEmpty)%4096] = process
            self.totalFreeMem -= 1
        self.nextPointer = (self.nextPointer + abs(lastEmpty - current))%4096

    #remove the process from memory
    def delete(self, process):
        for i in range(len(self.memory)):
            if self.memory[i] == process:
                self.memory[i] = 0
                self.totalFreeMem += 1
    
    #check to see if the process could fit
    def checkForFit(self, necesaryMem):
        lastEmpty = self.nextPointer
        current = self.nextPointer
        for i in range(self.capacity):
            if self.memory[current%self.capacity] == 0:
                if abs(lastEmpty - current) >= necesaryMem:
                    return True
            else:
                lastEmpty = current
            current += 1
        return False        

    #compact the memory
    def compaction(self):
        shiftCount = 0
        for i in range(self.capacity-1,0,-1):
            if self.memory[i] == 0:
                self.memory.pop(i)
                shiftCount += 1
        self.nextPointer = len(self.memory)
        for i in range(shiftCount):
            self.memory.append(0)

    
        


######################   First Come First Serve   ######################

class FCFSQueue:
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
        self.memQ = []
        self.memory = Memory(4096)
        
    def insert(self, process):
        self.readyQ.append(process)
        
    def popTop(self):
        return self.readyQ.pop(0)

    def addByPriority(self, process):
        inserted = False
        for i in range(len(self.readyQ)):
            if self.readyQ[i].priority > process.priority:
                self.readyQ.insert(i,process)
                inserted = True
                break
        if not inserted:
            self.readyQ.append(process)
    
    def nextCycle(self, arrivalList):
        self.cycle += 1
                       
        #check for new process and add it to the waiting for mem area
        if len(arrivalList[self.cycle]) > 0:
            for process in arrivalList[self.cycle]:
                self.numProcesses += 1
                process.setPriority(self.numProcesses)
                self.memQ.append(process)                

        #check mem waiting area
        if len(self.memQ) > 0:
            removeProcesses = []
            for process in self.memQ:
                if self.memory.checkForFit(process.memory):
                    self.memory.insert(process)
                    self.insert(process)
                    removeProcesses.append(process)
                elif self.memory.totalFreeMem > process.memory:
                    self.memory.compaction()
                    self.memory.insert(process)
                    self.insert(process)
                    removeProcesses.append(process)
            for process in removeProcesses:
                self.memQ.remove(process)

        #check if the cpu needs to move somewhere else
        if self.cpu != 0:
            self.cpu.cyclesCompleted += 1
            self.cpu.IOcounter += 1
            if self.cpu.processCompleted():
                #get rid of it
                self.cpu.endCycle = self.cycle
                self.finishedProcesses.append(self.cpu)
                self.memory.delete(self.cpu)
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
                self.addByPriority(process)

        #update the contextSwitch
        if not self.contextFinished:
            if self.contextCounter >= self.context:
                self.contextFinished = True
                self.contextCounter = -1
            self.contextCounter += 1

        #check if anyone needs to be moved into the cpu
        if self.cpu == 0 and len(self.readyQ) > 0 and self.contextFinished:
            self.cpu = self.popTop()
        

######################   Round Robin   ######################
class RRQueue:
    def __init__(self,context,quantum):
        self.quantum = quantum
        self.quantumCounter = 0
        self.cpu = 0
        self.readyQ = []
        self.IOwaitingArea = []
        self.cycle = -1
        self.numProcesses = 0
        self.context = context
        self.contextCounter = 0
        self.contextFinished = True
        self.finishedProcesses = []
        self.memQ = []
        self.memory = Memory(4096)
        
    def insert(self, process):
        self.readyQ.append(process)
        
    def popTop(self):
        return self.readyQ.pop(0)        
    
    def nextCycle(self, arrivalList):
        self.cycle += 1
                       
        #check for new process and add it to the waiting for mem area
        if len(arrivalList[self.cycle]) > 0:
            for process in arrivalList[self.cycle]:
                self.numProcesses += 1
                self.memQ.append(process)                

        #check mem waiting area
        if len(self.memQ) > 0:
            removeProcesses = []
            for process in self.memQ:
                if self.memory.checkForFit(process.memory):
                    self.memory.insert(process)
                    self.insert(process)
                    removeProcesses.append(process)
                elif self.memory.totalFreeMem > process.memory:
                    self.memory.compaction()
                    self.memory.insert(process)
                    self.insert(process)
                    removeProcesses.append(process)
            for process in removeProcesses:
                self.memQ.remove(process)

        #check if the cpu needs to move somewhere else
        if self.cpu != 0:
            self.cpu.cyclesCompleted += 1
            self.cpu.IOcounter += 1
            self.quantumCounter += 1
            if self.cpu.processCompleted():
                #get rid of it
                self.cpu.endCycle = self.cycle
                self.finishedProcesses.append(self.cpu)
                self.memory.delete(self.cpu)
                self.cpu = 0
                self.quantumCounter = 0
                self.contextFinished = False
            elif self.cpu.IOneeded():
                #put it in the I/O waiting area
                self.cpu.IOcounter = 0
                self.IOwaitingArea.append(self.cpu)
                self.cpu = 0
                self.quantumCounter = 0
                self.contextFinished = False
            elif self.quantumCounter >= self.quantum and len(self.readyQ) > 0:
                #move it to the back of the queue
                self.quantumCounter = 0
                self.insert(self.cpu)
                self.cpu = 0
                self.contextFinished = False
                
        #increment everything in the I/O waiting area
        for process in self.IOwaitingArea:
            process.IOcounter += 1
            if process.IOCompleted():
                process.IOcounter = 0
                self.IOwaitingArea.remove(process)
                self.insert(process)

        #update the contextSwitch
        if not self.contextFinished:
            if self.contextCounter >= self.context:
                self.contextFinished = True
                self.contextCounter = -1
            self.contextCounter += 1

        #check if anyone needs to be moved into the cpu
        if self.cpu == 0 and len(self.readyQ) > 0 and self.contextFinished:
            self.cpu = self.popTop()

######################   File Formating   ######################
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

    #for arrivalTime in arrivalList:
    #    print(arrivalTime)

    return arrivalList
        



