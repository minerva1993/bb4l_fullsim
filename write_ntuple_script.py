import os, sys
import argparse
from collections import OrderedDict

parser = argparse.ArgumentParser(usage="%prog [options]")
parser.add_argument("-Y", "--year", dest="year", type=str, default="", help="Select ul16apv, ul16, ul17, or ul18")
parser.add_argument("-I", "--input", dest="input", type=str, default="", help="Input MINIAOD folder name")
parser.add_argument("-O", "--outfolder", dest="outfolder", type=str, default="", help="Output folder name")
parser.add_argument("-W", "--width", dest="width", type=str, default="1p0", help="Width flag, 0p7 or 1p3")
parser.add_argument("--workflow", dest="workflow", type=str, default="MC_bb4l_2018", help="Workflow name")
options = parser.parse_args()

# Count the maximum file number; can be differ from number of files due to broken jobs

n_files = 0
file_dict = OrderedDict()

for f in os.listdir(options.input):
    if f.endswith("root"):
        fullpath = os.path.join(options.input, f)
        file_dict[n_files] = fullpath
        n_files += 1

file_dict = OrderedDict(
    sorted(file_dict.items(), key=lambda x: x[1])
)

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

            if line.strip().startswith("Queue"):
                line = "Queue\n"

            out.write(line)

        out.write("\n")  # separate job blocks

print("To submit", str(n_files), "files")
print("Written submit file:", output_file)
