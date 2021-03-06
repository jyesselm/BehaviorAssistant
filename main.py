import argparse
import log
import render
import config
import template
import notifications
import os

def parse_args():
    parser = argparse.ArgumentParser(description='')

    parser.add_argument('-p', help='program', required=True)
    parser.add_argument('-args', required=False)
    parser.add_argument('-files',required=False)
    args = parser.parse_args()
    return args

if __name__ == '__main__':

    # Brief sketch follows
    args = parse_args()
    config = get_configuration(os.getcwd())
    log = log.Log(config)
    if args.render is not None:
        # This means we render stuff in whatever renderer was specified 
        # in args.render (e.g. html or latex)
        log_entries = log.read(args.since, args.until)
        renderer = render.
        renderer.render(log_entries)
    else:
        # Then this is a commit
        needs_push = log.commit(args.command, args.command_args, template=args.template)
        if needs_push:
            notifications.show('According to your current configuration you need to push now!')
            while True:
                answer = notifications.input('Do you want to push? ([y]/n ').lower().strip()
                if answer[0] == 'n':
                    notifications.show('Skipping push per user input')
                    break
                elif answer[0] == 'y':
                    notifications.show('Pushing...')
                    log.push()
                    break
                else:
                    notifications.show('Invalid answer')




