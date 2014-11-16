
import sys
import os
import time
import subprocess
import argparse
import shutil

import git

def get_result_dir_name():
	current_dir = os.getcwd().split("/")[-1]
	return "log/" + current_dir + "." + time.strftime("%Y.%m.%d.%H.%M.%S")

#from http://stackoverflow.com/questions/377017/test-if-executable-exists-in-python
def which(program):
    import os
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None

def use_cli_or_config(v1,v2):
	if v1 == None and v2 == None:
		return None
	elif v1 != None:
		return v1
	else:
		return v2

def get_program_path(args,configs):
	prog_path = use_cli_or_config(args.program,configs.program)
	if prog_path == None:
		raise ValueError("run::get_program_path need to set either args.program or configs.program to know what program to run for this test")

	os.chdir("log")
	exe_file = which(prog_path)
	if exe_file != None:
		return exe_file
	os.chdir("../")

	#path is relative 
	return os.getcwd() + "/" + prog_path

def run_process(args,configs):
	#no log yet
	if not os.path.isdir("log"):
		os.mkdir("log")

	current_path = os.getcwd()
	git_repo = git.GitRepo.factory(configs.git_repo)
	log_dir = get_result_dir_name()
	program_path = get_program_path(args,configs)

	os.mkdir(os.getcwd() + "/" + log_dir)
	print "running test in ",log_dir

	if args.files:
		files = args.files.split(",")
		for f in files:
			shutil.copy(f, os.getcwd() + "/" + log_dir)

	os.chdir( os.getcwd() + "/" + log_dir)

	command = program_path
	if args.args:
		command += " " + args.args
		f=open("args","w")
		f.write(args.args)
		f.close()

	f=open("message","w")
	f.write(args.message)
	f.close()

	t0 = time.clock()
	outfile = open("output","w")
	subprocess.call(command,shell=True,universal_newlines=True, stdout=outfile)
	outfile.close()

	statfile = open("stats","w")
	statfile.write("time: " + str(time.clock() - t0) + "\n")
	statfile.close() 

	os.chdir(current_path)
	git_repo.add("-A")
	git_repo.commit("-m "+args.message)









