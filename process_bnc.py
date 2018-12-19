from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

sentences = []

corpus = '/home/lizaku/Документы/Big_Data/bnc_reference.txt'
with open(corpus) as f_in:
    for line in f_in:
        sentence = ' '.join([word.split('_')[0] for word in line.strip().split()])
        sentences.append(sentence)

count_model = CountVectorizer(ngram_range=(2,2)) # default bigram model
X = count_model.fit_transform(sentences)
# X[X > 0] = 1 # run this line if you don't want extra within-text cooccurence (see below)
Xc = (X.T * X) # this is co-occurrence matrix in sparse csr format
#Xc.setdiag(0) # sometimes you want to fill same word cooccurence to 0
#print(Xc.todense()) # print out matrix in dense format
#print(count_model.vocabulary_)
#sum_occ = np.sum(X.todense(),axis=0)
#print('Sum of word-word occurrences:', sum_occ)
#obj = zip(count_model.get_feature_names(),np.array(sum_occ)[0].tolist())
#for o in obj:
#    print(o[0], o[1])
vocab = set()
with open('bnc.sm', 'w', encoding='utf-8') as matrix:
    for pair in count_model.vocabulary_:
        w1, w2 = pair.split()
        count = count_model.vocabulary_[pair]
        vocab.add(w1)
        vocab.add(w2)
        matrix.write(w1 + ' ' + w2 + ' ' + str(count) + '\n')

with open('bnc.cols', 'w', encoding='utf-8') as dims:
    for w in vocab:
        dims.write(w + '\n')

