import re

unigram_counts = {}
unigram_prob = {}
bigram_counts = {}
tokenization_list = []

def read_data(file_name):
    data = []
    f=open(file_name, mode="r")
    data = f.read()
    count = 0
    for tokens in data:
        if tokens.endswith(".") or tokens.endswith("!") or tokens.endswith("?"):
            count += 1
    #print(f"number of sentences: {count}")
    myRegex_start = "(?:^|(?:[\*]\s+))"
    myRegex_end = "[.,!?]"
    add_end = re.sub(myRegex_end, " </s>*", data)
    add_start = re.sub(myRegex_start, " <s> ",add_end).lower()
    tokenization_list = add_start.split()
    tokenization_list[-1] = "</s>"
    return  tokenization_list

def unigram_calculation(file_name):
    tokenization_list = tokenization(file_name)
    total_count = 0
    for word in tokenization_list:
        total_count+=1
        if word not in unigram_counts:
            unigram_counts[word] = 1
        else:
            unigram_counts[word] += 1

    print("Unigram kelime sayıları: ")
    print("unigram listesi: " , unigram_counts)
    
    #for word in unigram_counts:
     #   print(word,unigram_counts[word])
    print("Unigram olasılıkları: ")
    for word in unigram_counts:
        unigram_prob = {word,unigram_counts[word]/total_count}
    return unigram_prob

def bigram_calculations(file_name):
    tokenization_list = read_data(file_name)
    
    for i in range(len(tokenization_list)-1):
        temp = (tokenization_list[i], tokenization_list[i+1])
        if not temp in bigram_counts:
            bigram_counts[temp] = 1
        else:
            bigram_counts[temp] += 1
    print("Bigram listesi: ", bigram_counts  )

    return bigram_counts

#bigram_calculations("deneme.txt", bigram_counts)
#unigram_calculation("hw01_tinytr.txt")
#unigram_calculation("hw01_bilgisayar.txt")



if __name__ == "__main__":
    file_name = "hw01_tinytr.txt"
    tokenization_list = read_data(file_name)
    bigram_calculations(file_name)
