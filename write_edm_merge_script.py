#!/usr/bin/env python2

import os
import re
import argparse

parser = argparse.ArgumentParser(description="Create edmCopyPickMerge script")
parser.add_argument("-I", "--input", required=True, help="Input directory containing MINIv2_X.root files")
parser.add_argument("-N", "--chunk-size", type=int, default=100, help="Number of files per merge (default: 100)")
options = parser.parse_args()


# check width string
m_width = re.search(r'(twidthx[0-9p]+)', options.input)
if not m_width:
    print "Cannot find twidth in directory name"
    exit(1)

twidth_tag = m_width.group(1)

# input job number
m_job = re.search(r'_([0-9]+)_SIM', options.input)
if not m_job:
    print "Cannot find job number in directory name"
    exit(1)

job_number = m_job.group(1)

output_script = "run_merge_%s_%s.sh" % (twidth_tag, job_number)


# Get file list
pattern = re.compile(r"MINIv2_(\d+)\.root$")
files = []

for f in os.listdir(options.input):
    m = pattern.match(f)
    if m:
        files.append((int(m.group(1)), f))

if not files:
    print "No MINIv2_X.root files found."
    exit(1)

files.sort()
files = [f[1] for f in files]

chunks = [files[i:i+options.chunk_size] for i in range(0, len(files), options.chunk_size)]

out_folder = "miniaodv2_%s" % twidth_tag
if not os.path.exists(out_folder):
    os.makedirs(out_folder)

# write script
with open(output_script, "w") as out:
    out.write("#!/bin/bash\n\n")

    for i, chunk in enumerate(chunks):
        input_string = ",".join(
            ["file:%s" % (os.path.join(options.input, f)) for f in chunk]
        )

        output_file = "merged_%s_%s_%d.root" % (twidth_tag, job_number, i)

        cmd = (
            "cmsRun copyPickMerge_cfg.py "
            "inputFiles=%s "
            "outputFile=%s "
            "maxSize=10000000\n" % (input_string, os.path.join(out_folder, output_file))
        )

        out.write(cmd)

print "Created:", output_script
print "Total input files:", len(files)
print "Total merge jobs:", len(chunks)
