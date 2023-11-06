import re
import codecs

unigram_prob = {}
bigram_counts = {}

def tokenizeFile(file_name):
    data = []
    f=codecs.open(file_name, mode="r",encoding="utf-8")
    data = f.read()
    f.close()

    myRegex_start = "(?:^|(?:[\*]\s+))"
    myRegex_end = "[.,!?]"
    add_end = re.sub(myRegex_end, " </s>*", data)
    add_start = re.sub(myRegex_start, " <s> ",add_end).lower()
    tokenization_list = add_start.split()
    tokenization_list[-1] = "</s>"
    return  tokenization_list

def countUniqueItem( list ):
    uniqueCounts = {}
    for item in list:
        if item not in uniqueCounts:
            uniqueCounts[item] = 1
        else:
            uniqueCounts[item] += 1
    return uniqueCounts

def tokenListToBigram(tokenization_list):
    bigram_list = []
    for i in range (len(tokenization_list)-1):
        temp = (tokenization_list[i], tokenization_list[i+1])
        bigram_list.append(temp)
    return bigram_list

def findUnigramProb(tokenization_list, unigram_counts):
    total_count = len(tokenization_list)
    unigram_strings = []
    for word in unigram_counts:
        unigram_probabilities = {word,unigram_counts[word]/total_count}
        unigram_strings.append(unigram_probabilities)
    return unigram_strings

def findBigramProb(bigram_list, unigram_counts, bigram_counts):
    listOfProb = {}
    for bigram in bigram_list:
        word1 = bigram[0]
        word2 = bigram[1]
        listOfProb[bigram] = (bigram_counts[bigram])/ (unigram_counts[word1])

    return listOfProb

def write_file(file_name_write,  unigram_counts, unigram_probability, bigram_counts, bigram_probability, sentenceCount, totalWordCount):
    
    with codecs.open(file_name_write, 'w', encoding="utf-8") as fw:

        fw.write("Cümle sayısı : ")
        fw.write(str(sentenceCount))
        fw.write("\nToplam kelime sayısı : ")
        fw.write(str(totalWordCount))
        fw.write("\nUnique kelime sayısı : ")
        fw.write(str(len(unigram_counts)))
        fw.write("\nUnigram sayıları: \n")
        fw.write(str(unigram_counts))
        fw.write("\nUnigram olasılıkları: \n")
        fw.write(str(unigram_probability))
        fw.write("\nBigram sayıları: \n")
        fw.write(str(bigram_counts))
        fw.write("\nBigram olasılıkları : \n")
        fw.write(str(bigram_probability))

    #bigram_data = str(bigram_calculations(file_name_open))
    fw.close()

if __name__ == "__main__":
    fileName = "deneme.txt"
    tokenizationList = tokenizeFile(fileName)
    unigramCounts = countUniqueItem(tokenizationList)
    unigram_probability= findUnigramProb(tokenizationList, unigramCounts)
    bigram_list = tokenListToBigram(tokenizationList)
    bigram_counts = countUniqueItem(bigram_list)
    bigram_probability = findBigramProb(bigram_list,unigramCounts,bigram_counts)
    sentenceCount = unigramCounts["</s>"]
    totalWordCount = len(tokenizationList)

    
    write_file("sonuc.txt",unigramCounts, unigram_probability, bigram_counts, bigram_probability, sentenceCount, totalWordCount)
