import os, sys
import re
import gzip
import argparse

parser = argparse.ArgumentParser(usage="%prog [options]")
parser.add_argument("-Y", "--year", dest="year", type=str, default="", help="Select ul16apv, ul16, ul17, or ul18")
parser.add_argument("-I", "--input", dest="input", type=str, default="", help="Input LHE folder name")
parser.add_argument("-W", "--width", dest="width", type=str, default="1p0", help="Width flag, 0p7 or 1p3")
options = parser.parse_args()

# Count the maximum file number; can be differ from number of files due to broken jobs
pattern = re.compile(r"^SIM_(\d+)\.root$")

numbers = []
for f in os.listdir(options.input):
    m = pattern.match(f)
    if m:
        numbers.append(int(m.group(1)))

if numbers:
    max_number = max(numbers)
else:
    max_number = None


input_file = "template_bb4l_widthWIDTH_sim_to_mini_ERA"
output_file = "template_bb4l_widthWIDTH_sim_to_mini_ERA".replace("template", "submit").replace("WIDTH", options.width).replace("ERA", options.year)

with open(input_file) as f:
    template = f.readlines()

n_files = 0

with open(output_file, "w") as out:

    for i in range(max_number+1):

        if not os.path.exists(os.path.join(options.input, "SIM_" + str(i) + ".root")):
            continue

        for line in template:

            if line.startswith("JobBatchName"):
                line = line.replace("WIDTH", options.width).replace("ERA", options.year)

            if line.startswith("Executable"):
                line = line.replace("ERA", options.year)

            if line.startswith("Args"):
                line = line.replace("INPUT", options.input)\
                           .replace("FILENUMBER", str(i))\

            if line.strip().startswith("Queue"):
                line = "Queue\n"

            out.write(line)

        out.write("\n")  # separate job blocks

        n_files += 1

print("To submit", str(n_files), "files")
print("Written submit file:", output_file)
