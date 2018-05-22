# -*- coding: utf-8 -*-
import numpy as np

def shiftch(ch,ikey):
    if ch.isupper():
        newch=chr(((ord(ch)+ikey-65)%26)+65)
    elif ch.islower():
        newch=chr(((ord(ch)+ikey-97)%26)+97)
    else:
        newch=ch
    
    return newch

def shiftlines(lines,ikey):
    newlines=[]
    for line in lines:
        newline=""
        for ch in line:
            newline=newline+shiftch(ch,ikey)
        newlines.append(newline)
    return newlines
    
def getfreq(lines):
    totals=26*[0]
    for line in lines:
        lowerLine=line.lower()
        for letter in range(97,123):
            totals[letter-97]+=lowerLine.count(chr(letter))
        
    freqlst=[]
    grandtotal=sum(totals)
    
    for total in totals:
        freq=total/grandtotal*100
        freqlst.append(freq)
    return freqlst    

def listdif(a,b):
    total=0.
    
    for i in range(len(a)):
        total+= abs(a[i]-b[i])
        
    return total

def idxmin(lst):
    idx=np.argmin(lst)
    return idx

#import frequency data
freqfile=open("ch-freq-en.txt")
freqs=[]
for line in freqfile.readlines():
    line=line.split('\n')
    freqs.append(line[0].split('\t'))
    
freqfile.close()

#make master frequency list
masterfreqlist=np.zeros(26)
for item in freqs:
    masterfreqlist[ord(item[0])-65]=item[1]

#Loop for each secret file
for n in range(7):
    secretfilename=('secret-files\\secret'+str(n)+'.txt')
    decodedfilename=('decoded\\decoded'+str(n)+'.txt')
    
    #import secret text
    secretfile=open(secretfilename)
    secret=secretfile.readlines()
    secretfile.close()
    
    #make frequency list of secret text
    freqlst=getfreq(secret)
    
    #Calculate score for each possible key and determine best key
    scores=np.zeros(26)    
    for key in range(26):
        shiftedlst=np.roll(freqlst,key)
        scores[key]=listdif(masterfreqlist,shiftedlst)
    
    correctkey=idxmin(scores)
    
    #Shift secret text with found key
    decoded=shiftlines(secret,correctkey)    
    
    #Save decoded text to file
    f=open(decodedfilename,"w")
    f.writelines(decoded)
    f.close()
    
    print('decoded ',secretfilename,' with a key of ',correctkey)
    
print("Done")