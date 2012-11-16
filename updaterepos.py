#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
update all git repositories from current folder
supports bare git and git-svn repositories
"""
import os
from gevent.pool import Pool
from gevent.subprocess import Popen, PIPE, STDOUT

worker_number = 40
pool = Pool(worker_number)
git_sign = ".git"


def list_directories(path):
    """
    list folders in current path
    """
    dir_list = os.listdir(path)
    directories = [f for f in dir_list if os.path.isdir(os.path.join(path, f))]
    return directories


def get_command(bare, path):
    """
    get command based on folder type
    returns either command for bare git, standard git or git-svn
    """

    if(bare):
        cmd = ["git", "fetch"]
        return cmd

    directories = list_directories(os.path.join(path, git_sign))

    if "svn" in directories:
        cmd = ["git", "svn", "rebase"]
    else:
        cmd = ["git", "pull"]

    return cmd


def is_bare(path):
    p = os.path.basename(path)
    return (len(p) > 4) & (p.endswith(git_sign))
    pass


def update_repos(repo_list):
    """
    Update repository list
    """

    repo_count = 0

    for repo in repo_list:
        bare, path = repo
        cmd = get_command(bare, path)
        # print repo_count,"]==> ", repo, "cmd=> ", cmd
        pool.spawn(update_repo, repo, cmd, repo_count)
        repo_count += 1


def update_repo(repo, cmd, count):
    bare, path = repo

    os.chdir(path)
    print count, "]", "updating:", path
    p = Popen(' '.join(cmd), cwd=path, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    for line in p.stdout:
        if line != "Already up-to-date.\n":
            print count, "]", path, ":", line,


def find_repos(path):
    """
    Find list of potential repositories in current and child folders
    """

    repolist = []
    global repo_count
    os.chdir(path)
    directories = list_directories(path)

    # is this a standard git/git-svn repo?
    if git_sign in directories:
        repolist.append((False, path))
        return repolist

    # find git bare repos
    for d in directories:
        p = os.path.join(path, d)
        bare = is_bare(d)
        if bare:
            repolist.append((bare, p))
        else:
            repolist.extend(find_repos(p))

    return repolist

if __name__ == "__main__":
    cwd = os.getcwd()
    repos = find_repos(cwd)
    update_repos(repos)
    os.chdir(cwd)

    # pool.join()
    print "Processed ", len(repos), " repositories"
