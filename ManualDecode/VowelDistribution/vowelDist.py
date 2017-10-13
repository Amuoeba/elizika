# -*- coding: utf-8 -*-
import copy
import itertools as it

def FindNext (test,subList):
    for i in subList:
        if test(i):
            return i    
    return False
    
def VowelDistance(txt):
    """Accepts text as a single string. Retuns a multidimensional dictionary whit distances
    between two neighbouring vowels and the count of all vowels. ({"a": {"a":[],"e":[],...}, "e":{"a":[],"e":[],...},.....},count) """
    text = list(enumerate(txt))
    samoglasniki = ["a","e","i","o","u"]
    count = 0
    SpacingDict = {}
    
    
    for s in samoglasniki:
        SpacingDict[s] = {vowel: [] for vowel in samoglasniki}
    
    for char in text:
        if char[1] in samoglasniki:
            count += 1
            pos1 = char[0]
            nxt =FindNext(lambda x: x[1] in samoglasniki, text[pos1+1:])
            if nxt:
                pos2 = nxt[0]            
                distance = pos2 - pos1 -1
                SpacingDict[char[1]][nxt[1]].append(distance) 
            else:
                return (SpacingDict,count)
    
    return (SpacingDict,count)

def Joiner(text,function):
    """Auxilary finction which speeds up the preformance of analisis of one long string.
    It seperates the long string on 50000 long substrings which can be passed, for example, to VovelDistance(txt).
    it accepts the text in a form of a string and a function to wich the text is passed to. It returns a combined dictionary"""
    l = len(text)
    bs = list(range(0,l))
    matrix =bs[0::50000]
    matrix.append(l)
    combined = []
    for i in enumerate(matrix):
        if i[0]+1 <  len(matrix):        
            combined.append(function(text[i[1] : matrix[i[0]+1]]))
    
    WHOLE = combined[0]
    for i in combined[1:]:
        ele = i[0]
        for f in ele:
            for s in ele:
                WHOLE[0][f][s].extend(ele[f][s])
    #TODO: Dodaj še counte, ni pa nujno    
    return WHOLE[0]

def ComputeAverage(dct,distrib = False):
    """Accepts a vovelDict, returned by VowelDistance(txt), and computes the average distance between pairs of vowels.Returns a vowel dict
    with average distances, rather than the list of absolute distances. Allso accepts an optional parameter if we want to obsesrve the distribution of 
    spacings between two vowels. "seperate" --> outputs a nested dictionary of gap distributions for each pair of vowels.
    "combined" --> outputs the gap distributions of all vowels"""
    vowelDict = copy.deepcopy(dct)  
    for i in vowelDict:
        for j in vowelDict:
            summ = 0
            auxList = vowelDict[i][j]
            for n in auxList:
                summ = summ + n
            if len(auxList) != 0:
                vowelDict[i][j] = summ/len(auxList)
            else:
                vowelDict[i][j] = 0
    if distrib == "seperate":
        auxDict1 = copy.deepcopy(dct)
        for i in auxDict1:
            for j in auxDict1:
                distDict = {}
                entryCount= 0
                for distEntry in auxDict1[i][j]:
                    entryCount += 1
                    if distEntry not in distDict:
                        distDict[distEntry] = 1
                    else:
                        distDict[distEntry] = distDict[distEntry] + 1
                for x in distDict:
                    if entryCount != 0:
                        distDict[x] = distDict[x]/entryCount
                    else:
                        distDict[x] = 0
                auxDict1[i][j] = distDict
        return auxDict1
    
    if distrib == "combined":
        auxDict2 = copy.deepcopy(dct)
        combinedDistances = []
        for i in auxDict2:
            for j in auxDict2:
                combinedDistances.extend(auxDict2[i][j])
        combinedDistDict = {}
        for ele in combinedDistances:
            if ele not in combinedDistDict:
                combinedDistDict[ele] = 1
            else:
                combinedDistDict[ele] = combinedDistDict[ele] + 1
        
        for ele in combinedDistDict:
            if len(combinedDistances) != 0:                
                combinedDistDict[ele] = combinedDistDict[ele] / len(combinedDistances)
            else:
                combinedDistDict[ele] = 0
        return combinedDistDict
    return vowelDict

def CankarLetterNeighbours(text,ntupSize=2,seperated=True,sort=False,freq=False):
    """This fuction accepts a text in the form of a list of words, or as a single string. If text is in a form of a list
    the parameter "seperated" must be set to True, if text is in a form of a single string "seperated" must be set to False.
    It accepts 2 optional parameters "sort" and "freq". If "sort" is true the returned value will be a sorted list of tuples, sorted by
    the number of occurances of each n-tuple, else a dictionary object for with n-tuples as keys is returned. If freq is set to true the
    number of occurances will be replaced by frequencies"""
    CountNtup = 0
    if seperated == True:
        ntupFreq = {}
        auxTup = {}
        for word in text:
            for i in range(0,len(word)-ntupSize+1):
                tup = []
                for j in range(0,ntupSize):
                    tup.append(word[i+j])
                tup="".join(tup)
                CountNtup +=1
                if auxTup.get(tup,False) == False:
                    auxTup[tup] = True
                    ntupFreq[tup] = 1
                else:
                    ntupFreq[tup] =ntupFreq[tup] + 1
        if freq:
            for i in ntupFreq:
                ntupFreq[i]=ntupFreq[i]/CountNtup
        
        if sort:
            srt = sorted(ntupFreq.items(), key=lambda x: x[1],reverse=True)
         
            return srt
        else:
            return ntupFreq
    else:
        ntupFreq = {}
        auxTup = {}
        word = text
        for i in range(0,len(word)-ntupSize+1):
                tup = []
                for j in range(0,ntupSize):
                    tup.append(word[i+j])
                tup="".join(tup)
                CountNtup +=1
                if auxTup.get(tup,False) == False:
                    auxTup[tup] = True
                    ntupFreq[tup] = 1
                else:
                    ntupFreq[tup] =ntupFreq[tup] + 1
        if freq:
            for i in ntupFreq:
                ntupFreq[i]=ntupFreq[i]/CountNtup
        if sort:
            srt = sorted(ntupFreq.items(), key=lambda x: x[1],reverse=True)
            return srt
        else:
            return ntupFreq

def VowelCombinations(letterMap,letters):
    """Accepts a decyphering dictionary, and list of letters. Returns a list of dictionaries, which are all possible combinations of maps
    for the given letters"""
    Keys = list(letterMap)
    if "\n" in Keys:
        Keys.remove("\n")
    KeyComb = list(it.combinations(Keys,len(letters)))    
    dictCombinations = [zip(x,letters) for x in KeyComb]
    for i in range(0,len(dictCombinations)):
        dictCombinations[i] = dict(list(dictCombinations[i]))
    for i in  dictCombinations:
        for j in Keys:
            if j not in i:
                i[j] = "*"
    for i in dictCombinations:
        i["\n"] = "\n"
    return dictCombinations

def distribMetric(ref,inQ):
    """Accepts a reference dictionary of vowel distributions and a dictionary in question of 
    vowel distributions. Returns a distance between the two dictionaries"""
    reference = dict(ref)
    inQuestion = dict(inQ)
    for i in reference:
        if i not in inQuestion:
            inQuestion[i] = 0
    for i in inQuestion:
        if i not in reference:
            reference[i] = inQuestion[i] * 100
    SquareDifference = 0
    for i in reference:
        dif=(pow(reference[i]-inQuestion[i],2))
        SquareDifference = SquareDifference + dif
    return SquareDifference

def CypherTextVowelDist(text,dictList,ref):
    """Accepts the text you want to decypher, list of dictionaries returned by VowelCombinations(letterMap,letters) and
    a refference vowel gap distributions (calculated from a corpora). Returns a list of maps that create a similar vowel gap distribution
    as the corpora text. The metric to determine similarities between two vowel gap distributions is square difference"""
    textList = []
    distribList = []
    ProminentMaps =[]
    for i in dictList:
        newText = []
        for letter in text:
            newText.append(i[letter])
        newText="".join(newText)
        textList.append((newText,i))
    for txt in textList:
        vowelSpacings = VowelDistance(txt[0])
        vowelDistributions = ComputeAverage(vowelSpacings[0],distrib="combined")
        distribList.append((vowelDistributions,txt[1]))
    for i in distribList:
        SqDif=distribMetric(ref,i[0])
        ProminentMaps.append((SqDif,i[0],i[1]))
    ProminentMaps.sort(key=lambda x: x[0])
    return ProminentMaps

def whichCharMoreCommon(dictList):
    """Takes the data produced by CypherTextVowelDist(eliza,dictComb,analisisTogether)[:50] and returns a sorted list
    of characters that occur in potential vowelMaps most often"""
    dictList = [x[2] for x in dictList]
    charFreq ={}
    count = 0
    for item in dictList:
        for char in item:
            if item[char] != "*":
                if char not in charFreq:
                    charFreq[char] = 1
                    count += 1
                else:
                    charFreq[char] = charFreq[char] +1
                    count += 1
    for item in charFreq:
        charFreq[item] = charFreq[item]/count 
    del charFreq["\n"]
    srt = sorted(charFreq.items(), key=lambda x: x[1],reverse=True)    
    return srt

