import os, sys
import re
import gzip
import argparse

parser = argparse.ArgumentParser(usage="%prog [options]")
parser.add_argument("-Y", "--year", dest="year", type=str, default="", help="Select ul16apv, ul16, ul17, or ul18")
parser.add_argument("-I", "--input", dest="input", type=str, default="", help="Input LHE folder name")
parser.add_argument("-W", "--width", dest="width", type=str, default="1p0", help="Width flag, 0p7 or 1p3")
parser.add_argument("-M", "--maxevents", dest="maxevents", type=int, default="1000", help="Number of events per job")
options = parser.parse_args()

# Count the maximum file number; can be differ from number of files due to broken jobs
pattern = re.compile(r"^LHE_(\d+)\.lhe.gz$")

numbers = []
for f in os.listdir(options.input):
    m = pattern.match(f)
    if m:
        numbers.append(int(m.group(1)))

if numbers:
    max_number = max(numbers)
else:
    max_number = None

file_to_count = ""
if (os.path.exists(os.path.join(options.input, "LHE_0.lhe.gz"))): file_to_count = "LHE_0.lhe.gz"
else: file_to_count = "LHE_1.lhe.gz"

n_events = 0
with gzip.open(os.path.join(options.input, file_to_count), "rt") as f:   # "rt" = read text mode
    for line in f:
        if line.strip() == "<event>":
            n_events += 1

n_jobs_per_file = n_events / options.maxevents

if(options.maxevents > n_events):
    print("Maxevents is greater than total event in a file!")
    sys.exit()
if isinstance(n_jobs_per_file, int):
    pass
elif isinstance(x, float):
    if n_jobs_per_file.is_integer():
        pass
    else:
        print("Nevents cannot be divided by maxevents!")
        sys.exit()

n_jobs_per_file = int(n_jobs_per_file)

input_file = "template_bb4l_widthWIDTH_gen_to_sim_ERA_multiQ"
output_file = "template_bb4l_widthWIDTH_gen_to_sim_ERA_multiQ".replace("template", "submit").replace("WIDTH", options.width).replace("ERA", options.year)

with open(input_file) as f:
    template = f.readlines()

n_files = 0

with open(output_file, "w") as out:

    for line in template:

        if line.startswith("JobBatchName"):
            line = line.replace("WIDTH", options.width).replace("ERA", options.year)

        if line.startswith("Executable"):
            line = line.replace("ERA", options.year)

        if line.startswith("Args"):
            line = line.replace("INPUT", options.input)\
                       .replace("MAXEVENT", str(options.maxevents))

        out.write(line)

    out.write("queue FILENUMBER, SKIPEVENT, OUTNUMBER from (")


    for i in range(max_number+1):

        if not os.path.exists(os.path.join(options.input, "LHE_" + str(i) + ".lhe.gz")):
            continue

        for j in range(n_jobs_per_file):
            skipevent = int(options.maxevents * j)

            line = str(i) + " " + str(skipevent) + " " + str(int(n_files * n_jobs_per_file) + j) + "\n"
            out.write(line)

        n_files += 1

    out.write(")")

print("To submit", str(n_files), "files, split per", options.maxevents, "events, resulting in", str(int(n_files * n_events / options.maxevents)), "jobs")
print("Written submit file:", output_file)
