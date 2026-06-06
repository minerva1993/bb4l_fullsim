import os, sys
import re
import argparse

parser = argparse.ArgumentParser(usage="%prog [options]")
parser.add_argument("-Y", "--year", dest="year", type=str, default="", help="Select ul16apv, ul16, ul17, or ul18")
parser.add_argument("-I", "--input", dest="input", type=str, default="", help="Input LHE folder name")
parser.add_argument("-W", "--width", dest="width", type=str, default="1p0", help="Width flag, 0p7 or 1p3")
parser.add_argument("--minjobid", dest="minjobid", type=int, default=0, help="Min jobid for condor job")
parser.add_argument("--maxjobid", dest="maxjobid", type=int, default=0, help="Min jobid for condor job")
parser.add_argument("--postfix", dest="postfix", type=str, default="", help="output name postfix")
options = parser.parse_args()

# Count the maximum file number; can be differ from number of files due to broken jobs
pattern = re.compile(r"^SIM_(\d+)\.root$")

min_number = 0
max_number = 0

numbers = []
for f in os.listdir(options.input):
    m = pattern.match(f)
    if m:
        numbers.append(int(m.group(1)))

if options.minjobid == 0 and options.maxjobid == 0:
    if numbers:
        max_number = max(numbers)
    else:
        max_number = None
else:
    min_number = options.minjobid
    max_number = options.maxjobid


input_file = "template_bb4l_UNC_sim_to_mini_ERA"
output_file = "template_bb4l_UNC_sim_to_mini_ERA".replace("template", "submit").replace("UNC", options.width).replace("ERA", options.year)

if len(options.postfix) > 0:
    output_file += "_" + options.postfix

with open(input_file) as f:
    template = f.readlines()

n_files = 0

with open(output_file, "w") as out:

    for i in range(min_number, max_number+1):

        if not os.path.exists(os.path.join(options.input, "SIM_" + str(i) + ".root")):
            continue

        for line in template:

            if line.startswith("JobBatchName"):
                line = line.replace("UNC", options.width).replace("ERA", options.year)

                if len(options.postfix) > 0:
                    line = line.replace('"\n', "_"+options.postfix+'"\n')

            if line.startswith("Executable"):
                line = line.replace("ERA", options.year)

            if line.startswith("Args"):
                line = line.replace("INPUT", options.input)\
                           .replace("FILENUMBER", str(i))\

            if line.startswith("Log") or line.startswith("Output") or line.startswith("Error"):
                line = line.replace("UNC", options.width)\
                           .replace("FILENUMBER",  str(i))


            if line.strip().startswith("Queue"):
                line = "Queue\n"

            out.write(line)

        out.write("\n")  # separate job blocks

        n_files += 1

print("To submit", str(n_files), "files")
print("Written submit file:", output_file)
