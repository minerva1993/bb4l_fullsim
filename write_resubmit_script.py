import sys, os
import re
import argparse

pairs = []

parser = argparse.ArgumentParser(usage="%prog [options]")
parser.add_argument("-I", "--input", dest="input_file", type=str, default="", help="Input submission script")
parser.add_argument("-O", "--output", dest="output", type=str, default="", help="output folder, optional for root file existence check")
options = parser.parse_args()

check_missing = False

if not sys.stdin.isatty():
    for line in sys.stdin:
        fname = line.strip()

        # match err_Cluster_Process.txt
        m = re.search(r"err_(\d+)_(\d+)\.txt$", fname)

        if "_2.txt" in fname:
            m = re.search(r"err_(\d+)_(\d+)\_2.txt$", fname)
        if m:
            cluster = int(m.group(1))
            process = int(m.group(2))
            pairs.append([cluster, process])

if len(pairs) < 1 or len(options.output) > 0:
    check_missing = True

missing_numbers = []
job_id = ""

if check_missing:

    if "gen_to_sim" in options.input_file:

        njobs = 0

        with open(options.input_file) as f:
            for line in f:
                if "Queue" in line:
                    njobs += 1

        for i in range(njobs):
            out_file = os.path.join(options.output, "SIM_%s.root" % i)

            if not os.path.exists(out_file):
                missing_numbers.append(str(i))

    elif "sim_to_mini" in options.input_file:

        with open(options.input_file) as f:
            for line in f:
                line = line.strip()
                if line.startswith("Args"):
                    content = line.split('"')[1]
                    parts = content.split()

                    out_file = os.path.join(options.output, "MINIv2_%s.root" % parts[1])
                    if not os.path.exists(out_file):
                        missing_numbers.append(parts[1])


output_file = "re" + options.input_file

job_proc = 0
job_blocks = []

with open(options.input_file) as f:
    blocks = f.readlines()

    tmp_lines = []
    for line in blocks:

        if len(missing_numbers) > 0: #do this only for missing file check
            #line = line.strip()
            if line.startswith("Args"):
                content = line.split('"')[1]
                parts = content.split()
                if "gen_to_sim" in options.input_file and parts[-3] in missing_numbers:
                    pairs.append([options.output.split("out/")[-1].split("_")[0], job_proc])
                elif "sim_to_mini" in options.input_file and parts[-3] in missing_numbers:
                    pairs.append([options.output.split("out/")[-1].split("_")[0], job_proc])

        if line == "\n":
            job_blocks.append(tmp_lines)
            tmp_lines = []
            job_proc += 1
            continue
        tmp_lines.append(line)


print("To resubmit", len(pairs), "jobs")
print(pairs)

to_remove = []

with open(output_file, "w") as out:

    for cluster, process in pairs:

        tmp_block = job_blocks[process]

        for line in tmp_block:

            if line.startswith("JobBatchName"):
                line = line.rstrip().rstrip('"') + '_resubmit"\n'

            # process id and filenumber might be different!
            if line.startswith("Args"):
                content = line.split('"')[1]
                parts = content.split()
                if "gen_to_sim" in options.input_file:
                    to_remove.append(parts[4])
                elif "sim_to_mini" in options.input_file:
                    to_remove.append(parts[1])

            line = line.replace("$(Cluster)", str(cluster))
            line = line.replace("$(Process)", str(process))
            if line.strip().startswith(("Log", "Output", "Error")):
                line = re.sub(r"\.txt", r"_2.txt", line)

            out.write(line)

        out.write("\n")

print("Written resubmit file:", output_file)

print("To remove", len(pairs), "jobs")

output_file = "Remove_" + str(pairs[0][0]) + ".sh"

with open(output_file, "w") as out:

    #for cluster, process in pairs:
    for process in to_remove:

        if "gen_to_sim" in options.input_file:
            line = "rm SIM_" + str(process) + ".root"
        elif "sim_to_mini" in options.input_file:
            line = "rm MINIv2_" + str(process) + ".root"

        out.write(line)

        out.write("\n")

print("Written remove file:", output_file)
print("Get into the output folder and run it")
