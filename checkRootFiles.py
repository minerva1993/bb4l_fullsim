import sys, os
import glob
import multiprocessing
import argparse
import re
from subprocess import check_call

from ROOT import *
import ROOT

parser = argparse.ArgumentParser(usage="%prog [options]")
parser.add_argument("-I", "--input", dest="input_folder", type=str, default="miniTree_", help="Input folder. You can change this to run `check_zombie` over mergedMiniTree folder")
parser.add_argument("-N", "--file_number", dest="file_number", nargs='*', help="Min and max file number for partial checks")
options = parser.parse_args()


file_list = os.listdir(options.input_folder)

print('Cheking: ' + os.path.join(options.input_folder))

if not options.file_number:
    pass
elif len(options.file_number) == 2 and int(options.file_number[0]) < int(options.file_number[1]):
    print("Running on the range of ", options.file_number)
    low = int(options.file_number[0])
    high = int(options.file_number[1])
    file_list = [f for f in file_list if low <= int(f.split('_')[-1].replace('.root', '')) <= high]
else:
    print("Check file number range!!! Exiting...")
    sys.exit()

total = len(file_list)
for i, input_file in enumerate(file_list, 1):

    bar_width = 50
    filled = int(bar_width * i / total)
    bar = ">" * filled + " " * (bar_width - filled)
    sys.stdout.write("\r[{}] {}/{} {:<50}".format(bar, i, total, input_file))
    #sys.stdout.write("\r[{}/{}] Checking: {:<50}".format(i, total, input_file))
    sys.stdout.flush()

    try:
        f = TFile.Open(os.path.join(options.input_folder, input_file))
        if f.IsZombie():
            print("input_file ", input_file, " is boken, please delete...")
            #os.remove(input_file)
        elif f.TestBit(ROOT.TFile.kRecovered):
            print("input_file ", input_file, " is missing keys, please delete...")
            #os.remove(input_file)
        elif f.GetNkeys() < 1:
            print("input_file ", input_file, " has no keys, please delete...")
            #os.remove(input_file)
        else:
            f.Close()
    except:
        print("Cannot open the file ", input_file, " plase delete...")
        #os.remove(input_file)

sys.stdout.write("\n")
sys.stdout.flush()
