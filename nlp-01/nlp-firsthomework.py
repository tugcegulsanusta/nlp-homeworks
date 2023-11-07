import re
import codecs
from collections import defaultdict

unigram_prob = {}
bigram_counts = {}

def tokenize_file(file_name):
    data = []
    f=codecs.open(file_name, mode="r",encoding="utf-8")
    data = f.read()
    f.close()

    myRegex_start = "(?:^|(?:[\*]\s+))"
    myRegex_end = "[.,!?]"
    add_end = re.sub(myRegex_end, " </s>*", data)
    add_start = re.sub(myRegex_start, " <s> ",add_end).lower()
    tokenizationList = add_start.split()
    tokenizationList[-1] = "</s>"
    return  tokenizationList

def count_unique_item( list ):
    unique_counts = {}
    for item in list:
        if item not in unique_counts:
            unique_counts[item] = 1
        else:
            unique_counts[item] += 1
    return unique_counts

def sortItem(unigram_count, unigram_prob, bigram_count, bigram_prob, smoothedList):
    sorted_unigram_count = dict(sorted(unigram_count.items(), key=lambda item: -item[1]))
    sorted_unigram_prob = unigram_prob
    sorted_bigram_count = dict(sorted(bigram_count.items(), key=lambda item: -item[1]))
    sorted_bigram_prob = dict(sorted(bigram_prob.items(), key=lambda item: -item[1]))
    sorted_smoothed_list= dict(sorted(smoothedList.items(),key=lambda item: -item[1]))
    return sorted_unigram_count, sorted_unigram_prob, sorted_bigram_count, sorted_bigram_prob ,sorted_smoothed_list

def token_list_to_bigram(tokenization_list):
    bigram_list = []
    for i in range (len(tokenization_list)-1):
        temp = (tokenization_list[i], tokenization_list[i+1])
        bigram_list.append(temp)
    return bigram_list

def find_unigram_prob(tokenization_list, unigram_counts):
    total_count = len(tokenization_list)
    unigram_strings = []
    for word in unigram_counts:
        unigram_probability = {word,unigram_counts[word]/total_count}
        unigram_strings.append(unigram_probability)
    return unigram_strings

def find_bigram_prob(bigram_list, unigram_counts, bigram_counts):
    list_of_prob = {}
    for bigram in bigram_list:
        word1 = bigram[0]
        list_of_prob[bigram] = (bigram_counts[bigram])/ (unigram_counts[word1])

    return list_of_prob

def add_k_smoothing( unigram_counts, bigram_counts, bigram_list):
    smoothed_list= {}
    uniqueWordCount = len(unigram_counts)
    k = 1.5
    
    for bigram in bigram_list:
        word1 = bigram[0]
        smoothed_list[bigram] = (bigram_counts[bigram]+ k)  / (unigram_counts[word1] + (k*uniqueWordCount))
    return smoothed_list
  

def write_file(file_name_write,  unigram_counts, unigram_probability, bigram_counts, bigram_probability, sentence_count, total_word_count,smoothed_list):
    
    with codecs.open(file_name_write, 'w', encoding="utf-8") as fw:

        fw.write("Cümle sayısı : ")
        fw.write(str(sentence_count))
        fw.write("\nToplam kelime sayısı : ")
        fw.write(str(total_word_count))
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
        fw.write("\nAdd k Smoothing olasılıkları: \n")
        fw.write(str(smoothed_list))

    #bigram_data = str(bigram_calculations(file_name_open))
    fw.close()

if __name__ == "__main__":
    file_name = "deneme.txt"
    tokenization_list = tokenize_file(file_name)
    unigram_counts = count_unique_item(tokenization_list)
    unigram_probability= find_unigram_prob(tokenization_list, unigram_counts)
    bigram_list = token_list_to_bigram(tokenization_list)
    bigram_counts = count_unique_item(bigram_list)
    bigram_probability = find_bigram_prob(bigram_list,unigram_counts,bigram_counts)
    sentence_count = unigram_counts["</s>"]
    total_word_count = len(tokenization_list)
    smoothed_list = add_k_smoothing(unigram_counts,bigram_counts, bigram_list)
    sorted_unigram_count, sorted_unigram_prob, sorted_bigram_count, sorted_bigram_prob, sorted_smoothed_list = sortItem(unigram_counts,bigram_list,bigram_counts,bigram_probability, smoothed_list)
    
    write_file("sonuc.txt",sorted_unigram_count, unigram_probability, sorted_bigram_count, sorted_bigram_prob, sentence_count, total_word_count, sorted_smoothed_list)
