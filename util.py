#!/usr/bin/env python3
import subprocess
import sys, os


def warn(msg):
    print('\033[1;33m' + str(msg) + '\033[0;0m')

def die(msg):
    print('\033[1;31m' + str(msg) + '\033[0;0m')
    sys.exit(1)

# Synchronously runs a command on the local system, and returns a list of lines that that command sent to STDOUT.
def run_cmd(cmd, cwd=None):
    lines = []
    if sys.version_info >= (2,7):
        lines = str(subprocess.check_output(cmd, shell=True, cwd=cwd), 'utf-8').split('\n')
    else:
        lines = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, cwd=cwd).communicate()[0]
        lines = lines.split('\n')

    return list(filter(lambda l: l != '', lines))

# Takes in a directory, and makes a copy of it by copying the directory
# structure, but hardlinking the non-directory contents instead of copying them.
# TODO: use symlinks (cp -as?) instead? (might be faster?)
def linkclone_dir(srcDir, destDir):
    run_cmd('cp -al %s %s' % (srcDir, destDir))

# print with no newline
def print_nobr(msg):
    sys.stdout.write(msg)
    sys.stdout.flush()
