
import subprocess
import shutil
import os
import sys
import time

import BehaviorAssistant.git as git

if os.path.isdir("git_repo"):
	shutil.rmtree("git_repo")
os.mkdir("git_repo")

if os.path.isdir("log"):
	shutil.rmtree("log")

f = open("git_repo/contributions.txt","w")
f.write("jyesselm\n")
f.close()

git_repo = git.GitRepo.factory("git_repo")
git_repo("init")
git_repo.add("-A")
git_repo.commit("-m init commit")

shutil.copy("script.py","git_repo/script.py")
subprocess.call('ba.py -m "first commit" -args test_arg ',shell=True)
time.sleep(2)

shutil.copy("script_2.py","git_repo/script.py")
subprocess.call('ba.py -m "second commit" -args test_arg ',shell=True)
time.sleep(2)

shutil.copy("script_3.py","git_repo/script.py")
subprocess.call('ba.py -m "third commit" -args test_arg ',shell=True)