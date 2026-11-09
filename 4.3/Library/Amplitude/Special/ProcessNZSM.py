#!/usr/bin/env python3

# The records are first converted to CSV files using the official utility (https://www.geonet.org.nz/data/supplementary/strong_motion_file_formats).
# This script processes the CSV files and generate compact single column files for each component.

import os
import shutil
from pathlib import Path
import numpy as np


input_folder = "NZ"
output_folder = "OUTPUT"

try:
    # try to create folder
    os.mkdir(output_folder)
except OSError:
    # if folder exists, remove it and create an empty one
    shutil.rmtree(output_folder)
    os.mkdir(output_folder)

os.mkdir(output_folder + "\\A")
os.mkdir(output_folder + "\\V")
os.mkdir(output_folder + "\\D")

for record in os.listdir(input_folder):
    print(record)
    motion_name = record.replace("_V2A.csv", "")
    lines = (Path(input_folder) / record).read_text().splitlines()
    lines.pop(0)
    component_list = lines.pop(0).replace(" ", "").replace("\n", "").split(",")
    component_list[1] += "_A"
    component_list[2] += "_A"
    component_list[3] += "_A"
    component_list[4] += "_V"
    component_list[5] += "_V"
    component_list[6] += "_V"
    component_list[7] += "_D"
    component_list[8] += "_D"
    component_list[9] += "_D"
    lines.pop(0)
    lines.pop(0)
    lines.pop(0)
    output_motion = Path(output_folder) / motion_name
    output_motion.write_text("\n".join(lines))
    motion: np.ndarray = np.genfromtxt(output_motion.as_posix(), delimiter=",")
    motion *= 1000.0
    incre_time = motion[1, 0] - motion[0, 0]
    for i in range(1, motion.shape[1]):
        file_dest = output_folder
        if i < 4:
            file_dest += "\\A"
        elif i < 7:
            file_dest += "\\V"
        else:
            file_dest += "\\D"
        file_dest += "\\" + motion_name + "_" + component_list[i]
        with open(file_dest, "w") as output:
            output.write("{}\n".format(int(incre_time)))
            max_amp = motion[:, i].max()
            min_amp = motion[:, i].min()
            output.write(
                "{}\n".format(int(max_amp if max_amp > -min_amp else -min_amp))
            )
            for j in range(0, motion.shape[0]):
                output.write("{}\n".format(int(motion[j, i])))
    output_motion.unlink()
