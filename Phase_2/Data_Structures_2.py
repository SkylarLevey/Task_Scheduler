#Pfizer I Hardly Know Her!

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
        self.priority = 0

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
                       
        #check for new process and add it if necesary
        if len(arrivalList[self.cycle]) > 0:
            for process in arrivalList[self.cycle]:
                self.numProcesses += 1
                process.setPriority(self.numProcesses)
                self.insert(process)

        #check if the cpu needs to move somewhere else
        if self.cpu != 0:
            self.cpu.cyclesCompleted += 1
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
        
    def insert(self, process):
        self.readyQ.append(process)
        
    def popTop(self):
        return self.readyQ.pop(0)        
    
    def nextCycle(self, arrivalList):
        self.cycle += 1
                       
        #check for new process and add it if necesary
        if len(arrivalList[self.cycle]) > 0:
            for process in arrivalList[self.cycle]:
                self.numProcesses += 1
                self.insert(process)

        #check if the cpu needs to move somewhere else
        if self.cpu != 0:
            self.cpu.cyclesCompleted += 1
            self.cpu.IOcounter += 1
            self.quantumCounter += 1
            if self.cpu.processCompleted():
                #get rid of it
                self.cpu.endCycle = self.cycle
                self.finishedProcesses.append(self.cpu)
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
            elif self.quantumCounter >= self.quantum:
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


######################   MAIN   ######################
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
        
def test():
    #process = Process(name, arrival, cycles, IOfreq, IOduration)
    FcfsP1 =  Process("1", 2, 6, 3, 5)
    RrP1 = Process("1", 2, 6, 3, 5)
    FcfsP2 =  Process("2", 3, 7, 0, 5)
    RrP2 = Process("2", 3, 7, 0, 5)
    FcfsP3 =  Process("3", 3, 4, 5, 5)
    RrP3 = Process("3", 3, 4, 5, 5)
    FcfsP4 =  Process("4", 4, 8, 3, 5)
    RrP4 = Process("4", 4, 8, 3, 5)
    FcfsP5 =  Process("5", 8, 2, 1, 5)
    RrP5 = Process("5", 8, 2, 1, 5)
    FcfsP6 =  Process("6", 6, 5, 0, 5)
    RrP6 = Process("6", 6, 5, 0, 5)
    
    fcfsArrivalTime = formatArrivalTime([FcfsP1,FcfsP2,FcfsP3,FcfsP4,FcfsP5,FcfsP6])
    rrArrivalTime = formatArrivalTime([RrP1,RrP2,RrP3,RrP4,RrP5,RrP6])

    fcfsQ = FCFSQueue(0)
    for i in range(100):
        if fcfsQ.cycle >= len(fcfsArrivalTime)-1:
            fcfsArrivalTime.append([])
        fcfsQ.nextCycle(fcfsArrivalTime)
        print("CYCLE NUMBER", fcfsQ.cycle, "- CPU", fcfsQ.cpu, "- Q",len(fcfsQ.readyQ),"- I/O", len(fcfsQ.IOwaitingArea))


if __name__ == "__main__":
    test()
        
#auto end

#Summary at end of run/add auto finish when everything is empty
    
#finish cycle for each process 
#turnaround for each process (arrived to completed)
#average turnaround for each alg

#Read file resets the program




