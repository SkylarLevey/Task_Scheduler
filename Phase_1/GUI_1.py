from graphics import *
import program
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
    def __init__(self, gwin, centerPoint, width, height, color, lable):
        self.point1 = Point(centerPoint.getX()+width/2, centerPoint.getY()+height/2)
        self.point2 = Point(centerPoint.getX()-width/2, centerPoint.getY()-height/2)

        buttonRec = Rectangle(self.point1,self.point2)
        buttonRec.setFill(color)
        buttonRec.draw(gwin)

        text = Text(centerPoint,lable)
        text.draw(gwin)

    #checks if a click was on a button
    def isClicked(self,pt):
        if pt.getX() <= self.point1.getX() and pt.getX() >= self.point2.getX() and \
            pt.getY() <= self.point1.getY() and pt.getY() >= self.point2.getY():
            return True
        return False

#updates the GUI list elements
def updateLists(priority_list,fairness_list,heap,queue):
    heapPopTracker = []
    queuePopTracker = []
    num_items = heap.n
    if num_items > 10:
        num_items = 10
    for i in range(10):
        if i >= num_items:
            priority_list[i].setText("")
            fairness_list[i].setText("")
        else:
            this_process = heap.popMin()
            priority_list[i].setText(str(i+1)+". "+this_process.name+",     priority: "+str(this_process.priority))
            heapPopTracker.append(this_process)
            that_process = queue.popTop()
            fairness_list[i].setText(str(i+1)+". "+that_process.name+",     cycles waited: "+str(that_process.cyclesWaited))
            queuePopTracker.append(that_process)

    for i in range(num_items):
        heap.insert(heapPopTracker.pop(0))
        queue.insert(queuePopTracker.pop(0))

#Reads in a CSV file and then creates a process out of every line
def makeProcessFromCSV(filename):
    with open(filename,'r') as file:
        lines = [line.split(',') for line in file.read().split('\n')]
        all_processes = lines[1:]
        process_objects = []

        for process in all_processes:
            if len(process) != 4:
                continue

            name = process[0]
            priority = process[1]
            cycles = process[2]
            ram = process[3]

            new_process = program.Process(name,priority,cycles,ram)
            process_objects.append(new_process)

    return process_objects

def makeProcessFromInput(name,priority,cycles,ram):
    return program.Process(name,priority,cycles,ram)

def main():
    win = GraphWin("Process Scheduler", 900,600)
    win.setBackground("lightblue")
    win.setCoords(1,1,150,100)

    #Memory
    makeText(win,17,93,"Memory Availible:",15)
    mem = makeText(win,40,93,"X Gigs",15)

    #Cores Stuff
    makeText(win,20,83,"Core 1",15)
    makeRect(win,5,35,50,80,"white")
    c1Name = makeText(win,20,72,"Empty",10)
    makeText(win,20,66,"Cycles",10)
    c1Cycles = makeText(win,20,60,"0/0",20)

    makeText(win,20,43,"Core 2",15)
    makeRect(win,5,35,10,40,"white")
    c2Name = makeText(win,20,32,"Empty",10)
    makeText(win,20,26,"Cycles",10)
    c2Cycles = makeText(win,20,20,"0/0",20)

    #Queues Stuff
    makeText(win,65,90,"Priority Queue",12)
    makeRect(win,40,90,45,85,"white")

    makeText(win,120,90,"Fairness Queue",12)
    makeRect(win,95,145,45,85,"white")

    #Control Buttons
    run100 = Button(win,Point(80,39),20,8,"skyblue","Run 100 Cycles")
    run1 = Button(win,Point(105,39),20,8,"skyblue","Run a Cycle")

    #Process Entry - File
    makeText(win,60,25,"Add all processes from a file",10)
    fileInput = Entry(Point(60, 21), 20)
    fileInput.setText("Chrome.csv")
    fileInput.draw(win)
    addFileButton = Button(win,Point(60,15),18,6,"skyblue","Read File")

    #Process Entry - Single
    makeText(win,95,22,"Add an individual\n process",10)
    addProcButton = Button(win,Point(95,15),14,6,"skyblue","Add")

    makeText(win,133,25,"- Name",9)
    nameInput = Entry(Point(117, 25), 15)
    nameInput.draw(win)

    makeText(win,133,21,"- Priority",9)
    priorityInput = Entry(Point(117, 21), 15)
    priorityInput.draw(win)

    makeText(win,133,17,"- Cycles",9)
    cyclesInput = Entry(Point(117, 17), 15)
    cyclesInput.draw(win)

    makeText(win,137,13,"- Memory Needed",9)
    ramInput = Entry(Point(117, 13), 15)
    ramInput.draw(win)

    ################################################

    priority_list = []
    fairness_list = []

    for proc_number in range(10):
        message = ""
        proc_text = makeText(win,65,80-proc_number*3,message,10)
        priority_list.append(proc_text)

        fairness_message = ""
        fairness_text = makeText(win,120,80-proc_number*3,fairness_message,10)
        fairness_list.append(fairness_text)

    priority = program.Heap()
    fairness = program.Queue(0)
    core1, core1_cycles = program.Process("Empty",0,0,0),0
    core2, core2_cycles = program.Process("Empty",0,0,0),0

    ################################################

    #Main user clicking loop
    pt = win.getMouse()
    while win.isOpen():

        try:
            #Add Process Button Logic
            if addProcButton.isClicked(pt):
                new_process = makeProcessFromInput(nameInput.getText(),
                                     priorityInput.getText(),
                                     cyclesInput.getText(),
                                     ramInput.getText())

                for entry in [nameInput,priorityInput,cyclesInput,ramInput]:
                    entry.setText('')

                priority.insert(new_process)
                fairness.insert(new_process)


            elif addFileButton.isClicked(pt):
                new_processes = makeProcessFromCSV(fileInput.getText())
                fileInput.setText('')

                for proc_object in new_processes:
                    priority.insert(proc_object)
                    fairness.insert(proc_object)

            #Run Button Logic
            if run100.isClicked(pt):
                for cycle in range(100):
                    #Core 1
                    if core1_cycles >= core1.cycles and priority.n > 0:
                        core1 = priority.popMin()
                        fairness.removeItem(core1)
                        core1_cycles = 0
                        c1Cycles.setText(str(core1_cycles)+"/"+str(core1.cycles))
                        c1Name.setText(core1.name)
                    elif core1_cycles <= core1.cycles - 1:
                        core1_cycles += 1
                        c1Cycles.setText(str(core1_cycles)+"/"+str(core1.cycles))
                    elif priority.n <= 0 and core1_cycles >= core1.cycles:
                        core1_cycles = 1
                        core1 = program.Process("Empty",0,0,0)
                        c1Name.setText(core1.name)
                        c1Cycles.setText(str(core1_cycles)+"/"+str(core1.cycles))

                    #Core 2
                    if core2_cycles >= core2.cycles and priority.n > 0:
                        core2 = priority.popMin()
                        fairness.removeItem(core2)
                        core2_cycles = 0
                        c2Cycles.setText(str(core2_cycles)+"/"+str(core2.cycles))
                        c2Name.setText(core2.name)
                    elif core2_cycles <= core2.cycles -1:
                        core2_cycles += 1
                        c2Cycles.setText(str(core2_cycles)+"/"+str(core2.cycles))
                    elif priority.n <= 0 and core2_cycles >= core2.cycles:
                        core2_cycles = 1
                        core2 = program.Process("Empty",0,0,0)
                        c2Name.setText(core2.name)
                        c2Cycles.setText(str(core2_cycles)+"/"+str(core2.cycles))
                        
                    #update fairness cycle values
                    waitedTooLong = fairness.addCycle()
                    for i in waitedTooLong:
                        priority.removeItem(i)
                        fairness.removeItem(i)
                        i.priority = -1
                        priority.insert(i)
                        fairness.insert(i)
                    
                    updateLists(priority_list,fairness_list,priority,fairness)
                    mem.setText(str(16-core1.ram-core2.ram) + " GB")
                    time.sleep(.1)


            elif run1.isClicked(pt):
                #Core 1
                if core1_cycles >= core1.cycles and priority.n > 0:
                    core1 = priority.popMin()
                    fairness.removeItem(core1)
                    core1_cycles = 0
                    c1Cycles.setText(str(core1_cycles)+"/"+str(core1.cycles))
                    c1Name.setText(core1.name)
                elif core1_cycles <= core1.cycles - 1:
                    core1_cycles += 1
                    c1Cycles.setText(str(core1_cycles)+"/"+str(core1.cycles))
                elif priority.n <= 0 and core1_cycles >= core1.cycles:
                    core1_cycles = 1
                    core1 = program.Process("Empty",0,0,0)
                    c1Name.setText(core1.name)
                    c1Cycles.setText(str(core1_cycles)+"/"+str(core1.cycles))
                #Core 2
                if core2_cycles >= core2.cycles and priority.n > 0:
                    core2 = priority.popMin()
                    fairness.removeItem(core2)
                    core2_cycles = 0
                    c2Cycles.setText(str(core2_cycles)+"/"+str(core2.cycles))
                    c2Name.setText(core2.name)
                elif core2_cycles <= core2.cycles -1:
                    core2_cycles += 1
                    c2Cycles.setText(str(core2_cycles)+"/"+str(core2.cycles))
                elif priority.n <= 0 and core2_cycles >= core2.cycles:
                    core2_cycles = 1
                    core2 = program.Process("Empty",0,0,0)
                    c2Name.setText(core2.name)
                    c2Cycles.setText(str(core2_cycles)+"/"+str(core2.cycles))

                #update fairness cycle values
                waitedTooLong = fairness.addCycle()
                for i in waitedTooLong:
                    priority.removeItem(i)
                    fairness.removeItem(i)
                    i.priority = -1
                    priority.insert(i)
                    fairness.insert(i)

            updateLists(priority_list,fairness_list,priority,fairness)
            mem.setText(str(16-core1.ram-core2.ram) + " GB")
            pt = win.getMouse()

        except GraphicsError: break

    print("window closed")


main()
