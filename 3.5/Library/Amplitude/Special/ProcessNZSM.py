import os
import shutil

from pyarma import *

input_folder = 'NZ'
output_folder = 'OUTPUT'

try:
    # try to create folder
    os.mkdir(output_folder)
except OSError:
    # if folder exists, remove it and create an empty one
    shutil.rmtree(output_folder)
    os.mkdir(output_folder)

os.mkdir(output_folder + '\\A')
os.mkdir(output_folder + '\\V')
os.mkdir(output_folder + '\\D')

for record in os.listdir(input_folder):
    print(record)
    motion_name = record.replace('_V2A.csv', '')
    file = open(input_folder + '\\' + record, 'r')
    lines = file.readlines()
    lines.pop(0)
    component_list = lines.pop(0).replace(' ', '').replace('\n', '').split(',')
    component_list[1] += '_A'
    component_list[2] += '_A'
    component_list[3] += '_A'
    component_list[4] += '_V'
    component_list[5] += '_V'
    component_list[6] += '_V'
    component_list[7] += '_D'
    component_list[8] += '_D'
    component_list[9] += '_D'
    lines.pop(0)
    lines.pop(0)
    lines.pop(0)
    output = open(output_folder + '\\' + motion_name, 'w')
    output.writelines(lines)
    output.close()
    motion = mat()
    motion.load(output_folder + '\\' + motion_name, csv_ascii)
    motion *= 1000.
    incre_time = motion[1, 0] - motion[0, 0]
    for i in range(1, motion.n_cols):
        file_dest = output_folder
        if i < 4:
            file_dest += '\\A'
        elif i < 7:
            file_dest += '\\V'
        else:
            file_dest += '\\D'
        file_dest += '\\' + motion_name + '_' + component_list[i]
        output = open(file_dest, 'w')
        output.write('{}\n'.format(int(incre_time)))
        max_amp = motion[:, i].max()
        min_amp = motion[:, i].min()
        output.write('{}\n'.format(int(max_amp if max_amp > -min_amp else -min_amp)))
        for j in range(0, motion.n_rows):
            output.write('{}\n'.format(int(motion[j, i])))
        output.close()
    os.remove(output_folder + '\\' + motion_name)
