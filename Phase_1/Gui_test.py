from graphics import *

def makeRect(gwin,x1,x2,y1,y2,color):
    rec = Rectangle(Point(x1,y1),Point(x2,y2))
    rec.setFill(color)
    rec.draw(gwin)

def makeText(gwin,x,y,text,size):
    guiText = Text(Point(x,y),text)
    guiText.setSize(size)
    guiText.draw(gwin)
    return guiText

class Button:
    def __init__(self, gwin, centerPoint, width, height, color, lable):
        self.point1 = Point(centerPoint.getX()+width/2, centerPoint.getY()+height/2)
        self.point2 = Point(centerPoint.getX()-width/2, centerPoint.getY()-height/2)
        
        buttonRec = Rectangle(self.point1,self.point2)
        buttonRec.setFill(color)
        buttonRec.draw(gwin)
        
        text = Text(centerPoint,lable)
        text.draw(gwin)

    def isClicked(pt):
        if pt.getX() >= self.point1.getX() and pt.getY() >= self.point1.getY() and \
            pt.getX() <= self.point2.getX() and pt.getY() <= self.point2.getY():
            return True
        return False
            

def main():
    win = GraphWin("Process Scheduler", 900,600)
    win.setBackground("lightblue")
    win.setCoords(1,1,150,100)

    #Memory
    makeText(win,17,93,"Memory Availible:",15)
    mem = makeText(win,40,93,"X Gigs",15)

    #Cores Stuff
    makeText(win,20,83,"Core 1",12)
    makeRect(win,5,35,50,80,"white")
    c1Name = makeText(win,20,72,"<Process Name>",10)
    makeText(win,20,66,"Cycles",10)
    c1Cycles = makeText(win,20,60,"3/5",20)
    
    makeText(win,20,43,"Core 2",12)
    makeRect(win,5,35,10,40,"white")
    c2Name = makeText(win,20,32,"<Process Name>",10)
    makeText(win,20,26,"Cycles",10)
    c2Cycles = makeText(win,20,20,"3/5",20)

    #Queues Stuff
    makeText(win,65,90,"Priority Queue",12)
    makeRect(win,40,90,45,85,"white")
    makeRect(win,83,90,45,85,"white")
    makeText(win,43,65,"1.\n\n2.\n\n3.\n\n4.\n\n5.\n\n6.\n\n7.",10)

    makeText(win,120,90,"Fairness Queue",12)
    makeRect(win,95,145,45,85,"white")
    makeRect(win,138,145,45,85,"white")
    makeText(win,98,65,"1.\n\n2.\n\n3.\n\n4.\n\n5.\n\n6.\n\n7.",10)

    #Control Buttons
    play = Button(win,Point(72.5,39),14,8,"skyblue","Play")
    pause = Button(win,Point(92.5,39),14,8,"skyblue","Pause")
    nextC = Button(win,Point(112.5,39),14,8,"skyblue",">>")

    #Process Entry - File
    makeText(win,60,25,"Add all processes from a file",10)
    fileInput = Entry(Point(60, 21), 20)
    fileInput.draw(win)
    addFile = Button(win,Point(60,15),18,6,"skyblue","Read File")

    #Process Entry - Single
    makeText(win,95,22,"Add an individual\n process",10)
    addProc = Button(win,Point(95,15),14,6,"skyblue","Add")

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


main()
