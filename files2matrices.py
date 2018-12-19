import re


PATH_IN = 'visual_genome/'
PATH_OUT = 'dissect_spaces/'
#PATH_OUT = ''

obj_freq_file = PATH_IN + 'objects_freq.txt'
obj_freq = set()

with open(obj_freq_file, 'r', encoding='utf-8') as freq:
    for line in freq:
        word, f = line.lower().strip().split('\t')
        if int(f) >= 10:
            word = word.replace(' ', '_')
            obj_freq.add(word)
print(len(obj_freq), 'objects filtered by frequency')

def create_row():
    objects = set()
    with open(PATH_IN + 'objects_freq.txt', 'r', encoding='utf-8') as f_in:
        for line in f_in:
            objects.add(line.lower().strip().split('\t')[0])
    with open(PATH_OUT + 'images.rows', 'w', encoding='utf-8') as f_out:
        for obj in objects:
            f_out.write(obj + '\n')
    

def create_space_relations(obj_freq):
    freq_file = PATH_IN + 'relations2_freq.txt'
    freq_dict = set()
    with open(freq_file, 'r', encoding='utf-8') as freq:
        for line in freq:
            try:
                rel, f = line.lower().strip().split('\t')
            except ValueError:
                continue
            if int(f) >= 10:
                rel = rel.replace(' ', '_')
                freq_dict.add(rel)
    print(len(freq_dict), 'relations filtered by frequency')
    relations = set()
    relations_dict = {}
    print('Reading relations...')
    with open(PATH_IN + 'relations2.txt', 'r', encoding='utf-8') as f_in:
        for line in f_in:
            subj, pred, obj = line.lower().strip().split('\t')
            subj = subj.replace(' ', '_')
            if subj not in obj_freq:
                continue
            if subj not in relations_dict:
                relations_dict[subj] = {}
            if pred not in freq_dict:
                    continue
            col = pred + ' ' + obj
            col = col.replace(' ', '_')
            if col == '':
                continue
            relations.add(col)
            try:
                relations_dict[subj][col] += 1
            except:
                relations_dict[subj][col] = 1
    return relations, relations_dict

def create_space_attributes(obj_freq):
    freq_file = PATH_IN + 'attributes2_freq.txt'
    freq_dict = set()
    with open(freq_file, 'r', encoding='utf-8') as freq:
        for line in freq:
            att, f = line.lower().strip().split('\t')
            if int(f) >= 10:
                att = att.replace(' ', '_')
                freq_dict.add(att)
    print(len(freq_dict), 'attributes filtered by frequency')
    attributes = set()
    attributes_dict = {}
    print('Reading attributes...')
    with open(PATH_IN + 'attributes2.txt', 'r', encoding='utf-8') as f_in:
        for line in f_in:
            try:
                attrs, subj = line.lower().strip().split('\t')
            except:
                continue
            attrs_list = re.split(', ', attrs)
            attrs = [attr.replace(' ', '_') for attr in attrs_list]
            if '' in attrs:
                continue
            subj = subj.replace(' ', '_')
            if subj not in obj_freq:
                continue
            if subj not in attributes_dict:
                attributes_dict[subj] = {}
            for attr in attrs:
                if attr not in freq_dict:
                    continue
                attributes.add(attr)
                try:
                    attributes_dict[subj][attr] += 1
                except:
                    attributes_dict[subj][attr] = 1
    return attributes, attributes_dict
                    
def write_files(attributes, attributes_dict):
    print('Writing everything down...')
    with open(PATH_OUT + 'relations_f10.cols', 'w', encoding='utf-8') as f_out:
        for attr in attributes:
            f_out.write(attr + '\n')
    with open(PATH_OUT + 'relations_f10.rows', 'w', encoding='utf-8') as f_out:
        for obj in attributes_dict:
            f_out.write(obj + '\n')
    with open(PATH_OUT + 'relations_f10.sm', 'w', encoding='utf-8') as f_out:
        for obj in attributes_dict:
            for attr in attributes_dict[obj]:
                f_out.write(obj + ' ' + attr + ' ' + str(attributes_dict[obj][attr]) + '\n')

#att1, att2 = create_space_attributes(obj_freq)
rel1, rel2 = create_space_relations(obj_freq)
write_files(rel1, rel2)
