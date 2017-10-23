import string
import random

WORDLIST_FILENAME = "words.txt"

def loadWords():
    print "Loading word list from file..."
    inFile = open(WORDLIST_FILENAME, 'r')
    wordList = inFile.read().split()
    print "  ", len(wordList), "words loaded."
    return wordList

def isWord(wordList, word):
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\\:;'<>?,./\"")
    return word in wordList

def randomWord(wordList):
    return random.choice(wordList)

def randomString(wordList, n):
    """
    Returns a string containing n random words from wordList

    wordList: list of words
    returns: a string of random words separated by spaces.
    """
    return " ".join([randomWord(wordList) for _ in range(n)])

def randomScrambled(wordList, n):
    """
    Generates a test string by generating an n-word random string
    and encrypting it with a sequence of random shifts.

    wordList: list of words
    n: number of random words to generate and scamble
    returns: a scrambled string of n random words

    NOTE:
    This function will ONLY work once you have completed your
    implementation of applyShifts!
    """
    s = randomString(wordList, n) + " "
    shifts = [(i, random.randint(0, 25)) for i in range(len(s)) if s[i-1] == ' ']
    return applyShifts(s, shifts)[:-1]

def getStoryString():
    """
    Returns a story in encrypted text.
    """
    return open("story.txt", "r").read()



#Encryption
def buildCoder(shift):
    """
    Returns a dict that can apply a Caesar cipher to a letter.
    The cipher is defined by the shift value. Ignores non-letter characters
    like punctuation, numbers and spaces.

    shift: 0 <= int < 26
    returns: dict
    """
    c1=[]
    c2=[]
    for c in string.ascii_lowercase:
        c1.append(c)
    for c in string.ascii_uppercase:
        c2.append(c)

    dict={}
    index=0
    for char in c1:
        dict.keys().append(char)
        dict[char]=c1[index+shift]
        if index+shift==25:
            index=-shift
        else:
            index+=1         
    index=0
    for char in c2:
        dict.keys().append(char)
        dict[char]=c2[index+shift]
        if index+shift==25:
            index=-shift
        else:
            index+=1         
    return dict

    

def applyCoder(text, coder):
    """
    Applies the coder to the text. Returns the encoded text.

    text: string
    coder: dict with mappings of characters to shifted characters
    returns: text after mapping coder chars to original text
    """
    result=''
    for char in text:
        try:
            result=result+coder[char]
        except KeyError:
            result=result+char
            continue

    return result

def applyShift(text, shift):
    """
    Given a text, returns a new text Caesar shifted by the given shift
    offset. Lower case letters should remain lower case, upper case
    letters should remain upper case, and all other punctuation should
    stay as it is.

    text: string to apply the shift to
    shift: amount to shift the text (0 <= int < 26)
    returns: text after being shifted by specified amount.
    """
    return applyCoder(text, buildCoder(shift))

#Decryption

def findBestShift(wordList, text):
    """
    Finds a shift key that can decrypt the encoded text.

    text: string
    returns: 0 <= int < 26
    """
    shift=1
    words=text.split(" ")
    bestnum=0
    bestshift=0
    while shift<26:
        num=0
        for word in words:      
            word=applyCoder(word, buildCoder(shift))
            if isWord(wordList, word):
                num=num+1
            else:
                continue
        if num>bestnum:
            bestshift=shift
            bestnum=num
        shift=shift+1
    


    return bestshift




def decryptStory():
    """
    Using the methods you created in this problem set,
    decrypt the story given by the function getStoryString().
    Use the functions getStoryString and loadWords to get the
    raw data you need.

    returns: string - story in plain text
    """
    return applyShift(getStoryString(), findBestShift(loadWords(), getStoryString()))


# Build data structures used for entire session and run encryption

if __name__ == '__main__':
    wordList = loadWords()
    s = applyShift('Hello, world!', 8)
    bestShift = findBestShift(wordList, s)
    assert applyShift(s, bestShift) == 'Hello, world!'
    print decryptStory()