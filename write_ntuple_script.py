import os, sys
import re
import argparse
from collections import OrderedDict

parser = argparse.ArgumentParser(usage="%prog [options]")
parser.add_argument("-Y", "--year", dest="year", type=str, default="", help="Select ul16apv, ul16, ul17, or ul18")
parser.add_argument("-I", "--input", dest="input", type=str, default="", help="Input MINIAOD folder name")
parser.add_argument("-J", "--jobid", dest="jobid", type=int, default=-1, help="Input MINIAOD jobid")
parser.add_argument("-O", "--outfolder", dest="outfolder", type=str, default="", help="Output folder name")
parser.add_argument("-W", "--width", dest="width", type=str, default="1p0", help="Width flag, 0p7 or 1p3")
parser.add_argument("--workflow", dest="workflow", type=str, default="MC_bb4l_2018", help="Workflow name")
parser.add_argument("-N", "--number", dest="number_start", type=int, default=0, help="Starting file number in case of sample addition")
options = parser.parse_args()

# Count the maximum file number; can be differ from number of files due to broken jobs

n_files = options.number_start
file_dict = OrderedDict()

for f in os.listdir(options.input):
    if f.endswith("root"):
        if options.jobid > 0:
            if str(options.jobid) not in f: continue
        fullpath = os.path.join(options.input, f)
        file_dict[n_files] = fullpath
        n_files += 1

sorted_values = sorted(file_dict.values(), key=lambda x: [int(n) for n in re.findall(r'\d+', os.path.basename(x))])

file_dict = OrderedDict(zip(file_dict.keys(), sorted_values))

input_file = "template_bb4l_widthWIDTH_mini_to_ntuple_ERA"
output_file = "template_bb4l_widthWIDTH_mini_to_ntuple_ERA".replace("template", "submit").replace("WIDTH", options.width).replace("ERA", options.year)

with open(input_file) as f:
    template = f.readlines()

with open(output_file, "w") as out:

    for i, filepath in file_dict.items():

        for line in template:

            if line.startswith("JobBatchName"):
                line = line.replace("WIDTH", options.width).replace("ERA", options.year)

            if line.startswith("Executable"):
                line = line.replace("ERA", options.year)

            if line.startswith("Args"):
                line = line.replace("INFILE", filepath)\
                           .replace("OUTFOLDER", options.outfolder)\
                           .replace("OUTNUMBER", str(i))\
                           .replace("WORKFLOW", options.workflow)

            if line.startswith("Log") or line.startswith("Output") or line.startswith("Error"):
                line = line.replace("WIDTH", options.width)\
                           .replace("OUTNUMBER", str(i))

            if line.strip().startswith("Queue"):
                line = "Queue\n"

            out.write(line)

        out.write("\n")  # separate job blocks

#print("To submit", str(n_files), "files")
print("To submit", str(len(file_dict.keys())), "files")
print("Written submit file:", output_file)
