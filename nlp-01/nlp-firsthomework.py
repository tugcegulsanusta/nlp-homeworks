import re
import sys




f= open("hw01_bilgisayar.txt", encoding="utf-8", mode="r")
data =  f.read()
count = 0
for tokens in data:
    if tokens.endswith(".") or tokens.endswith("!") or tokens.endswith("?"):
        count += 1
print(f"number of sentences: {count}")

myRegex_start = "(?:^|(?:[\*]\s+))"
myRegex_end = "[.,!?]"
clean_data = re.sub(myRegex_end, " </s>*", data)
clean_data_new = re.sub(myRegex_start, " <s> ",clean_data).lower()
tokenization_list = clean_data_new.split()
tokenization_list[-1] = "</s>"
print(tokenization_list)

total_count=0
counts = {}
for word in tokenization_list:
    total_count+=1
    if word not in counts:
        counts[word] = 1
    else:
        counts[word] += 1

def wordCounts(counts):
     for word in counts:
        print( word,counts[word])

def unigramProb(counts,total_count):
    for word in counts:
        print(word, counts[word]/total_count)

print("kelime sayıları: ")
wordCounts(counts)

print("unigram olasılıkları: ")
unigramProb(counts, total_count)