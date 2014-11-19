import sys
import time
import subprocess
import argparse
import shutil
import os

import notifications
import log as logging
import config
import render

#from http://stackoverflow.com/questions/377017/test-if-executable-exists-in-python
def which(command):
    import os
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(command)
    if fpath:
        if is_exe(command):
            return command
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip("'")
            exe_file = os.path.join(path, command)
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

def get_command_path(args,configs):
    #TODO setup proper options for command path in configs
    #prog_path = use_cli_or_config(args.command, configs)
    prog_path = args.command
    return prog_path
    if prog_path == None:
        raise ValueError("run::get_command_path need to set either args.command or configs.program to know what program to run for this test")

    os.chdir("log")
    exe_file = which(prog_path)
    if exe_file != None:
        return exe_file
    os.chdir("../")

    #path is relative 
    return os.getcwd() + "/" + prog_path

def run_process(args, configs):
    log = logging.Log(configs)
    if args.render is not None:
        # This means we render stuff in whatever renderer was specified 
        # in args.render (e.g. html or latex)
        log_entries = log.read(args.since, args.until)
        renderer = render.get_renderer(args.render)
        renderer_output = renderer.render(log_entries, configs)
        args.renderout.write(renderer_output)
        args.renderout.close()
    else:
        # This means we run a command and commit
        command_path = get_command_path(args, configs)
        
        notifications.show("running command %s" % (args.command))
        
        """
        if args.files:
            files = args.files.split(",")
            for f in files:
                shutil.copy(f, os.getcwd() + "/" + log.log_dir)
        """

        command = command_path
        if args.args:
            command += " " + args.args
            f=open("args","w")
            f.write(args.args)
            f.close()
        
        t0 = time.clock()
        print command
        process = subprocess.Popen(command, shell=True, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        
        commit_content_dict, needs_push = log.commit(args.command, args.args, args.message, out, err, command_run_time=t0)
        # TODO command should be command_path
        # TODO also command sanitization, e.g. getting rid of ./ should be elsewhere
        log.move_resources_to_resource_dir(commit_content_dict, configs.templates[command.split()[0].strip("./")])
        if needs_push:
            notifications.show("According to your current configuration you need to push now!")
            while True:
                answer = notifications.input("Do you want to push? ([y]/n ").lower().strip()
                if answer[0] == "n":
                    notifications.show("Skipping push per user input")
                    break
                elif answer[0] == "y":
                    notifications.show("Pushing...")
                    log.push()
                    break
                else:
                    notifications.show("Invalid answer")





