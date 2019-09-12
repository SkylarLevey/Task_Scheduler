#Pfizer I Hardly Know Her!

class Process:
    def __init__(self, name, priority, cycles, ram):
        self.name = name
        self.cycles = cycles
        self.priority = priority
        self.ram = ram
        self.cyclesWaited = 0

class Queue:
    def __init__(self, priority):
        self.Q = [priority]
    def insert(self, process):
        self.Q.append(process)
    def popTop(self):
        if len(self.Q) >= 2:
            return self.Q.pop(1)

class Heap:
    def __init__(self): 
        self.heap = []  

    def insert(self, process):
        priorityValInHeap = False
        for q in self.heap:
            if q.Q[0] == process.priority:
                q.insert(process)
                priorityValInHeap = True
        if not priorityValInHeap:
            newQueue = Queue(process.priority)
            newQueue.insert(process)
            self.heap.append(newQueue)
            index = len(self.heap) - 1
            while(self.heap[self.parent(index)].Q[0] > self.heap[index].Q[0] and index > 0):
                self.swop(index,self.parent(index))
                index = self.parent(index)

    def popMin(self):
        val = self.heap[0].popTop()
        if len(self.heap[0].Q) <= 1:
            self.swop(0,len(self.heap)-1)
            self.heap.pop(len(self.heap)-1)
            index = 0

            stopSwitching = False
            while index*2+1 <= len(self.heap)-1 and not stopSwitching:
                if index*2+2 <= len(self.heap)-1:
                    if self.heap[index*2+1].Q[0] < self.heap[index].Q[0] and self.heap[index*2+2].Q[0] < self.heap[index].Q[0]:
                        if self.heap[index*2+2].Q[0] > self.heap[index*2+1].Q[0]:
                            self.swop(self.heap[index*2+1].Q[0],self.heap[index].Q[0])
                            index = index*2+1
                        else:
                            self.swop(self.heap[index*2+2].Q[0],self.heap[index].Q[0])
                            index = index*2+2
                    elif self.heap[index*2+1].Q[0] < self.heap[index].Q[0]:
                        self.swop(self.heap[index*2+1].Q[0],self.heap[index].Q[0])
                        index = index*2+1
                    elif self.heap[index*2+2].Q[0] < self.heap[index].Q[0]:
                        self.swop(self.heap[index*2+2].Q[0],self.heap[index].Q[0])
                        index = index*2+2
                    else:
                        stopSwitching = True
                else:
                    if self.heap[index*2+1].Q[0] < self.heap[index].Q[0]:
                          self.swop(self.heap[index*2+1].Q[0],self.heap[index])
                    stopSwitching = True
        return val

    def swop(self, x, y):
        temp = self.heap[x]
        self.heap[x] = self.heap[y]
        self.heap[y] = temp

    def parent(self,x):
        if x%2 == 1:
            return x//2
        else:
            return (x-1)//2



def test():
    Fairness = Queue(0)
    Priority = Heap()

    p = [Process("div", 5, 6, 6),Process("ex", 5, 6, 6),Process("log", 5, 6, 6),
         Process("add", 3, 6, 6),Process("sub", 1, 6, 6),Process("mult", 1, 6, 6)]
         
    for i in p:
        Fairness.insert(i)
        Priority.insert(i)
    for i in Fairness.Q:
        if i != 0:
            print(i.name)
    print("\n")
    for i in Priority.heap:
        print(i.Q[0],len(i.Q),i.Q)
    for i in range(6):
        p = Priority.popMin()
        print(p.name,p.priority)
        #for i in Priority.heap:
        #    print(i.Q[0],len(i.Q),i.Q)
    
#test()
                
    
    
