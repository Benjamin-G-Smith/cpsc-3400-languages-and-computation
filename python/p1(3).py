'''
    Ben Smith
    Project #1 File searching
    4/19/2018
'''


import os
import string
import math

punct = set(string.punctuation)
def getFileList(directoryName):
    '''
    Given a directory name (path) as a string, returns a list of file paths for
    files contained in that directory.
    INPUT: directoryName is a string containing a relative or absolute path for a directory
    RETURNS: a list containing the file paths (as strings) of all files within the directory
    RAISES: FileNotFoundError if the directoryName does not exist,
            NotADirectoryError if the directoryName is not a directory (e.g., if it's a regular file)
            ValueError if the directoryName contains characters that render it an invalid path name
    '''
    fileList = os.listdir(directoryName)
    fileList = [directoryName + '/' + file for file in fileList if not file.startswith('.')] # append file name to directory, and ignore hidden files
    fileList = [file for file in fileList if os.path.isfile(file)] # include only actual files (not directories)
    return fileList

def removePunct(line):
    '''Removes all punctuation from a given string (line)'''
    return ''.join(x for x in line if x not in punct)
def removeNumbers(line):
    '''Removes all numbers from the document'''
    return ''.join(x for x in line if not x.isdigit())

def setWordList(file):
    '''Strips the files of punctuation and any other unessary characters. Then adds the words in a
        line into a set to be accessed later.
        Inputs: A valid file to be worked in
        Returns: None
        Results: Words and their occurences are added to a master dictionary to be used later.
    '''
    sets = {}
    with open(file) as doc:
        lines = doc.readlines()
        for line in lines:
            line = removeNumbers(line)
            cleanLine = removePunct(line)
            cleanLine = cleanLine.strip().lower()
            list = cleanLine.split(' ')
            for items in list:
                key = items
                if key in sets:
                    sets[key] += 1
                else:
                    sets[key] = 1
        wordAppearanceInDocs.append(sets)

def getOccurences(word,lists):
    ''' Return the number of times a word appears in a document
        Inputs: A Word and the list of words for a particular document
        Returns: The number of occurences for a word in a file if it is in the file
    '''
    found = False
    for items in lists:
        if items == word:
            found = True

    if found:
        userInput[word] += 1
        return lists[word]
    else:
        return 0

def setOccurencesInDocs(word):
    '''Preforms the main functionality of the program
        Gets the occurences for a particualr word, creating a list of documents and values
    '''
    for lists in wordAppearanceInDocs:
        oc = getOccurences(word, lists)
        '''Sets the document with the oc count for a word doc[] = #oc of that word'''
        values[documentList[wordAppearanceInDocs.index(lists)]] = oc
        '''# oc of word '''
        inputOc[word] = oc


def end():
    '''Function to let the user know the program is finished'''
    print("Goodbye...")

def run():
    '''Validates user input to run the program'''
    userInput = input("Would you like to query for a string ['y'/'n']: ").lower()
    return userInput == 'y'

def calcValue(word):
    '''
        Calculates the TF-IDF value for a given word
        Inputs: A word to find the value for
        Returns: The calculated value of the word or zero if the word does not appear in the doc
    '''
    max = 0
    doc = ''
    '''max is the finds the most frequent occutence of a word'''
    for items in documentList:
        if max < values[items]:
            doc = items
            max = values[items]
            '''Gives the maximum value for highest occurences in the most relavent doc'''
    if userInput[word] != 0:
        temp = float(numDocs)/(float(userInput[word]))
        IDF = math.log(temp)
        TFIDF = 0
        TFIDF = IDF * float(max)
        return TFIDF
    else:
        return 0

def getHighestDoc():
    '''For a gven word finds the largest number of occurences in a doc related to that word
    Inputs: None
    Returns: the string of the path to the document most relevent to the query
    '''
    
    doc = ''
    max = 0
    for items in documentList:
        if max < values[items]:
            doc = items
            max = values[items]

    return doc

def loadFiles(fileList):
    '''
        Tries to open all files in a given directory. If a file fails to open then a error message is
        given to the user.
        Inputs: a fileList containing the pahs to all files in a given directory
        Returns: The total number of documents avalible to be used in a directory
    '''
    docs = 0
    for doc in fileList:
        try:
            f = open(doc, 'rb')
            docs += 1
            documentList.append(doc)
            f.close()
        except IOError:
            print("Could not read file:", f)
            docs -= 1
            f.close()
    print("Loading Document Files")
    for file in fileList:
        setWordList(file)
    print("Directory Files Loaded...")
    return docs

def getMostRelivent(results):
    '''
        Finds the most relevent file for a given string of words
        Inputs: a list of dictionaries that contain information about files and word counts in each
        Returns: The string containing the most relevent word,file, and value for a given string query
    '''
    maxV = 0
    doc = ''
    key = ''
    for i in range(0, len(results)):
        if maxV < results[i]['value']:
            doc = results[i]['path']
            maxV = results[i]['value']
            key = results[i]['word']

    return " Input: "+ key + " Value: " + str(maxV) +" Path: "+ doc

'''--------------------------------------------------------------'''


directory = input("Enter Your Directory Path: ")
userInput = {}
inputOc = {}
values = {}
results = []
'''List containing the dictionary of each files words and their frequency'''
wordAppearanceInDocs = []
documentList = []

fileList = getFileList(directory)
done = run()
'''numDocs = len(documentList)'''
numDocs = loadFiles(fileList)

'''Main loop of program'''
while(done):
    searchSrt = input("Search:")
    if(searchSrt != '\n'):
        searchSrt = removePunct(removeNumbers(searchSrt)).strip().lower()
        searchList = searchSrt.split()
        setResults = {}
        for word in searchList:
            '''Creates a set for the word,value, and path for file with most oc of word'''
            inputOc[word] = 0
            userInput[word] = 0
            setOccurencesInDocs(word)
            setResults['word'] = word
            setResults['value'] = calcValue(word)
            setResults['path'] = getHighestDoc()
            results.append(setResults.copy())
        '''list of top three values from the values dictionary'''
        topValues = [(item, values[item]) for item in sorted(values, key=values.get, reverse=True)][:3]
        queryString = getMostRelivent(results)
        print("Most Relevent Documents: ")
        for items in topValues:
            print(items)
        print(queryString)
        results[:] = []
        userInput.clear()
        values.clear()
        done = run()
end()
























this = 0
