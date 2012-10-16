#!/usr/bin/env python
"""
update all git repositories from current folder
supports git and git-svn repositories
"""
import os
import subprocess
import gevent
from gevent.pool import Pool

pool = Pool(20)

def list_directories(path):
    """
    list folders in current path
    """
    dir_list = os.listdir(path)
    directories = [f for f in dir_list if os.path.isdir(os.path.join(path, f))]
    return directories


def get_command():
    """
    get command based on folder type
    returns either command for git or git-svn
    """
    os.chdir(".git")
    directories = list_directories(os.getcwd())
    cmd = ["git", "pull"]
    if "svn" in directories:
        cmd = ["git","svn", "rebase"]
    os.chdir("..")
    return cmd

def update_repo(path, cmd):
    print "updating: ", path
    p = subprocess.Popen(' '.join(cmd), cwd=path, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
    output = p.stdout.read()
    if output != "Already up-to-date.\n":
        print output


def find_git_repos(path):
    """
    check whether the current folder is a git or git-svn repository
    update the git or git-svn repository if found
    """
    os.chdir(path)
    print "Looking at: " + path 
    directories = list_directories(path)
    if ".git" in directories:
        cmd = get_command()
        pool.spawn(update_repo,path, cmd)

    else:
        for d in directories:
            p = os.path.join(path, d)
            find_git_repos(p)
    os.chdir("..")

if __name__ == "__main__":
    cwd = os.getcwd()
    find_git_repos(cwd)
    pool.join()

