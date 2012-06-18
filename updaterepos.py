#!/usr/bin/env python
"""
update all git repositories from current folder
supports git and git-svn repositories
"""
import os
import subprocess

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
    return ["git", "pull"]


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
        subprocess.call(cmd)
    else:
        for d in directories:
            p = os.path.join(path, d)
            find_git_repos(p)
    os.chdir("..")

if __name__ == "__main__":
    cwd = os.getcwd()
    find_git_repos(cwd)
