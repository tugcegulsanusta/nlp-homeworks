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

def change_to_unk(tokenization_list, unigram_counts):
    last_key = 'UNK'
    unigram_counts_unk =dict(sort_desc_by_value(unigram_counts))
    last_value =  next(reversed(unigram_counts_unk.values()))
    replaced = list(unigram_counts_unk.popitem())

    unigram_counts_unk[last_key]= last_value

    tokenization_list_unk = ["UNK" if word == replaced[0] else word for word in tokenization_list ]

    print(type(replaced))
    print(replaced)
    print( unigram_counts_unk , tokenization_list_unk)
    return tokenization_list_unk,unigram_counts_unk


def sort_desc_by_value( dictionary ):
    return sorted(dictionary.items(), key=lambda item: -item[1])

def token_list_to_bigram(tokenization_list):
    bigram_list = []
    for i in range (len(tokenization_list)-1):
        temp = (tokenization_list[i], tokenization_list[i+1])
        bigram_list.append(temp)

    return bigram_list


def find_unigram_prob(tokenization_list, unigram_counts):
    total_count = len(tokenization_list)
    unigram_prob = {}
    for word in unigram_counts:
        probability = unigram_counts[word]/total_count
        unigram_prob[word]=probability
    return unigram_prob

def find_bigram_prob(bigram_list, unigram_counts, bigram_counts):
    list_of_prob = {}
    for bigram in bigram_list:
        word1 = bigram[0]
        list_of_prob[bigram] = (bigram_counts[bigram])/ (unigram_counts[word1])
    return list_of_prob

def add_k_smoothing( unigram_counts, bigram_counts, bigram_list):
    smoothed_list= {}
    uniqueWordCount = len(unigram_counts)
    k = 0.5
    for bigram in bigram_list:
        word = bigram[0]
        smoothed_list[bigram] = (bigram_counts[bigram]+ k)  / (unigram_counts[word] + (k*uniqueWordCount))

    # Add 0 probabilities
    for word1 in unigram_counts:
        for word2 in unigram_counts:
            if ((word1,word2) not in bigram_counts):
                smoothed_list[(word1,word2)] = ( k)  / (unigram_counts[word1] + (k*uniqueWordCount))
    return smoothed_list

def write_file_line( fw, label, value):
    line = str(label)+" : "+str(value)+"\n"
    fw.write(line)

def write_ngram_info(fw, label, ngram_count, ngram_probability):
    fw.write("\n"+str(label)+"\n")
    for couple in sort_desc_by_value(ngram_count):
        word = couple[0]
        count = couple[1]
        probability = ngram_probability.get(word)
        fw.write(str(word)+" \t "+str(count)+" \t "+str(probability)+"\n")

def write_smoothed_info(fw, label, bigram_probability, smoothed_probability):
    limit = 100
    fw.write("\n"+str(label)+"\n")
    for couple in sort_desc_by_value(smoothed_probability):
        limit = limit - 1
        word = couple[0]
        smoothed = couple[1]
        probability = bigram_probability.get(word)
        fw.write(str(word)+" \t "+str(probability)+" \t "+str(smoothed)+"\n")
        if(limit<1):
            break

def write_file(file_name_write,  unigram_counts, unigram_probability, 
               bigram_counts, bigram_probability, sentence_count, 
               total_word_count,smoothed_list, ):
    with codecs.open(file_name_write, 'w', encoding="utf-8") as fw:
        write_file_line(fw,"Cümle sayısı",sentence_count)
        write_file_line(fw,"Toplam kelime sayısı",total_word_count)
        write_file_line(fw,"Unique kelime sayısı",len(unigram_counts))

        write_ngram_info(fw, "Unigram Bilgileri", unigram_counts, unigram_probability)
        write_ngram_info(fw, "Bigram Bilgileri", bigram_counts, bigram_probability) 

        write_smoothed_info(fw,"Add k Smoothing olasılıkları",bigram_probability, dict(smoothed_list))
    fw.close()

if __name__ == "__main__":
    file_name = "deneme.txt"
    tokenization_list = tokenize_file(file_name)
    unigram_counts = count_unique_item(tokenization_list)
    tokenization_list_unk, unigram_counts_unk = change_to_unk(tokenization_list,unigram_counts)
    unigram_probability= find_unigram_prob(tokenization_list_unk, unigram_counts_unk)
    bigram_list_unk = token_list_to_bigram(tokenization_list_unk)
    bigram_counts_unk = count_unique_item(bigram_list_unk)
    bigram_probability = find_bigram_prob(bigram_list_unk,unigram_counts_unk,bigram_counts_unk)
    sentence_count = unigram_counts["</s>"]
    total_word_count = len(tokenization_list)
    smoothed_list = add_k_smoothing(unigram_counts_unk,bigram_counts_unk, bigram_list_unk)
    #sentence1 = input("Lütfen birinci cümleyi giriniz: ")
    #sentence2 = input("Lütfen ikinci cümleyi giriniz: ")
    write_file("sonuc.txt", unigram_counts_unk, unigram_probability,
                bigram_counts_unk, bigram_probability, sentence_count,
                total_word_count, sort_desc_by_value(smoothed_list))
