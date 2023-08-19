import pandas as pd
import csv
import glob
import re
import collections

def get_data():
    file= open('MWE_BPE_Data.txt', 'r+', encoding='UTF-8')
    corpus=[]
    man_line= file.readlines()
    for text in man_line:
        for word in text.split():
            
            word= word.replace('-', '')
            num_pat=r'[0-9]'
            #word.translate({ord(i): None for i in r'[0-9]'})
            match= re.search(num_pat, word)
            match_0= re.search("[A-Za-z]", word)
            match_1= re.search('[\|\’ÿêòóÃ«û¬ÆîçéüìÜûø¼Ë‘ÑÛ´æÐöïô¬?õ`!@#$%&*();,.:/=>\[\]<+\'%]', word)
            
            if match_0:
                #print('H')
                #corpus.append(word)
                continue
            if match_1:
                    #print('I')
                continue
            if match:
                word= re.sub(num_pat, '', word)
                continue
            else:
                corpus.append(word)
    return corpus


corpus= get_data()
corpus= list(filter(None, corpus))  


chars= list(set([w_i for w in corpus for w_i in w]))
vocab = list(set(" ".join(corpus)))
vocab.remove(' ')



corpus=[" ".join(token) for token in corpus]
corpus=['</s> '+token+' </e>' for token in corpus]




import collections
corpus= collections.Counter(corpus)


def get_stats(corpus):
    pairs = collections.defaultdict(int)
    for word, freq in corpus.items():
        #print(word)
        #print(freq)
        symbols = word.split()
        #i=len(symbols)-1
        #while i>=0:
        i=len(symbols)-1
        #print(i)
        while(i>0):
        #for i in range(len(symbols)-1):
            #match= re.compile('[া ি ী ু ূ ে ৈ ো ৌ ৎ ৗ ঁ ং ঃ ় ্]]')
            match= re.match('[া ি ী ু ূ ে ৈ ো ৌ ৎ ৗ ঁ ং ঃ ় ্]' , symbols[i-1])
           # print('matched')
            #print(match)
            #p.group()
            #pp=p.start()
            if match:
                i=i-1
                continue
            else:
                pairs[symbols[i-1],symbols[i]] += freq
            #print(symbols[i-1]+""+symbols[i])
            #print(freq)
                i=i-1
            #print('--'+str(i))
    return pairs

import re
morphemes=[]
def merge_vocab(pair, corpus_in):
    corpus_out = {}
    bigram = re.escape(' '.join(pair))
    #morphemes.append(bigram)
    #if bigram==' '
    p = re.compile(r'(?<!\S)' + bigram + r'(?!\S)')
    #print(p)
    for word in corpus_in:
        w_out = p.sub(''.join(pair), word)
       
        
        corpus_out[w_out] = corpus_in[word]
    morphemes.append(''.join(pair))
    return corpus_out

def merge_vocab_final(pair, corpus_in):
    #print('in merge func '+str(pair)+' recieved')
    corpus_out = {}
    bigram = re.escape(' '.join(pair))
    #print('bigram in merge func '+bigram)
    #if bigram==' '
    p = re.compile(r'(?<!\S)' + bigram + r'(?!\S)')
    #print('pattern in merge func '+str(p))
    for word in corpus_in:
        w_out = p.sub(''.join(pair), word)
        #print('joined in merge funct '+w_out)
        
        corpus_out[w_out] = corpus_in[word]
    #morphemes.append(''.join(pair))
    return corpus_out
# =============================================================================
# 
# def delete(best):
#     pairs.pop(best)
# =============================================================================


merges = []
num_merges = 5000
for i in range(num_merges):
    
    #compute frequency of bigrams in a corpus
    pairs = get_stats(corpus)
    
    #compute the best pair
    best = max(pairs, key=pairs.get)
    print(best)
    
    
    #merge the frequent pair in corpus
    corpus = merge_vocab(best, corpus)
    
    #append to merge list and vocabulary
    merges.append(best)
    vocab.append(best)


#testing with dataset
file= open('named_entity.txt','r', encoding='utf-8')
write_file=open('extracted_info.txt', 'w+', encoding='UTF-8')
for lines in file.readline().split(' '):
    j=0
    write_file.write(str(lines)+'\n')
    #word='ইবোপিশক্না'
    word=lines
    word=" ".join(word)
    #word= word+' </w>'
    word= '</s> '+word+' </e'
    word= {word:1}
    i=0
    #j=0
    print(word)
    #input()
    while(True):
        #input()
        #compute frequency
        pairs = get_stats(word)
        print(pairs)
        #extract keys
        pairs = pairs.keys()
        #print(pairs)
        #find the pairs available in the learned operations
        ind=[merges.index(i) for i in pairs if i in merges]
        print(ind)
            #sorted_ind= sorted(ind)
            #for i in sorted_ind:
              #   best= merges[i]
              #  word= merge_vocab(best, word)
                # print("Iteration ",i+1, list(word.keys())[0])
                
        if(len(ind)==0):
            print("\nBPE Completed...")
            break
        
        #choose the most frequent learned operation
        best = merges[min(ind)]
        print(best)
        
        #merge the best pair
        word = merge_vocab_final(best, word)
        
        print("Iteration ",i+1, list(word.keys())[0])
        extract=list(word.keys())[0]
        write_file.write(extract)
        write_file.write('\n')
        #file.write("Iteration ")
        #file.write(str(i+1)+" ")
        #file.write(str(list(word.keys())[0])+"\n")
        i=i+1
    
    #corpus1.iloc[j,1]=list(word.keys())[0]
    #j+=1
    #file.write("--------------\n")
file.close()
write_file.close()
