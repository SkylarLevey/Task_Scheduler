from graphics import *
from Data_Structures_3 import *
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
def updateLists(algo1, algo2, algo1Ready, algo1IO, algo2Ready, algo2IO):
    loopCounts = [len(algo1.readyQ),len(algo1.IOwaitingArea),len(algo2.readyQ),len(algo2.IOwaitingArea)]
    for i in range(4):
        if loopCounts[i] > 10:
            num_items = 10
    for i in range(10):
        if i >= loopCounts[0]:
            algo1Ready[i].setText("")
        else:
            algo1Ready[i].setText(algo1.readyQ[i].name+"   "+str(algo1.readyQ[i].cyclesCompleted)+"/"+str(algo1.readyQ[i].cycles)+"   Remaining: "+str(algo1.readyQ[i].cycles-algo1.readyQ[i].cyclesCompleted))
            algo1Ready[i].setFill(color_rgb(algo1.readyQ[i].color[0],algo1.readyQ[i].color[1],algo1.readyQ[i].color[2]))
            
        if i >= loopCounts[1]:
            algo1IO[i].setText("")
        else:
            algo1IO[i].setText(algo1.IOwaitingArea[i].name+"   "+str(algo1.IOwaitingArea[i].IOcounter)+"/"+str(algo1.IOwaitingArea[i].IOduration)+"   Remaining: "+str(algo1.IOwaitingArea[i].cycles-algo1.IOwaitingArea[i].cyclesCompleted))
            algo1IO[i].setFill(color_rgb(algo1.IOwaitingArea[i].color[0],algo1.IOwaitingArea[i].color[1],algo1.IOwaitingArea[i].color[2]))
            
        if i >= loopCounts[2]:
            algo2Ready[i].setText("")
        else:
            algo2Ready[i].setText(algo2.readyQ[i].name+"   "+str(algo2.readyQ[i].cyclesCompleted)+"/"+str(algo2.readyQ[i].cycles)+"   Remaining: "+str(algo2.readyQ[i].cycles-algo2.readyQ[i].cyclesCompleted))
            algo2Ready[i].setFill(color_rgb(algo2.readyQ[i].color[0],algo2.readyQ[i].color[1],algo2.readyQ[i].color[2]))
            
        if i >= loopCounts[3]:
            algo2IO[i].setText("")
        else:
            algo2IO[i].setText(algo2.IOwaitingArea[i].name+"   "+str(algo2.IOwaitingArea[i].IOcounter)+"/"+str(algo2.IOwaitingArea[i].IOduration)+"   Remaining: "+str(algo2.IOwaitingArea[i].cycles-algo2.IOwaitingArea[i].cyclesCompleted))
            algo2IO[i].setFill(color_rgb(algo2.IOwaitingArea[i].color[0],algo2.IOwaitingArea[i].color[1],algo2.IOwaitingArea[i].color[2]))

#updates the GUI cpu elements
def updateCPUs(algo1, algo2, c1Name, c1Cycles, c1IO, c2Name, c2Cycles, c2IO, context1, context2):
    if algo1.cpu != 0:
        c1Name.setText(algo1.cpu.name)
        c1Name.setFill(color_rgb(algo1.cpu.color[0],algo1.cpu.color[1],algo1.cpu.color[2]))
        c1Cycles.setText(str(algo1.cpu.cyclesCompleted)+"/"+str(algo1.cpu.cycles))
        c1Cycles.setFill(color_rgb(algo1.cpu.color[0],algo1.cpu.color[1],algo1.cpu.color[2]))
        c1IO.setText(str(algo1.cpu.IOcounter)+"/"+str(algo1.cpu.IOfreq))
        c1IO.setFill(color_rgb(algo1.cpu.color[0],algo1.cpu.color[1],algo1.cpu.color[2]))
    else:
        c1Name.setText("Empty")
        c1Name.setFill(color_rgb(0,0,0))
        c1Cycles.setText("0/0")
        c1Cycles.setFill(color_rgb(0,0,0))
        c1IO.setText("0/0")
        c1IO.setFill(color_rgb(0,0,0))
    if algo2.cpu != 0:
        c2Name.setText(algo2.cpu.name)
        c2Name.setFill(color_rgb(algo2.cpu.color[0],algo2.cpu.color[1],algo2.cpu.color[2]))
        c2Cycles.setText(str(algo2.cpu.cyclesCompleted)+"/"+str(algo2.cpu.cycles))
        c2Cycles.setFill(color_rgb(algo2.cpu.color[0],algo2.cpu.color[1],algo2.cpu.color[2]))
        c2IO.setText(str(algo2.cpu.IOcounter)+"/"+str(algo2.cpu.IOfreq))
        c2IO.setFill(color_rgb(algo2.cpu.color[0],algo2.cpu.color[1],algo2.cpu.color[2]))
    else:
        c2Name.setText("Empty")
        c2Name.setFill(color_rgb(0,0,0))
        c2Cycles.setText("0/0")
        c2Cycles.setFill(color_rgb(0,0,0))
        c2IO.setText("0/0")
        c2IO.setFill(color_rgb(0,0,0))
        
    if not algo1.contextFinished:
        context1.setText(str(algo1.contextCounter)+"/"+str(algo1.context))
    else:
        context1.setText("0/"+str(algo1.context))
    if not algo2.contextFinished:
        context2.setText(str(algo2.contextCounter)+"/"+str(algo2.context))
    else:
        context2.setText("0/"+str(algo2.context))

#updates the GUI nextArrival field
def updateArrival(cycle, prog, nextArrival):
    if cycle+1 == len(prog[0]):
        prog[0].append([])
        prog[1].append([])
    nextArrivalNames = ""
    for process in prog[0][cycle+1]:
        nextArrivalNames += process.name+" ("+str(process.cycles)+"),  "
    nextArrival.setText(nextArrivalNames)

def finished(algo1,algo2):
    if algo1.cpu == 0 and len(algo1.readyQ) == 0 and len(algo1.IOwaitingArea) == 0 and \
        algo2.cpu == 0 and len(algo2.readyQ) == 0 and len(algo2.IOwaitingArea) == 0 and algo2.cycle > 10:
        return True
    return False

def displayResults(algo1,algo2):
    win = GraphWin("Analysis", 600,600)
    algo1Analysis = "Shortest Process Next\n"
    algo2Analysis = "Shortest Remaining Time\n"
    algo1Total, algo2Total = 0,0
    for process in algo1.finishedProcesses:
        algo1Total += process.endCycle-process.arrival
        algo1Analysis += process.name+", finish at Cycle "+str(process.endCycle)+", With a turnaround time of "+str(process.endCycle-process.arrival)+"\n"
    for process in algo2.finishedProcesses:
        algo2Total += process.endCycle-process.arrival
        algo2Analysis += process.name+", finish at Cycle "+str(process.endCycle)+", With a turnaround time of "+ str(process.endCycle-process.arrival)+"\n"
    algo1Analysis += "Average turnaround time:  "+str(round(algo1Total/len(algo1.finishedProcesses),4))
    algo2Analysis += "Average turnaround time:  "+str(round(algo2Total/len(algo2.finishedProcesses),4))
    makeText(win,300,150,algo1Analysis,15)
    makeText(win,300,450,algo2Analysis,15)
    with open("Summary.txt","w") as outfile:
        outfile.write(algo1Analysis+"\n\n"+algo2Analysis)    

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
    makeText(win,20,108,"SPN CPU",15)
    makeRect(win,5,35,75,105,"white")
    c1Name = makeText(win,20,97,"Empty",10)
    makeText(win,20,91,"Prog            I/O ",10)
    c1Cycles = makeText(win,14,84,"0/0",20)
    c1IO = makeText(win,26,84,"0/0",20)

    makeText(win,20,68,"SRT CPU",15)
    makeRect(win,5,35,35,65,"white")
    c2Name = makeText(win,20,57,"Empty",10)
    makeText(win,20,51,"Prog            I/O ",10)
    c2Cycles = makeText(win,14,44,"0/0",20)
    c2IO = makeText(win,26,44,"0/0",20)

    makeText(win,10,103,"Context",8)
    context1 = makeText(win,10,100,"0/0",15) 
    makeText(win,10,63,"Context",8)
    context2 = makeText(win,10,60,"0/0",15)

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

    spnReadiness = []
    spnIO = []
    srtReadiness = []
    srtIO = []

    for proc_number in range(10):
        message = ""
        readiness_text1 = makeText(win,65,106-proc_number*3,message,10)
        spnReadiness.append(readiness_text1)
        readiness_text2 = makeText(win,65,66-proc_number*3,message,10)
        srtReadiness.append(readiness_text2)

        fairness_message = ""
        io_text1 = makeText(win,120,106-proc_number*3,fairness_message,10)
        spnIO.append(io_text1)
        io_text2 = makeText(win,120,66-proc_number*3,fairness_message,10)
        srtIO.append(io_text2)


######################   Logic   ######################
	#SPN shortest process next
	#SRT shortest remaining time

    CONTEXT = 1
    cycle = -1
    SPN = SPNQueue(CONTEXT)
    SRT = SRTQueue(CONTEXT)
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
                    spnArrivalTime = makeProcesses(fileInput.getText())
                    srtArrivalTime = makeProcesses(fileInput.getText())
                    prog = [formatArrivalTime(spnArrivalTime),formatArrivalTime(srtArrivalTime)]
                    cycle = -1
                    fileInput.setText('Program Loaded')
                    run1.activate()
                    run100.activate()

                    #reset the process scheduler       
                    SPN = SPNQueue(CONTEXT)
                    SRT = SRTQueue(CONTEXT)
                    cycle = -1
                    updateArrival(cycle, prog, nextArrival)
                    updateLists(SPN, SRT, spnReadiness, spnIO, srtReadiness, srtIO)
                    updateCPUs(SPN, SRT, c1Name,c1Cycles,c1IO,c2Name,c2Cycles,c2IO,context1,context2)
                    currentCycle.setText(str(cycle))
                    
                else:
                    fileInput.setText('That file is invalid')
                
            #Run 1 cycle Button Logic
            if run1.isClicked(pt):
                SPN.nextCycle(prog[0])
                SRT.nextCycle(prog[1])
                cycle+=1
                
                updateArrival(cycle, prog, nextArrival)
                updateLists(SPN, SRT, spnReadiness, spnIO, srtReadiness, srtIO)
                updateCPUs(SPN, SRT, c1Name,c1Cycles,c1IO,c2Name,c2Cycles,c2IO,context1,context2)
                currentCycle.setText(str(cycle))
                if finished(SPN,SRT):
                    displayResults(SPN,SRT)
                    SPN = SPNQueue(CONTEXT)
                    SRT = SRTQueue(CONTEXT)
                    cycle = -1
                    updateLists(SPN, SRT, spnReadiness, spnIO, srtReadiness, srtIO)
                    updateCPUs(SPN, SRT, c1Name,c1Cycles,c1IO,c2Name,c2Cycles,c2IO,context1,context2)
                    currentCycle.setText(str(cycle))
                
            #Run 100 cycles Button Logic
            if run100.isClicked(pt):
                for i in range(100):
                    SPN.nextCycle(prog[0])
                    SRT.nextCycle(prog[1])
                    cycle+=1

                    updateArrival(cycle, prog, nextArrival)
                    updateLists(SPN, SRT, spnReadiness, spnIO, srtReadiness, srtIO)
                    updateCPUs(SPN, SRT, c1Name,c1Cycles,c1IO,c2Name,c2Cycles,c2IO,context1,context2)
                    currentCycle.setText(str(cycle))
                    time.sleep(.1)
                    if finished(SPN,SRT):
                        break
                if finished(SPN,SRT):
                    displayResults(SPN,SRT)
                    SPN = SPNQueue(CONTEXT)
                    SRT = SRTQueue(CONTEXT)
                    cycle = -1
                    updateLists(SPN, SRT, spnReadiness, spnIO, srtReadiness, srtIO)
                    updateCPUs(SPN, SRT, c1Name,c1Cycles,c1IO,c2Name,c2Cycles,c2IO,context1,context2)
                    currentCycle.setText(str(cycle))
                
            pt = win.getMouse()

        except GraphicsError: break


main()
