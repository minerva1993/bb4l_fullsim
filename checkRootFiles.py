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
options = parser.parse_args()


file_list = os.listdir(options.input_folder)

print('Cheking: ' + os.path.join(options.input_folder))


for input_file in file_list:

    try:
        f = TFile.Open(os.path.join(options.input_folder, input_file))
        if f.IsZombie():
            print("input_file ", input_file, " is boken, deleting...")
            #os.remove(input_file)
        elif f.TestBit(ROOT.TFile.kRecovered):
            print("input_file ", input_file, " is missing keys, deleting...")
            #os.remove(input_file)
        elif f.GetNkeys() < 1:
            print("input_file ", input_file, " has no keys, deleting...")
            #os.remove(input_file)
        else:
            f.Close()
    except:
        print("Cannot open the file ", input_file, " deleting...")
        #os.remove(input_file)
