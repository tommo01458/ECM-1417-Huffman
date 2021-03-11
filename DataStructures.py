import sys, string #Importing system and string libraries.
from bitstring import BitArray #Importing bitstring library.
binaryCodes = {} #Defining binary codes dictionary.

def occurrence (str) : 
    frequencyDictionary = {}
    for x in str : #Number of items in the string input.
        frequencyDictionary[x] = frequencyDictionary.get(x,0) + 1 #Adding the symbols to the nect index of the dictionary.
    return frequencyDictionary

def inputAsTuple (frequencyDictionary) : 
    letterFrequency = frequencyDictionary.keys()
    letterTuple = []
    for p in letterFrequency : #For the number of dictionary keys.
        letterTuple.append((frequencyDictionary[p],p)) #Append the index to the tuple.
    letterTuple.sort() #Sort the tuple in ascending order.
    return letterTuple

def tupleAddition(letterTuple) :
    while len(letterTuple) > 1 :
        leastFrequent = tuple(letterTuple[0:2]) #Finding the least frequent tuple by value.             
        otherTuples  = letterTuple[2:] #Every tuple that isnt the the two smallest.          
        tupleAdding= leastFrequent[0][0] + leastFrequent[1][0] #Adding the two smallest.  
        letterTuple   = otherTuples + [(tupleAdding,leastFrequent)] #Adding the least frequent back to the others.  
        letterTuple = sorted(letterTuple, key=lambda x: x[0]) #Re-sort the tuples.
    return letterTuple[0]            

def removeInts (huffmanTree) :
    x = huffmanTree[1]                            
    if type(x) == type("") : #If the type is "" return the tree.
        return x     
    else : 
        return (removeInts(x[0]), removeInts(x[1])) #Remove the ints from the tuple at x[0] and x[1] for the entire tree.

def binaryValues (nodes, nullValue='') :
    global binaryCodes #Making the binary codes global.
    if type(nodes) == type("") : #If the type is "" the code is ''.
        binaryCodes[nodes] = nullValue            
    else  :                              
        binaryValues(nodes[0], nullValue+"0") #If the tree goes left (0) add 0.
        binaryValues(nodes[1], nullValue+"1") #If the tree goes right (1) add 1.

def encoding (str) :
    global binaryCodes
    nullOutput = ""
    for x in str : #For number of items in the string.
        nullOutput += binaryCodes[x] #Add the binary codes to the variable.
    return nullOutput

def decoding (huffmanTree, str) :
    nullOutput = ""
    x = huffmanTree
    for decodingBit in str : #For number of bits in the string.
        if decodingBit == '0' : #If the but is 0.
            x = x[0] #Take a left turn.
        else: 
            x = x[1] #Take a right turn.
        if type(x) == type("") : #If the type is "" the output is the tree.
            nullOutput += x             
            x = huffmanTree               
    return nullOutput

def main () :
    encodeFile = input("Enter a file to compress in the form filename.txt.") #Input file name.
    decodeFile = input("Enter the decoded file name in the form filename.bin.") #Output file name.
    with open(encodeFile, 'r') as f: #Read in the file.
        str = f.read()
    frequencyDictionary = occurrence(str) #Applying functions to the data.
    letterTuple = inputAsTuple(frequencyDictionary)
    huffmanTree = tupleAddition(letterTuple)
    huffmanTree = removeInts(huffmanTree)
    binaryValues(huffmanTree)
    encoded = encoding(str) #Encode the data.
    a = BitArray(bin=encoded) #Encoding the data as binary.
    with open(decodeFile, 'wb') as f:
	    a.tofile(f) #Writing to the file.

    with open(decodeFile, 'rb') as f:
	    b = BitArray(f.read()) #Reading from the file.

    open(encodeFile+'_huffman_tree.txt', 'w').write('\n'.join('%s %s' % x for x in huffmanTree)) #Writing huffman tree to a file.

    binaryDifference = (len(b.bin))-(len(a.bin)) #Removing added 0's from the binary conversion.
    for d in range(binaryDifference):
        b.bin = b.bin[:-1] #Removing the 0's

    decoded = decoding (huffmanTree,b.bin) #Decoding the data using the encoded data and the huffman tree.
    if (str == decoded): #If the original text equals the decoded data.
        print("Encoding and decoding successful.")
    else:
        print("Encoding and decoding not successful.")

if __name__ == "__main__" : #Runing the main code.
    main()