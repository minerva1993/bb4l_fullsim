#!/usr/bin/env python2

import os
import re
import argparse

parser = argparse.ArgumentParser(description="Create edmCopyPickMerge script")
parser.add_argument("-I", "--input", required=True, help="Input directory containing ntuple files")
parser.add_argument("-N", "--chunk-size", type=int, default=20, help="Number of files per merge (default: 100)")
options = parser.parse_args()


# check width string
m_width = re.search(r'(twidthx[0-9p]+)', options.input)
if not m_width:
    print("Cannot find twidth in directory name")
    exit(1)

twidth_tag = m_width.group(1)

output_script = "run_ntuple_merge_%s.sh" % twidth_tag

# Get file list
files = []
file_name_base = ""

for f in os.listdir(options.input):
    if f.endswith("root"):
        file_name_base = re.sub(r'\d+\.root$', '', f)
        fullpath = os.path.join(options.input, f)
        files.append(fullpath)

files.sort(key=lambda x: int(re.findall(r'\d+', x)[-1]))
print(files)
#files = [f[1] for f in files]

chunks = [files[i:i+options.chunk_size] for i in range(0, len(files), options.chunk_size)]

out_folder = "merged_%s" % options.input
if not os.path.exists(out_folder):
    os.makedirs(out_folder)

# write script
with open(output_script, "w") as out:
    out.write("#!/bin/bash\n\n")

    for i, chunk in enumerate(chunks):
        input_string = " ".join(
            ["%s" % f for f in chunk]
        )

        output_file = "%s%d.root" % (file_name_base, i)

        cmd = ("hadd -f %s %s \n" % (os.path.join(out_folder, output_file), input_string))

        out.write(cmd)

print("Created:", output_script)
print("Total input files:", len(files))
print("Total merge jobs:", len(chunks))
