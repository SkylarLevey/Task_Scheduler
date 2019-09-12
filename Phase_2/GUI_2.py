from graphics import *
from Data_Structures_2 import *
from data_entry import *
import time

#makes a rectangle in one line of code
def makeRect(gwin,x1,x2,y1,y2,color):
    rec = Rectangle(Point(x1,y1),Point(x2,y2))
    rec.setFill(color)
    rec.draw(gwin)

#makes a text object with one line of code
def makeText(gwin,x,y,text,size):
    guiText = Text(Point(x,y),text)
    guiText.setSize(size)
    guiText.draw(gwin)
    return guiText

#button class, makes a button with certain methods attached to it
class Button:
    def __init__(self, gwin, centerPoint, width, height, color, label):
        self.point1 = Point(centerPoint.getX()+width/2, centerPoint.getY()+height/2)
        self.point2 = Point(centerPoint.getX()-width/2, centerPoint.getY()-height/2)
        self.ogColor = color
        self.buttonRec = Rectangle(self.point1,self.point2)
        self.buttonRec.setFill(color)
        self.buttonRec.draw(gwin)

        text = Text(centerPoint,label)
        text.draw(gwin)

        self.active = True

    #checks if a click was on a button
    def isClicked(self,pt):
        if pt.getX() <= self.point1.getX() and pt.getX() >= self.point2.getX() and \
            pt.getY() <= self.point1.getY() and pt.getY() >= self.point2.getY() and self.active:
            return True
        return False

    def activate(self):
        self.active = True
        self.buttonRec.setFill(self.ogColor)

    def deactivate(self):
        self.buttonRec.setFill('lightgray')
        self.active = False

#updates the GUI list elements
def updateLists(fcfs, rr, fcfsReady, fcfsIO, rrReady, rrIO):
    loopCounts = [len(fcfs.readyQ),len(fcfs.IOwaitingArea),len(rr.readyQ),len(rr.IOwaitingArea)]
    for i in range(4):
        if loopCounts[i] > 10:
            num_items = 10
    for i in range(10):
        if i >= loopCounts[0]:
            fcfsReady[i].setText("")
        else:
            fcfsReady[i].setText(fcfs.readyQ[i].name+"   "+str(fcfs.readyQ[i].cyclesCompleted)+"/"+str(fcfs.readyQ[i].cycles))
            
        if i >= loopCounts[1]:
            fcfsIO[i].setText("")
        else:
            fcfsIO[i].setText(fcfs.IOwaitingArea[i].name+"   "+str(fcfs.IOwaitingArea[i].IOcounter)+"/"+str(fcfs.IOwaitingArea[i].IOduration))
            
        if i >= loopCounts[2]:
            rrReady[i].setText("")
        else:
            rrReady[i].setText(rr.readyQ[i].name+"   "+str(rr.readyQ[i].cyclesCompleted)+"/"+str(rr.readyQ[i].cycles))
            
        if i >= loopCounts[3]:
            rrIO[i].setText("")
        else:
            rrIO[i].setText(rr.IOwaitingArea[i].name+"   "+str(rr.IOwaitingArea[i].IOcounter)+"/"+str(rr.IOwaitingArea[i].IOduration))

#updates the GUI cpu elements
def updateCPUs(fcfs, rr, c1Name, c1Cycles, c1IO, c2Name, c2Cycles, c2IO, context1, context2, quant):
    if fcfs.cpu != 0:
        c1Name.setText(fcfs.cpu.name)
        c1Cycles.setText(str(fcfs.cpu.cyclesCompleted)+"/"+str(fcfs.cpu.cycles))
        c1IO.setText(str(fcfs.cpu.IOcounter)+"/"+str(fcfs.cpu.IOfreq))
    else:
        c1Name.setText("Empty")
        c1Cycles.setText("0/0")
        c1IO.setText("0/0")
    if rr.cpu != 0:
        c2Name.setText(rr.cpu.name)
        c2Cycles.setText(str(rr.cpu.cyclesCompleted)+"/"+str(rr.cpu.cycles))
        c2IO.setText(str(rr.cpu.IOcounter)+"/"+str(rr.cpu.IOfreq))
        quant.setText(str(rr.quantumCounter)+"/"+str(rr.quantum))
    else:
        c2Name.setText("Empty")
        c2Cycles.setText("0/0")
        c2IO.setText("0/0")
        quant.setText("0/"+str(rr.quantum))
        
    if not fcfs.contextFinished:
        context1.setText(str(fcfs.contextCounter)+"/"+str(fcfs.context))
    else:
        context1.setText("0/"+str(fcfs.context))
    if not rr.contextFinished:
        context2.setText(str(rr.contextCounter)+"/"+str(rr.context))
    else:
        context2.setText("0/"+str(rr.context))

#updates the GUI nextArrival field
def updateArrival(cycle, prog, nextArrival):
    if cycle+1 == len(prog[0]):
        prog[0].append([])
        prog[1].append([])
    nextArrivalNames = ""
    for process in prog[0][cycle+1]:
        nextArrivalNames += process.name+",  "
    nextArrival.setText(nextArrivalNames)

def finished(fcfs,rr):
    if fcfs.cpu == 0 and len(fcfs.readyQ) == 0 and len(fcfs.IOwaitingArea) == 0 and \
        rr.cpu == 0 and len(rr.readyQ) == 0 and len(rr.IOwaitingArea) == 0 and rr.cycle > 10:
        return True
    return False

def displayResults(fcfs,rr):
    win = GraphWin("Analysis", 600,600)
    fcfsAnalysis = "First Come First Serve\n"
    rrAnalysis = "Round Robin\n"
    fcfsTotal, rrTotal = 0,0
    for process in fcfs.finishedProcesses:
        fcfsTotal += process.endCycle-process.arrival
        fcfsAnalysis += process.name+", finish at Cycle "+str(process.endCycle)+", With a turnaround time of "+str(process.endCycle-process.arrival)+"\n"
    for process in rr.finishedProcesses:
        rrTotal += process.endCycle-process.arrival
        rrAnalysis += process.name+", finish at Cycle "+str(process.endCycle)+", With a turnaround time of "+ str(process.endCycle-process.arrival)+"\n"
    fcfsAnalysis += "Average turnaround time:  "+str(round(fcfsTotal/len(fcfs.finishedProcesses),4))
    rrAnalysis += "Average turnaround time:  "+str(round(rrTotal/len(rr.finishedProcesses),4))
    makeText(win,300,150,fcfsAnalysis,15)
    makeText(win,300,450,rrAnalysis,15)
    with open("Summary.txt","w") as outfile:
        outfile.write(fcfsAnalysis+"\n\n"+rrAnalysis)    

def main():
######################   GUI   ######################
    
    win = GraphWin("Process Scheduler", 900,750)
    win.setBackground("lightblue")
    win.setCoords(1,1,150,125)

    #Title graphic
    makeText(win,17,122,"Process Scheduler",15)
    makeText(win,14,116,"Current Cycle:",15)
    currentCycle = makeText(win,27,116,"0",15)

    #Cpu
    makeText(win,20,108,"FCFS CPU",15)
    makeRect(win,5,35,75,105,"white")
    c1Name = makeText(win,20,97,"Empty",10)
    makeText(win,20,91,"Prog            I/O ",10)
    c1Cycles = makeText(win,14,84,"0/0",20)
    c1IO = makeText(win,26,84,"0/0",20)

    makeText(win,20,68,"RR CPU",15)
    makeRect(win,5,35,35,65,"white")
    c2Name = makeText(win,20,57,"Empty",10)
    makeText(win,20,51,"Prog            I/O ",10)
    c2Cycles = makeText(win,14,44,"0/0",20)
    c2IO = makeText(win,26,44,"0/0",20)

    makeText(win,10,103,"Context",8)
    context1 = makeText(win,10,100,"0/0",15) 
    makeText(win,10,63,"Context",8)
    context2 = makeText(win,10,60,"0/0",15)
    makeText(win,30,63,"Quantum",8)
    quant = makeText(win,30,60,"0/0",15)

    #Queues Stuff
    makeText(win,65,112,"Readiness Queue(s)",12)
    makeRect(win,40,90,75,110,"white")
    makeRect(win,40,90,35,70,"white")
    
    makeText(win,120,112,"I/O Waiting Area(s)",12)
    makeRect(win,95,145,75,110,"white")
    makeRect(win,95,145,35,70,"white")

    makeText(win,92,123,"Next Arrival",12)
    makeRect(win,70,115,115,121,"white")
    nextArrival = makeText(win,92,118,"Empty",12)
    
    #Control Buttons
    run100 = Button(win,Point(20,25),20,8,"skyblue","Run 100 Cycles")
    run1 = Button(win,Point(20,15),20,8,"skyblue","Run a Cycle")

    run1.deactivate()
    run100.deactivate()

    #Process Entry - File
    makeText(win,60,25,"Add all processes from a file",10)
    fileInput = Entry(Point(60, 21), 20)
    fileInput.setText("test_1.csv")
    fileInput.draw(win)
    addFileButton = Button(win,Point(60,15),18,6,"skyblue","Read File")

    #Process Entry - Single
    makeText(win,95,22,"Add an individual\n process",10)
    addProcButton = Button(win,Point(95,15),14,6,"skyblue","Add")

    makeText(win,133,25,"- Name",9)
    nameInput = Entry(Point(117, 25), 15)
    nameInput.draw(win)

    makeText(win,133,21,"- Cycles",9)
    cyclesInput = Entry(Point(117, 21), 15)
    cyclesInput.draw(win)

    makeText(win,136,17,"- I/O Frequency",9)
    ioFreqInput = Entry(Point(117, 17), 15)
    ioFreqInput.draw(win)

    makeText(win,135,13,"- I/O Duration",9)
    ioDurInput = Entry(Point(117, 13), 15)
    ioDurInput.draw(win)

    fcfsReadiness = []
    fcfsIO = []
    rrReadiness = []
    rrIO = []

    for proc_number in range(10):
        message = ""
        readiness_text1 = makeText(win,65,106-proc_number*3,message,10)
        fcfsReadiness.append(readiness_text1)
        readiness_text2 = makeText(win,65,66-proc_number*3,message,10)
        rrReadiness.append(readiness_text2)

        fairness_message = ""
        io_text1 = makeText(win,120,106-proc_number*3,fairness_message,10)
        fcfsIO.append(io_text1)
        io_text2 = makeText(win,120,66-proc_number*3,fairness_message,10)
        rrIO.append(io_text2)


######################   Logic   ######################

    QUANTUM = 2
    CONTEXT = 0
    cycle = -1
    FCFS = FCFSQueue(CONTEXT)
    RR = RRQueue(CONTEXT,QUANTUM)
    #prog = processes()    

    #Main user clicking loop
    pt = Point(0,0)
    while win.isOpen():
        try:
            #Add Process Button Logic
            if addProcButton.isClicked(pt):
                if not cyclesInput.getText().isdigit():
                    cyclesInput.setText("Not valid")
                if not ioFreqInput.getText().isdigit():
                    ioFreqInput.setText("Not valid")
                if not ioDurInput.getText().isdigit():
                    ioDurInput.setText("Not valid")
                if cyclesInput.getText().isdigit() and ioFreqInput.getText().isdigit() and ioDurInput.getText().isdigit():
                    prog[0][cycle+1].append(Process(nameInput.getText(),
                                        cycle, int(cyclesInput.getText()),
                                        int(ioFreqInput.getText()), int(ioDurInput.getText())))
                    prog[1][cycle+1].append(Process(nameInput.getText(),
                                        cycle, int(cyclesInput.getText()),
                                        int(ioFreqInput.getText()), int(ioDurInput.getText())))
                    updateArrival(cycle, prog, nextArrival)
                    for entry in [nameInput,cyclesInput,ioFreqInput,ioDurInput]:
                        entry.setText('')
                    run1.activate()
                    run100.activate()                    

            #Read File Button Logic
            elif addFileButton.isClicked(pt):
                if isGoodToGo(fileInput.getText()):
                    fcfsArrivalTime = makeProcesses(fileInput.getText())
                    rrArrivalTime = makeProcesses(fileInput.getText())
                    prog = [formatArrivalTime(fcfsArrivalTime),formatArrivalTime(rrArrivalTime)]
                    cycle = -1
                    fileInput.setText('Program Loaded')
                    run1.activate()
                    run100.activate()

                    #reset the process scheduler       
                    FCFS = FCFSQueue(CONTEXT)
                    RR = RRQueue(CONTEXT,QUANTUM)
                    cycle = -1
                    updateArrival(cycle, prog, nextArrival)
                    updateLists(FCFS, RR, fcfsReadiness, fcfsIO, rrReadiness, rrIO)
                    updateCPUs(FCFS, RR, c1Name,c1Cycles,c1IO,c2Name,c2Cycles,c2IO,context1,context2,quant)
                    currentCycle.setText(str(cycle))
                    
                else:
                    fileInput.setText('That file is invalid')
                
            #Run 1 cycle Button Logic
            if run1.isClicked(pt):
                FCFS.nextCycle(prog[0])
                RR.nextCycle(prog[1])
                cycle+=1
                
                updateArrival(cycle, prog, nextArrival)
                updateLists(FCFS, RR, fcfsReadiness, fcfsIO, rrReadiness, rrIO)
                updateCPUs(FCFS, RR, c1Name,c1Cycles,c1IO,c2Name,c2Cycles,c2IO,context1,context2,quant)
                currentCycle.setText(str(cycle))
                if finished(FCFS,RR):
                    displayResults(FCFS,RR)
                    FCFS = FCFSQueue(CONTEXT)
                    RR = RRQueue(CONTEXT,QUANTUM)
                    cycle = -1
                    updateLists(FCFS, RR, fcfsReadiness, fcfsIO, rrReadiness, rrIO)
                    updateCPUs(FCFS, RR, c1Name,c1Cycles,c1IO,c2Name,c2Cycles,c2IO,context1,context2,quant)
                    currentCycle.setText(str(cycle))
                
            #Run 100 cycles Button Logic
            if run100.isClicked(pt):
                for i in range(100):
                    FCFS.nextCycle(prog[0])
                    RR.nextCycle(prog[1])
                    cycle+=1

                    updateArrival(cycle, prog, nextArrival)
                    updateLists(FCFS, RR, fcfsReadiness, fcfsIO, rrReadiness, rrIO)
                    updateCPUs(FCFS, RR, c1Name,c1Cycles,c1IO,c2Name,c2Cycles,c2IO,context1,context2,quant)
                    currentCycle.setText(str(cycle))
                    time.sleep(.1)
                    if finished(FCFS,RR):
                        break
                if finished(FCFS,RR):
                    displayResults(FCFS,RR)
                    FCFS = FCFSQueue(CONTEXT)
                    RR = RRQueue(CONTEXT,QUANTUM)
                    cycle = -1
                    updateLists(FCFS, RR, fcfsReadiness, fcfsIO, rrReadiness, rrIO)
                    updateCPUs(FCFS, RR, c1Name,c1Cycles,c1IO,c2Name,c2Cycles,c2IO,context1,context2,quant)
                    currentCycle.setText(str(cycle))
                
            pt = win.getMouse()

        except GraphicsError: break


main()


###test processes if the files break down
##def processes():
##    FcfsP1 =  Process("1", 2, 6, 3, 5)
##    RrP1 = Process("1", 2, 6, 3, 5)
##    FcfsP2 =  Process("2", 3, 7, 0, 5)
##    RrP2 = Process("2", 3, 7, 0, 5)
##    FcfsP3 =  Process("3", 3, 4, 5, 5)
##    RrP3 = Process("3", 3, 4, 5, 5)
##    FcfsP4 =  Process("4", 4, 8, 3, 5)
##    RrP4 = Process("4", 4, 8, 3, 5)
##    FcfsP5 =  Process("5", 8, 2, 1, 5)
##    RrP5 = Process("5", 8, 2, 1, 5)
##    FcfsP6 =  Process("6", 6, 5, 0, 5)
##    RrP6 = Process("6", 6, 5, 0, 5)
##    
##    fcfsArrivalTime = formatArrivalTime([FcfsP1,FcfsP2,FcfsP3,FcfsP4,FcfsP5,FcfsP6])
##    rrArrivalTime = formatArrivalTime([RrP1,RrP2,RrP3,RrP4,RrP5,RrP6])
##
##    return [fcfsArrivalTime,rrArrivalTime]
