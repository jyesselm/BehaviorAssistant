#!/usr/bin/env python
import os

#BA modules
import log
import git
#import render
import config
#import template
import cli
import run
import notifications



if __name__ == '__main__':

    # Brief sketch follows
    args = cli.parse_cli()
    configs = config.get_configurations(os.getcwd())
    run.run_process(args, configs)


