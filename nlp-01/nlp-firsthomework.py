import re
import sys

bigram_counts = {}

def tokenization(file_name):
    f=open(file_name, mode="r")
    data = f.read()
    count = 0
    for tokens in data:
        if tokens.endswith(".") or tokens.endswith("!") or tokens.endswith("?"):
            count += 1
    print(f"number of sentences: {count}")
    myRegex_start = "(?:^|(?:[\*]\s+))"
    myRegex_end = "[.,!?]"
    add_end = re.sub(myRegex_end, " </s>*", data)
    add_start = re.sub(myRegex_start, " <s> ",add_end).lower()
    tokenization_list = add_start.split()
    tokenization_list[-1] = "</s>"
    return  tokenization_list

def bigram_calculation(file_name):
    tokenization_list = tokenization(file_name)
    total_count = 0
    for word in tokenization_list:
        total_count+=1
        if word not in bigram_counts:
            bigram_counts[word] = 1
        else:
            bigram_counts[word] += 1

    print("Kelime sayıları: ")
    for word in bigram_counts:
        print(word,bigram_counts[word])
    print("Bigram olasılıkları: ")
    for word in bigram_counts:
        print(word,bigram_counts[word]/total_count)



bigram_calculation("hw01_tinytr.txt")