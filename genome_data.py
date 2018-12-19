from visual_genome import api
import codecs

#ids = api.get_image_ids_in_range(start_index=2000, end_index=2010)
ids = api.get_all_image_ids() 
# ids = xrange(107899, 107999)
all_descr = []
processed_ids = set([int(line.strip()) for line in codecs.open('processed_ids.txt', 'r', 'utf-8').readlines()])
w = codecs.open('descriptions_full.txt', 'a', 'utf-8')
w2 = codecs.open('processed_ids.txt', 'a', 'utf-8')
for i in ids:
    if i in processed_ids:
        continue
    print(i)
    w2.write(str(i) + '\n')
    #image = api.get_image_data(id=i)
    regions_set = set()
    try:
        regions = api.get_region_descriptions_of_image(id=i)
    except IndexError:
        continue
    for region in regions:
        regions_set.add(region.phrase)
    for reg in regions_set:
        w.write(reg + '\n')

w.close()
w2.close()


    
