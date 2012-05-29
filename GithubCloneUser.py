#!/usr/bin/env python

"""
    Given github user name, clone all public repositories
"""

__author__ = 'Huang Yung-Tai'

import GithubListRepo
import subprocess
import sys
import getopt

GIT_CMD = "git"
CLONE_CMD = "clone"


def clone_all(urls):
    """
    Clone all git repos given url list
    """

    for url in urls:
        subprocess.call([GIT_CMD, CLONE_CMD, url])

    pass


def main(argv):
    """
    main function loop for GitCloneUser
    """
    try:
        if not len(argv):
            raise getopt.GetoptError("No options given")
        opts, args = getopt.getopt(argv, "hu:", ["help", "user="])
    except getopt.GetoptError:
        usage()
        sys.exit()

    if not len(opts):
        usage()
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-u", "--user"):
            urls = GithubListRepo.list_repos(arg)
            clone_all(urls)

        else:
            usage()
            sys.exit()


def usage():
    print """
    -h --help print this usage information
    -u --user="git hub user name"
    """


if __name__ == "__main__":
    main(sys.argv[1:])
