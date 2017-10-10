class Cypher:
    """This class provides basic cypher text analysis"""
    
    def __init__(self,text):
        self.Text = text.replace("\n","")
        self.Length = len(self.Text)
        self.Ntups = self.Ntuples(3,freq=True)
        self.Alphabet = None
        self.Map = self.__InitMap__()
        
    def __InitMap__(self):
        """Initializes a character map to a blank map where each character maps to "*" """
        initialMap = {}
        for i in self.Text:
            if i not in initialMap:
                initialMap[i] = "*"
        return initialMap
                
    def setAlphabet(self,alphabet):
        """Sets alphabet for the cypher. Accepts a list of characters which represent the alphabet"""
        self.Alphabet = alphabet
    
    def setCustomMap(self,charMap):
        """"Sets Map to a custom map (keys must be all characters found in the cypher text)"""
        self.Map = charMap
    
    def Ntuples(self,N,freq=False):
        """ Returns a dictionary of lists of N-tuples sorted by number of occurances. Starting from 1 up to N.
        If optional parameter freq is set to True N-tuples are returned with coresponding frequencies instead"""
        ntups = {}
        for n in range(1,N+1):
            count = 0
            freqTups={}
            tups = [self.Text[i:i+n] for i in range(0,len(self.Text))]        
            
            for tup in tups:
                if tup in freqTups:
                    freqTups[tup] = freqTups[tup] + 1
                    count += 1
                else:
                    freqTups[tup] = 1
                    count += 1
            orderTups = sorted(list(freqTups.items()),key=lambda x: x[1],reverse = True)
            if freq:
                orderTups = [(x[0],x[1]/count) for x in orderTups]
            
            cleanedTups =list(filter(lambda x: len(x[0]) == n,orderTups))
            ntups[n] = cleanedTups        
        return ntups    
    
#TODO Calculate index of coincidence for given cypher text
#TODO Calculate gap distributions to determine potential vowels
#TODO Calculate probability of text based on 2-tuples
#TODO Implement different kinds of prints to eaze manual decoding
#TODO Implement filter function for dictionary attack
            
        
            