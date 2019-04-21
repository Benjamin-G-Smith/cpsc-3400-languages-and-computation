"""
Ben Smith
Python Assignment 2
5/7/2018
Family Trees

GEDCOM parser design

Create empty dictionaries of individuals and families
Ask user for a file name and open the gedcom file
Read a line
Skip lines until a FAM or INDI tag is found
    Call functions to process those two types
Print descendant chart when all lines are processed

Processing an Individual
Get pointer string
Make dictionary entry for pointer with ref to Person object
Find name tag and identify parts (surname, given names, suffix)
Find FAMS and FAMC tags; store FAM references for later linkage
Skip other lines

Processing a family
Get pointer string
Make dictionary entry for pointer with ref to Family object
Find HUSB WIFE and CHIL tags
    Add included pointer to Family object
    [Not implemented ] Check for matching references in referenced Person object
        Note conflicting info if found.
Skip other lines

Print info from the collect of Person objects
Read in a person number
Print pedigree chart
"""


#-----------------------------------------------------------------------

class Person():
    # Stores info about a single person
    # Created when an Individual (INDI) GEDCOM record is processed.
    #-------------------------------------------------------------------

    def __init__(self,ref):
        # Initializes a new Person object, storing the string (ref) by
        # which it can be referenced.
        self._id = ref
        self._asSpouse = []  # use a list to handle multiple families
        self._asChild = None
        self._events = None

    def addName(self, nameString):
        # Extracts name parts from nameString and stores them
        names = line[6:].split('/')  #surname is surrounded by slashes
        self._given = names[0].strip()
        self._surname = names[1]
        self._suffix = names[2].strip()
    def addEvent(self, listOfEvent, type):
        if not self._events:
            self._events = Event(self._id)
        if type == 'birth':
            self._events.addBirthEvent(listOfEvent)
        elif type == 'death':
            self._events.addDeathEvent(listOfEvent)
        elif type == 'marr':
            self._events.addMarriageEvent(listOfEvent)

    def isDescendant(self, person):
        # Method used to find the descendants of a person given an ID
        if person == self._id:
            return True
        else:
            for fam in self._asSpouse:
                if families[fam].isDescendant(person):
                    return True

    def addIsSpouse(self, famRef):
        # Adds the string (famRef) indicating family in which this person
        # is a spouse, to list of any other such families
        self._asSpouse += [famRef]

    def addIsChild(self, famRef):
        # Stores the string (famRef) indicating family in which this person
        # is a child
        self._asChild = famRef
    def printAncestors(self, prefix=''):
        # Used to print all of the given ancestors for a person
        famID = self._asChild
        if self._asChild:
            families[self._asChild].printAncestors(famID, prefix)
    def getAncestorsList(self):
        # returns a list of ancestors for closestCommonAncestor
        list = []
        self.getAncestors(list)
        return list
    def getAncestors(self, list):
        # Helper method used to build a list of ancestors
        famID = self._asChild
        if self._asChild:
            families[self._asChild].getAncestors(famID, list)

        return list
    def printDescendants(self, prefix=''):
        # print info for this person and then call method in Family
        #if self._events != None:
        print(prefix + self.__str__())
        # recursion stops when self is not a spouse
        for fam in self._asSpouse:
            families[fam].printFamily(self._id,prefix)

    def __str__(self):
        eventStr = ''
        if self._events != None:
            eventStr = self._events.getEventRecords()
        else:
            eventStr = ' '
        if self._asChild: # make sure value is not None
            childString = ' asChild: ' + self._asChild
        else: childString = ''
        if self._asSpouse != []: # make sure _asSpouse list is not empty
            spouseString = ' asSpouse: ' + str(self._asSpouse)
        else: spouseString = ''
        return self._given + ' ' + self._surname.upper()\
               + ' ' + self._suffix + eventStr
#               + childString + spouseString


#-----------------------------------------------------------------------
class Event():
    # Stores info about a single Event for a person
    # Created when an Individual (INDI) GEDCOM record is processed.
    #-------------------------------------------------------------------
    def __init__(self, ref):
        # Initializes a new Event object, storing the string (ref) by
        # which it can be referenced.
        self._personId = ref
        self._birthEvent = ''
        self._deathEvent = ''
        self._marriageEvent = ''

    def cleanInfo(self,List):
        # Cleans the line for processing items in an event
        cleanList = []
        for info in List:
            line = info.strip().split(' ')
            for elements in range(len(line)-2):
                cleanList.append(line[elements+2])
        return cleanList

    def addBirthEvent(self, Details):
        # adds a new birth event with the details to the event object
        content = self.cleanInfo(Details)
        self._birthEvent += ", [n]"
        for info in content:
            self._birthEvent += " " + str(info)

    def addDeathEvent(self, Details):
        # Adds a new death event ot the event object with dedails
        content = self.cleanInfo(Details)
        self._deathEvent += ", [d]"
        for info in content:
            self._deathEvent += " " + str(info)

    def addMarriageEvent(self, Details):
        # Adds a new marriage event to the Event object
        content = self.cleanInfo(Details)
        self._marriageEvent += ", [m]"
        for info in content:
            self._marriageEvent += " " + str(info)

    def getEventRecords(self):
        # Builds a concatinated string of the event objects events
        return self._birthEvent + ' '+ self._deathEvent + ' ' + self._marriageEvent


#-----------------------------------------------------------------------

class Family():
    # Stores info about a family
    # Created when an Family (FAM) GEDCOM record is processed.
    #-------------------------------------------------------------------

    def __init__(self, ref):
        # Initializes a new Family object, storing the string (ref) by
        # which it can be referenced.
        self._id = ref
        self._husband = None
        self._wife = None
        self._children = []

    def addHusband(self, personRef):
        # Stores the string (personRef) indicating the husband in this family
        self._husband = personRef

    def addWife(self, personRef):
        # Stores the string (personRef) indicating the wife in this family
        self._wife = personRef

    def addChild(self, personRef):
        # Adds the string (personRef) indicating a new child to the list
        self._children += [personRef]
    def addEvent(self, listOfEvent, type):
        if self._wife:
            persons[self._wife].addEvent(listOfEvent, type)
        if self._husband:
            persons[self._husband].addEvent(listOfEvent, type)

    def isDescendant(self, descendantId):
        for child in self._children:
            if persons[child].isDescendant(descendantId):
                return True
    def getAncestors(self,person, list):
        fam = families[person]
        if fam:
            if self._wife:
                list.append(str(persons[self._wife]))
                persons[self._wife].getAncestors(list)
            if self._husband:
                list.append(str(persons[self._husband]))
                persons[self._husband].getAncestors(list)


    def printAncestors(self, person ,prefix):
        # Given a person ID and the prefix of that person this
        # function prints the husband and wife of the child given
        # eventually building the tree of ancestors
        # Note: Printing is not as neat however, it prints in pairs
        # starting from the hightest relatives to the child ID given

        fam = families[person]
        if fam:
            if self._wife:
                persons[self._wife].printAncestors(prefix+' ')
            if self._husband:
                persons[self._husband].printAncestors(prefix+'  ')
        if self._wife:
            print(prefix + str(persons[self._wife]))
        if self._husband:
            print(prefix + str(persons[self._husband]) + "\n")


    def printFamily(self, firstSpouse, prefix):
        # Used by printDecendants in Person to print spouse
        # and recursively invole printDescendants on children
        if prefix != '': prefix = prefix[:-2]+'  '
        if self._husband == firstSpouse:
            if self._wife:  # make sure value is not None
                print(prefix+ '+' +str(persons[self._wife]))
        else:
            if self._husband:  # make sure value is not None
                print(prefix+ '+' +str(persons[self._husband]))
        for child in self._children:
             persons[child].printDescendants(prefix+'|--')

    def __str__(self):
        if self._husband: # make sure value is not None
            husbString = ' Husband: ' + self._husband
        else: husbString = ''
        if self._wife: # make sure value is not None
            wifeString = ' Wife: ' + self._wife
        else: wifeString = ''
        if self._children != []: childrenString = ' Children: ' + str(self._children)
        else: childrenString = ''
        return husbString + wifeString + childrenString


#-----------------------------------------------------------------------

def getPointer(line):
    # A helper function used in multiple places in the next two functions
    # Depends on the syntax of pointers in certain GEDCOM elements
    # Returns the string of the pointer without surrounding '@'s or trailing
    return line[8:].split('@')[0]

def processPerson(newPerson):
    global line
    line = f.readline()
    while line[0] != '0': # process all lines until next 0-level
        event = False
        tag = line[2:6]  # substring where tags are found in 0-level elements
        if tag == 'NAME':
            newPerson.addName(line[7:])
        elif tag == 'FAMS':
            newPerson.addIsSpouse(getPointer(line))
        elif tag == 'FAMC':
            newPerson.addIsChild(getPointer(line))
        elif tag == 'BIRT':
            birt = []
            birt.append(line)
            line = f.readline()
            while(line[0] != '1' and line[0] != '0'):
                birt.append(line)
                line = f.readline()
            event = True
            newPerson.addEvent(birt,'birth')
            birt.clear()
        elif tag == 'DEAT':
            deat = []
            deat.append(line)
            line = f.readline()
            while(line[0] != '1' and line[0] != '0'):
                deat.append(line)
                line = f.readline()
            event = True
            newPerson.addEvent(deat,'death')
            deat.clear()

        # read to go to next line
        if not event :
            line = f.readline()

def processFamily(newFamily):
    global line
    line = f.readline()
    while line[0] != '0':  # process all lines until next 0-leve
        event = False
        tag = line[2:6]
        if tag == 'HUSB':
            newFamily.addHusband(getPointer(line))
        elif tag == 'WIFE':
            newFamily.addWife(getPointer(line))
        elif tag == 'CHIL':
            newFamily.addChild(getPointer(line))
        elif tag == 'MARR':
            marr = []
            marr.append(line)
            line = f.readline()
            while(line[0] != '1' and line[0] != '0'):
                marr.append(line)
                line = f.readline()
            event = True
            newFamily.addEvent(marr, 'marr')
            marr.clear()
        # read to go to next line
        if not event :
            line = f.readline()

def closestCommonAncestor(personID_1, personID_2):
    # Builds two lists containing all of the ancestors of each persons
    # From those lists the closest common ancestor is determined
    p1_ancestors = []
    p2_ancestors = []
    p1_ancestors = persons[personID_1].getAncestorsList()
    p2_ancestors = persons[personID_2].getAncestorsList()

    found = False
    close = None
    for p1 in p1_ancestors:
        for p2 in p2_ancestors:
            if p1 == p2 and not found:
                close = p1
                found = True
    print("Closest common ancestor is: ",close)
    close = None

def testIsDescendant(person, newID):
    # Tests is descendant function
    if persons[person].isDescendant(newID):
        print("Prints ancestors of descendant")
        print("--------------------------------------------")
        print("["+newID + "isDescendant of " + person+"]")
        return True
    else:
        print("[ No descendant found ]")
        return False

def testPrintAncestors(newID):
    # Tests print ancestor function
    print(persons[newID].printAncestors())
    print(str(persons[newID]))
    print("Prints oldest ancestor first")
    print("--------------------------------------------")

def testClosestComonAncestor():
    # Tests closest common ancestor function
    print("Closest common ancestor Enter two people:")
    p1 = input("Enter p1: ")
    p2 = input("Enter p2: ")
    closestCommonAncestor(p1,p2)
    print("--------------------------------------------")

def continue_Processing():
    # Used to keep the program running
    continue_ = input("Do you want to keep searching ['y'/'n']?: ").lower()
    return continue_ != 'y'
## Main program starts here

persons = {}  # to save references to all of the Person objects
families = {} # to save references to all of the Family objects

#filename = "Kennedy.ged"  # Set a default name for the file to be processed

### Uncomment the next line to make the program interactive
filename = input("Type the name of the GEDCOM file:")

f = open (filename)

line = f.readline()
while line != '':  # end loop when file is empty
    fields = line.strip().split(' ')
    if line[0] == '0' and len(fields) > 2:
        # print(fields)
        if (fields[2] == "INDI"):
            ref = fields[1].strip('@')
            persons[ref] = Person(ref)  ## store ref to new Person
            processPerson(persons[ref])
        elif (fields[2] == "FAM"):
            ref = fields[1].strip('@')
            families[ref] = Family(ref) ## store ref to new Family
            processFamily(families[ref])
        else:    # 0-level line, but not of interest -- skip it
            line = f.readline()
    else:    # skip lines until next candidate 0-level line
        line = f.readline()


# Optionally print out all information stored about individuals
for ref in sorted(persons.keys()):
   print(ref+':', persons[ref])

# Optionally print out all information stored about families
for ref in sorted(families.keys()):
    print(ref+':', families[ref])

##person = "I46"  # Default selection to work with Kennedy.ged file
### Uncomment the next line to make the program interactive

done = False
while not done:
    person = input("Enter person to print [Descendant] tree: ")
    persons[person].printDescendants(person)
    newID = input("Enter descendatn to check for:")
    print("--------------------------------------------")

    if testIsDescendant(person, newID):
        testPrintAncestors(newID)

    testClosestComonAncestor()
    done = continue_Processing()


f.close()
