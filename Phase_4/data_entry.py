# Data Entry Module for Phase 4
#
# Team Battlefield

"""

This provides a set of functions, and two main functions, to validate and
return a list of Process objects.

####################################
code to use in another module:

if isGoodToGo(YOURFILENAME):
    my_processes = makeProcesses(YOURFILENAME,iodir)
else:
    return "Your File Is Trash and Made Me Error"

####################################


"""

from Data_Structures_4 import *

def isGoodToGo(infile):
##    ''' Returns True if file clears tests for data integrity '''
##    table = csvReader(infile)
##    data = clearHeaders(table)
##    cleanTable = clearHeadersInCells(data)
##
##    for row in cleanTable:
##        for cell in row[1:]:
##            if not isPosInt(cell):
##                return False
##
##    try:
##        makeProcesses(infile)
##    except:
##        return False
##    return True

    ''' Returns True if file clears tests for data integrity '''
    try:
        table = csvReader(infile)
        data = clearHeaders(table)
        cleanTable = clearHeadersInCells(data)

        for row in cleanTable:
            for cell in row[1:]:
                if not isPosInt(cell):
                    return False

        makeProcesses(infile)
        
        return True

    except:
        return False

def makeProcesses(infile):
    ''' Create process object for each row in file '''
    table = csvReader(infile)
    data = clearHeaders(table)
    cleanTable = clearHeadersInCells(data)

    return [Process(row[0], int(row[1]), int(row[2]), int(row[3]), int(row[4]), int(row[5])) for row in cleanTable]


################################################################################


def isPosInt(num):
    '''Returns True if value could be converted to a positive integer '''
    try:
        if int(num) >= 0:
            return True

    except ValueError:
        return False

def csvReader(infile):
    ''' Module to read csv file and return a list of lists (an indexable table)
        We don't use Python's built-in CSV reading module just because it's a bit tedious
    '''

    with open(infile,'r') as file:
        file = file.read().split('\n')
        lines = [line.split(',') for line in file]

    return lines

def clearHeaders(data):
    ''' Returns table without headers, if they exist'''
    if data[0][0].lower() == 'name':
        data = data[1:]
    return data

def clearHeadersInCells(data):
    ''' Returns table where variable names are cleared from cellsself.

        For example, 'arrival time = 6' goes to '6'
    '''

    newData = []
    for row in data:
        newRow = []
        if len(row) > 1:
            for cell in row:
                if "=" in cell:
                    cell = cell.split('=')[-1].strip()
                newRow.append(cell)
            newData.append(newRow)

    return newData
