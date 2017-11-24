# -*- coding: utf-8 -*-
import re, string, random, glob, operator, heapq
from collections import defaultdict
from math import log10
import functools
import pickle
import codecs
import sys
sys.setrecursionlimit(10000)

###########################################################
# Setting up word count and alphabet used in segmentation #
###########################################################

N=252960
#for english

N=0

#alphabet = 'abcdefghijklmnopqrstuvwxyz'
#with open("englishWordCountDump.txt","rb") as myfile:
#    WordFrequencies= pickle.load(myfile)

alphabet = 'abcčdefghijklmnoprsštuvzž'    
with open("./SlovenianCorpus/cankarCountDUMP.txt","rb") as myfile:
    WordFrequencies= pickle.load(myfile)

for i in WordFrequencies:
    N = N + WordFrequencies[i]
    
##################################################
# Calculating the probability of an unknown word #
##################################################
    
def probabilityOfUnknown(word,N):
    """Estimates the probability of an unknown word"""
    return 10.0/(N*100**(len(word)))

def WordProbability(word,wordFreqDict,N):
    if word in wordFreqDict:
        return wordFreqDict[word]/N
    else:
        return probabilityOfUnknown(word,N)

##################################
# Segmenting text without spaces #
################################## 
        
def memo(f):
    "Memoize function f."
    table = {}
    def fmemo(*args):
        if args not in table:
            table[args] = f(*args)
        return table[args]
    fmemo.memo = table
    return fmemo

def product(numList):
    """Returns a product of a list of numbers"""
    return functools.reduce(operator.mul, numList,1)


def splits(text, L=20):
    """Returns a list of all possible splits (first,rem) where len(first)<L"""
    return[(text[:i+1],text[i+1:]) for i in range(min(len(text),L))]
    
def Pword(words):
    """The naive bayes probability of a sequence of words."""
    return product(WordProbability(w,WordFrequencies,N) for w in words)

@memo
def segment(text):
    """Retruns a list of words that is the best segmentation for the text"""
    if not text:
        return []
    else:
        candidates=([first]+segment(rem)for first,rem in splits(text))
        return max(candidates, key=Pword)
    
###########################
#Encoding a custom message#
###########################
def encode(msg, key): 
    "Encode a message with a substitution cipher." 
    return msg.translate(str.maketrans(ul(alphabet), ul(key))) 

def ul(text): return text.upper() + text.lower() 

def allwords(text): 
    "Return a list of alphabetic words in text, lowercase." 
    return text.split()
######################################
# Loading files with N-tupple counts #
######################################

N1=0
N2=0
#with open("english2Ndump.txt","rb") as myfile1:
#    N2gramDict= pickle.load(myfile1)
#with open("english3Ndump.txt","rb") as myfile2:
#    N3gramDict= pickle.load(myfile2)

with open("./SlovenianCorpus/CankarXXtupleDUMP.txt","rb") as myfile:
    N2gramDict= pickle.load(myfile)
with open("./SlovenianCorpus/CankarXXXtupleDUMP.txt","rb") as myfile:
    N3gramDict= pickle.load(myfile)

for i in N2gramDict:
    N2 = N2 + N2gramDict[i]
for i in N3gramDict:
    N1 = N1 + N3gramDict[i]
###################################
# Auxilary funcions for Hillclimb #
###################################
    
def ngrams(seq, n):
    "List all the (overlapping) ngrams in a sequence."
    return [seq[i:i+n] for i in range(1+len(seq)-n)]
def logP3grams(text): 
    "The Naive Bayes probability of a string or sequence of words. based on N gram probability" 
    words = ngrams(text,3)    
    return sum([log10(WordProbability(x,N3gramDict,N1)) for x in words])
def logP2grams(words):
    return sum([log10(WordProbability(x,N2gramDict,N2)) for x in words])

###################################################
# Local search - Hillclimb to prefeorm decryption #
###################################################
    
#If verbose is set to true you see the algorithm in action    
VERBOSE =True

def hillSearch(x,f,neighbors,steps=10000):
    """Search for x that maximizes f(x) considering all the neighbours(x)"""
    if VERBOSE:
    	print("restart")
    fx=f(x)
    neighborhood=iter(neighbors(x))
    for i in range(steps):
        x2 = next(neighborhood)
        fx2 = f(x2)
        if fx2 > fx:
            x, fx= x2,fx2
            neighborhood = iter(neighbors(x))
        if VERBOSE and i%500 ==0:
        	print("Evaluation: ",fx)
    return x

def neighboring_msgs(msg):
    """Generate nearby messages based on switching most unlikely letters"""
    def swap(a,b): return msg.translate(str.maketrans(a+b, b+a))
    for bigram in heapq.nsmallest(20,set(ngrams(msg,2)),key=lambda x: WordProbability(x,N2gramDict,N2)):
        b1,b2=bigram
        for c in alphabet:
            if b1==b2:
                if WordProbability(c+c,N2gramDict,N2) > WordProbability(bigram,N2gramDict,N2):
                    yield swap(c,b1)
            else:
                if WordProbability(c+b2,N2gramDict,N2) > WordProbability(bigram,N2gramDict,N2):
                    yield swap(c,b1)
                if WordProbability(c+c,N2gramDict,N2) > WordProbability(bigram,N2gramDict,N2):
                    yield swap(c,b2)
    while True:
        yield swap(random.choice(alphabet),random.choice(alphabet))
                    

def shuffled(seq):
    """Return a randomly shuffled copy of the input sequence. Used for random restarts"""
    seq = list(seq)
    random.shuffle(seq)
    return seq

def decode_subst(msg,steps=4000,restarts=90):
    """Decode a substitution cypher with random restart hillclimbing"""
    msg="".join(allwords(msg)).lower()
    candidates=[hillSearch(encode(msg,key="".join(shuffled(alphabet))),logP3grams,neighboring_msgs,steps) for _ in range(restarts)]
    augCandidates = []
    for candidate in candidates:        
        segmentedCAndidate = segment(candidate)
        probSegCand = Pword(segmentedCAndidate)
        augCandidates.append((segmentedCAndidate,probSegCand))
        
    best=max(augCandidates,key= lambda x: x[1])
    return " ".join(best[0])



