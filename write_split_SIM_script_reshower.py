from __future__ import division
import os, sys
import re
import argparse

parser = argparse.ArgumentParser(usage="%prog [options]")
parser.add_argument("-Y", "--year", dest="year", type=str, default="", help="Select ul16pre, ul16post, ul17, or ul18")
parser.add_argument("-I", "--input", dest="input", type=str, default="", help="Input LHE folder name")
parser.add_argument("-W", "--width", dest="width", type=str, default="1p0", help="Uncertainty flag")
parser.add_argument("-M", "--maxevents", dest="maxevents", type=int, default=1000, help="Max N events per job")
options = parser.parse_args()

JOBS_PER_SUBMIT = 4000

pattern = re.compile(r"^LHE_(\d+)\.lhe$")
lhe_files = []

for d in sorted(os.listdir(options.input)):
    dpath = os.path.join(options.input, d)
    if not os.path.isdir(dpath):
        continue
    for f in sorted(os.listdir(dpath)):
        m = pattern.match(f)
        if m:
            lhe_files.append((dpath, int(m.group(1))))

lhe_files.sort(key=lambda x: (x[0], x[1]))


def count_events(filepath):
    n = 0
    with open(filepath, "r") as f:
        for line in f:
            if line.strip() == "<event>":
                n += 1
    return n


input_file = "template_bb4l_UNC_gen_to_sim_ERA"
base_output = ("template_bb4l_UNC_gen_to_sim_ERA"
               .replace("template", "submit")
               .replace("UNC", options.width)
               .replace("ERA",   options.year))

with open(input_file) as f:
    template = f.readlines()


submit_index        = 0
jobs_in_file        = 0
global_job_num      = 0
total_lhe_processed = 0
out                 = None

def open_next(base, idx):
    name = "{}_part{}".format(base, idx)
    print("Opening new submit file: {}".format(name))
    return open(name, "w")

for (dpath, i) in lhe_files:
    filepath = os.path.join(dpath, "LHE_{}.lhe".format(i))
    n_events = count_events(filepath)

    total_lhe_processed += 1

    # Each job processes [skipevent, skipevent + maxevents) - last chunk may be smaller
    for skipevent in range(0, n_events, options.maxevents):
        events_this_job = min(options.maxevents, n_events - skipevent)

        if out is None or jobs_in_file >= JOBS_PER_SUBMIT:
            if out is not None:
                out.close()
            out = open_next(base_output, submit_index)
            submit_index += 1
            jobs_in_file = 0

        for line in template:
            if line.startswith("JobBatchName"):
                line = line.replace("UNC", options.width).replace("ERA", options.year + '_part' + str(submit_index-1))
            if line.startswith("Executable"):
                line = line.replace("ERA", options.year)\
                           .replace("UNC", options.width)
            if line.startswith("Args"):
                line = line.replace("INPUT",     os.path.join(options.input, dpath))\
                           .replace("MAXEVENT",  str(events_this_job))\
                           .replace("SKIPEVENT", str(skipevent))\
                           .replace("FILENUMBER",str(i))\
                           .replace("OUTNUMBER", str(global_job_num))
            if line.startswith("Log") or line.startswith("Output") or line.startswith("Error"):
                line = (line.replace("UNC",     options.width)
                            .replace("OUTNUMBER", str(global_job_num)))
            if line.strip().startswith("Queue"):
                line = "Queue\n"
            out.write(line)

        out.write("\n")
        jobs_in_file   += 1
        global_job_num += 1

if out is not None:
    out.close()

print("\nProcessed {} LHE files".format(total_lhe_processed))
print("Total jobs: {}, split across {} submit file(s) (~{} jobs each)".format(global_job_num, submit_index, JOBS_PER_SUBMIT))
print("Output files: {}_part0 ... {}_part{}".format(base_output, base_output, str(submit_index-1)))
