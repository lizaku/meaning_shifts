from composes.utils import io_utils
from composes.similarity.cos import CosSimilarity
import sys
import codecs

obj_freq_file = 'visual_genome/objects_freq.txt'
obj_freq = set()

freq = codecs.open(obj_freq_file, 'r', 'utf-8')
for line in freq:
    word, f = line.lower().strip().split('\t')
    if int(f) >= 10:
        word = word.replace(' ', '_')
        obj_freq.add(word)

#model = sys.argv[1]
#word = sys.argv[2]
        
def jaccard_similarity(list1, list2):
    s1 = set(list1)
    s2 = set(list2)
    return len(s1.intersection(s2)) / float(len(s1.union(s2)))

def single_model(word, model):

    PATH = 'dissect_spaces/mine/'
    #load two spaces
    my_space = io_utils.load(PATH + model)
    print(word)
    #composes_space = io_utils.load('EN-wform.w.2.ppmi.svd.500.txt')

    #print my_space.id2row
    #print my_space.cooccurrence_matrix
    #print composes_space.id2row
    #print composes_space.cooccurrence_matrix

    #get the top two neighbours of "car" in aripheral space 
    print my_space.get_neighbours(word, 10, CosSimilarity()) 
                              #space2 = composes_space)
                              
def two_models(obj_freq):
    PATH = 'dissect_spaces/mine/'
    #load two spaces
    my_space = io_utils.load(PATH + 'result_attributes_f10.pkl')
    reference_space = io_utils.load(PATH + 'bnc_sample.pkl')
    
    overlap = codecs.open('bnc_overlap_5.csv', 'w', 'utf-8')
    overlap.write('Word\tJaccard\tGenome neighbors\tBNC neighbors\n')
    res_dic = {}
    for obj in list(obj_freq):
        # print(obj)
        try:
            my_n = [x[0] for x in my_space.get_neighbours(obj, 5, CosSimilarity())]
            r_n = [x[0] for x in reference_space.get_neighbours(obj, 5, CosSimilarity())]
            j = jaccard_similarity(my_n, r_n)
            res_dic[obj] = [j, my_n, r_n]
        except KeyError:
            continue
    for key, value in sorted(res_dic.iteritems(), key=lambda (k,v): (v[0],k)):
        try:
            overlap.write('\t'.join([key.decode('utf-8'), str(value[0]).decode('utf-8'), ' '.join(value[1]), ' '.join(value[2])]) + '\n')
        except:
            continue
    overlap.close()
                              
two_models(obj_freq)
#single_model(word, model)
