import re
import codecs


unigram_prob = {}
bigram_counts = {}
bigram_prob = {}

def read_data(file_name):
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

def total_counter(tokenization_list):
    total_count = 0
    for word in tokenization_list:
        total_count+=1
    return total_count

def unigram_counter(tokenization_list):
    unigram_counts = {}
    for word in tokenization_list:
        if word not in unigram_counts:
            unigram_counts[word] = 1
        else:
            unigram_counts[word] += 1
    return unigram_counts

def unigram_prob_counter(tokenization_list, unigram_counts):
    total_count = total_counter(tokenization_list)
    unigram_strings = []
    for word in unigram_counts:
        unigram_probabilities = {word,unigram_counts[word]/total_count}
        unigram_strings.append(unigram_probabilities)
    return unigram_strings


def bigram_counter(tokenization_list):
    for i in range(len(tokenization_list)-1):
        temp = (tokenization_list[i], tokenization_list[i+1])
        if not temp in bigram_counts:
            bigram_counts[temp] = 1
        else:
            bigram_counts[temp] += 1
    print("Bigram listesi: ", bigram_counts  )

    return bigram_counts

def write_file(file_name_write, tokenization_list,  unigram_counts):
    #fw = codecs.open(file_name_write,mode="w",encoding="utf-8")
    unique_word_counts_str = str(len(unigram_counts))
    unigram_counts_str =str(unigram_counts)
    unigram_probability_str = str(unigram_prob_counter(tokenization_list, unigram_counts))
    with codecs.open(file_name_write, 'w', encoding="utf-8") as fw:
        fw.write("Unique kelime sayısı : ")
        fw.write(unique_word_counts_str)
        fw.write("\nUnigram sayıları: \n")
        fw.write(unigram_counts_str)
        fw.write("\nUnigram olasılıkları: \n")
        fw.write(unigram_probability_str)

    #bigram_data = str(bigram_calculations(file_name_open))
    fw.close()

if __name__ == "__main__":
    file_name = "deneme.txt"
    tokenization_list = read_data(file_name)
    unigram_counts = unigram_counter(tokenization_list)
    #bigram_calculations(file_name)
    #unigram_calculation(file_name)
    write_file("sonuc.txt", tokenization_list,  unigram_counts)
