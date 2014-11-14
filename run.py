
import os
import glob 
import time
import subprocess
import argparse
import shutil

def parse_args():
	parser = argparse.ArgumentParser(description='')

	parser.add_argument('-p', help='program', required=True)
	parser.add_argument('-args', required=False)
	parser.add_argument('-files',required=False)
	args = parser.parse_args()
	return args

def get_result_dir_name():
	current_dir = os.getcwd().split("/")[-1]
	return "results/" + current_dir + "." + time.strftime("%Y.%m.%d.%H.%M.%S")

args = parse_args()

current_dir = get_result_dir_name()
os.mkdir(os.getcwd() + "/" + current_dir)
print "running test in ",current_dir

if args.files:
	files = args.files.split(",")
	for f in files:
		shutil.copy(f, os.getcwd() + "/" + current_dir)

os.chdir( os.getcwd() + "/" + current_dir)

command = args.p
if args.args:
	command += " " + args.args
	f=open("args","w")
	f.write(args.args)
	f.close()

t0 = time.clock()
logfile = open("log","w")
subprocess.call(command,shell=True,universal_newlines=True, stdout=logfile)
logfile.close()

statfile = open("stats","w")
statfile.write("time: " + str(time.clock() - t0) + "\n")
statfile.close() 







