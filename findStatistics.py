import codecs
import urllib.request
import re

def wordListToFreqDict(wordList):
    wordFreq = [wordList.count(p) for p in wordList]
    return dict(list(zip(wordList,wordFreq)))

def findOccurrences(content):
    occIndex = content.find("Occurrence")
    if occIndex > -1:
        quoteIndex = content.rfind(">",occIndex - 10, occIndex)
        if quoteIndex > -1:
            return int(content[quoteIndex + 1:occIndex].strip())
    return  -1

def findDefinition(content):
    occIndex = content.find("toptitle2")
    if occIndex > -1:
        quoteStartIndex = content.find(">",occIndex, occIndex + 50)
        quoteEndIndex = content.find("<",occIndex, occIndex + 50)
        if quoteStartIndex > -1 and quoteEndIndex > -1:
            result = content[quoteStartIndex + 1:quoteEndIndex].split(":")
            
            return {'translation': result[0].strip(), 'definition': result[1].strip()}
    return  {'translation': "", 'definition': ""}
    
bibleType = "hebrew" #hebrew or greek
codedWords = {}
print("Starting ...................")
with open('./wordsCode.txt', encoding='utf-8') as file:
    wordList = [l.rstrip("\n") for l in file]
    wordFreq = wordListToFreqDict(wordList)

    sortedWordFreq = {k: v for k, v in sorted(wordFreq.items(), reverse=True, key=lambda item: item[1])}
   
    #sortedWordFreq = wordFreq
    data = {}
    for key, value in sortedWordFreq.items():
        data[key] = {'translation':"", 'definition':"", 'occurrences':0, 'frequency':value}
        #print(str(key) +  " => " + str(value))

    for key in sortedWordFreq.keys():
        urlName = "https://saintebible.com/" + bibleType + "/" + str(key) + ".htm"
        data[key]['link'] = urlName
        print (urlName)
        x = urllib.request.urlopen(urlName)
        stream = x.read().decode("utf-8")
        #o = re.search(r'>(.*?)Occurrences<', stream).group(1)
        data[key]['occurrences'] = findOccurrences(stream)
        defini = findDefinition(stream)
        data[key]['translation'] = defini['translation']
        data[key]['definition'] = defini['definition']
        
                
    print("Code\tLink\t\t\t\t\tOccurrences\tFrequency\tTranslation\tDefinition")
    for key, value in data.items():
        print(str(key) +  "\t" + str(value['link']) + "\t" + str(value['occurrences']) +  "\t\t" + str(value['frequency']) +  "\t\t" + value['translation'] +  "\t\t" + value['definition'])
        #print(str(key) +  "\t" + value['definition'])
