#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
update all git repositories from current folder
supports bare git and git-svn repositories
"""
import os
from gevent.pool import Pool
from gevent.subprocess import Popen, PIPE, STDOUT

worker_number = 20
pool = Pool(worker_number)
git_signature = ".git"


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

    if bare:
        cmd = ["git", "fetch"]
        return cmd

    directories = list_directories(os.path.join(path, git_signature))

    if "svn" in directories:
        cmd = ["git", "svn", "rebase"]
    else:
        cmd = ["git", "pull"]

    return cmd


def is_bare(path):
    p = os.path.basename(path)
    return (len(p) > 4) & (p.endswith(git_signature))
    pass


def update_repositories(repository_list):
    """
    Update repository list
    """

    repo_count = 0

    for repository in repository_list:
        cmd, path = repository
        # print repo_count,"]==> ", repo, "cmd=> ", cmd
        pool.spawn(update_repository, path, cmd, repo_count)
        repo_count += 1


def update_repository(path, cmd, count):
    os.chdir(path)
    print count, "]", "updating:", path
    p = Popen(' '.join(cmd), cwd=path, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    for line in p.stdout:
        if line != "Already up-to-date.\n":
            print count, "]", path, ":", line,


def find_repositories(path):
    """
    Find list of potential repositories in current and child folders
    """

    repository_list = []
    os.chdir(path)
    directories = list_directories(path)

    # is this a standard git/git-svn repo?
    if git_signature in directories:
        cmd = get_command(False, path)
        repository_list.append((cmd, path))
        return repository_list

    # find git bare repositories
    for d in directories:
        p = os.path.join(path, d)
        bare = is_bare(d)
        if bare:
            cmd = get_command(bare, p)
            repository_list.append((cmd, p))
        else:
            repository_list.extend(find_repositories(p))

    return repository_list

if __name__ == "__main__":
    cwd = os.getcwd()
    repositories = sorted(find_repositories(cwd), key=lambda tup: tup[1])
    update_repositories(repositories)
    os.chdir(cwd)
    pool.join()
    print "Processed ", len(repositories), " repositories"
