# -*- coding: utf-8 -*-
import cypherClass
import pickle
import utills.plotters as plotters


import VowelDistribution.vowelDist as vowelDist
############################
# DEFINE YOUR PROBLEM HERE #
############################

CYPHER ="""1!2č47?8=2.794č4t.7928?=
145321?č4t4=5t2=262m4
72ktč?=?!85č759395čn59č4!
<5=?72!85č=5t472=565-2
53272ktč4k=295k1532č3č49
84=948m?812808?-!9301465
694=23=5+0!7460-č41295č
!85č759395čn49č4!5321?č4
=262m451532č
"""

CYPHER1 = """
abcdefey
gcghijkabclmcnexhgoncxpc
tmencprjffeseneijkabclkbj
kemepghretbphdcajrem
fetfekhteajremamcietfccmetc
fjhphdcncbghthfgeijtmrm
mabodhfaggmcbcldotep
"""

alphabet = "abcčdefghijklmnoprsštuvzž"
with open("RazdaljeMedSamoglasnikuDUMP.txt","rb") as vowelsData:
    referenceVowelDistribution = pickle.load(vowelsData)
  

print("This tool provides you with visual aid for manual decription of substitution cyphers")

newCypher = cypherClass.Cypher(CYPHER1)
newCypher.setAlphabet(alphabet)
# print(newCypher.Ntups)
# print(newCypher.DetermineVowelsByGapDistribution(referenceVowelDistribution))
#

for i in range(1, len(newCypher.Ntups)):
    ntup = newCypher.Ntups[i]
    x = [z[0] for z in ntup]
    y = [z[1] for z in ntup]
    # print(x)
    # print(y)
    name = "IF_freq_"+str(i)+"_tup"
    plotters.bar_freq_plot(x, y, name)

print(len(newCypher.Ntups))
