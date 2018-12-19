from composes.semantic_space.space import Space
from composes.utils import io_utils
from composes.transformation.scaling.ppmi_weighting import PpmiWeighting
from composes.transformation.scaling.normalization import Normalization

PATH = 'dissect_spaces/mine/'
#ppmi weighting

#create a space from co-occurrence counts in sparse format
my_space = Space.build(data = PATH + "images_f10.sm",
                       rows = PATH + "images_f10.rows",
                       cols = PATH + "images_f10.cols",
                       format = "sm")
                       
my_space = my_space.apply(PpmiWeighting())
my_space = my_space.apply(Normalization())

#export the space in sparse format
my_space.export(PATH + "result_attributes_f10", format = "sm")
    
#export the space in dense format
#my_space.export(PATH + "result_relations_f10", format = "dm")
io_utils.save(my_space, PATH + 'result_attributes_f10.pkl')
