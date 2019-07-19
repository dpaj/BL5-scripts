import re
import numpy as np
import itertools
from collections import Counter


def words(text): return re.findall(r'\w+', text.lower())

#WORDS = Counter(words(open('Words_PVs.txt').read()))
#DMP, I am adding this absolute path to make importing easier for 2019-B
path_to_Sala_python_libraries = '/home/bl-user/Script_Test/'
WORDS = Counter(words(open(path_to_Sala_python_libraries+'Words_PVs.txt').read()))

def P(word, N=sum(WORDS.values())): 
    "Probability of `word`."
    return WORDS[word] / N

def correction(word): 
    "Most probable spelling correction for word."
    return max(candidates(word), key=P)

def candidates(word): 
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words): 
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    numbers    = '1234567890_'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    nreplaces  = [L + c + R[1:]           for L, R in splits if R for c in numbers]
    ninserts   = [L + c + R               for L, R in splits for c in numbers]
    return set(deletes + transposes + replaces + inserts + nreplaces + ninserts)

def edits2(word): 
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))
    
    
###############################    

def SpellChk(word):
    klist=[]
    kwords=[]
    if word not in WORDS:
       #klist.append([correction(word.lower())])
       klist.append(list(candidates(word.lower())))
       kwords.append([item for sublist in klist for item in sublist])
       print("Suggestion:")
       #print("Most Probable = {0}  or...".format(kwords[0][0]))
       for ii in kwords[0]:
          if ii in WORDS:
             print(ii)
          else:
             print("Not Found !!! Check the PV Spelling or contact Instrument Scientist.")
       
       

