import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from jiwer import wer, mer, wil, wip,cer
import collections
import glob
import os
result_1= pd.read_csv('BPE_Outputs/out_1.csv', encoding='utf-8')
result_2= pd.read_csv('BPE_Outputs/out_2.csv', encoding='utf-8')
result_3= pd.read_csv('BPE_Outputs/out_3.csv', encoding='utf-8')
result_4 = pd.read_csv('BPE_Outputs/out_4.csv', encoding='utf-8')

pred=[]
true=[]
for w, wt in zip(result_1.iloc[:,0].values, result_1.iloc[:,1].values):
    w=w.replace('</e','')
    wt= wt.replace('</e','')
    pred.append(w)
    true.append(wt)
for w, wt in zip(result_2.iloc[:,0].values, result_2.iloc[:,1].values):
    w=w.replace('</e','')
    wt= wt.replace('</e','')
    pred.append(w)
    true.append(wt)
for w, wt in zip(result_3.iloc[:,0].values, result_3.iloc[:,1].values):
    w=w.replace('</e','')
    wt= wt.replace('</e','')
    pred.append(w)
    true.append(wt)
for w, wt in zip(result_4.iloc[:,0].values, result_4.iloc[:,1].values):
    w=w.replace('</e','')
    wt= wt.replace('</e','')
    pred.append(w)
    true.append(wt)

def calculate_wer(ref, hypo):
    ref_words = ref.split(' ')
    #print(ref_words)
    hyp_words = hypo.split(' ')
    #print(hyp_words)
    #print('True:{}   Generated:{}'.format(ref_words, hyp_words))
    # Counting the number of substitutions, deletions, and insertions
    substitutions = sum(1 for refs, hyp in zip(ref_words, hyp_words) if refs != hyp)
    #print(substitutions)
    deletions = len(ref_words) - len(hyp_words)
    #print(deletions)
    insertions = len(hyp_words) - len(ref_words)
    #print(insertions)
    # Total number of words in the reference text
    total_words = len(ref_words)
    #print(total_words)
    # Calculating the Word Error Rate (WER)
    wer = (substitutions + deletions + insertions) / total_words
    acc= 1-wer
    #print('Substitution:{}   Deletion:{}   Insertions:{}   AER:{}   Accuracy:{}'.format(substitutions, deletions, insertions,wer,acc))
    return wer, acc, substitutions, deletions, insertions

for i in range(len(true)):
    w, ac= calculate_wer(true[i], pred[i])
