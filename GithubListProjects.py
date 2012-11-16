#!/usr/bin/env python

"""
    Given github user url, list all public repositories
"""
import getopt

__author__ = 'Huang Yung-Tai'


import sys
import urllib2
from bs4 import BeautifulSoup


def extract_urls(doc):
    """
    Extract list of url given html document
    """
    soup = BeautifulSoup(doc)
    li = soup.findAll('li', "public source")
    li.extend(soup.findAll('li', "simple public source"))
    li.extend(soup.findAll('li', "public fork"))
    li.extend(soup.findAll('li', "simple public fork"))

    pathlist = list()

    for i in range(len(li)):
        try:
            pathlist.append(li[i].h3.a['href'])
        except AttributeError:
            pass

    return ["https://github.com/%s.git" % path for path in pathlist]


def list_repos(username):
    """
    list repositories given a github user url
    """
    GITHUB_USER_FMT = "https://github.com/%s"
    try:
        usock = urllib2.urlopen(GITHUB_USER_FMT % username)
    except (IOError, OSError):
        print "Something went wrong when opening %s" % str(username)
        sys.exit()

    doc = usock.read()
    usock.close()
    gitrepos = extract_urls(doc)
    print "\n".join(gitrepo for gitrepo in gitrepos)


def main(argv):
    """
    main function loop for GithubListProjects
    """
    try:
        if not len(argv):
            raise getopt.GetoptError("No options given")
        opts, args = getopt.getopt(argv, "hu:", ["help", "url="])
    except getopt.GetoptError:
        usage()
        sys.exit()
    if not len(opts):
        usage()
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
        elif opt in ("-u", "--user"):
            list_repos(arg)
        else:
            usage()
            sys.exit()


def usage():
    print """
    -h --help print this usage information
    -u --url="url of github user"
    """


if __name__ == "__main__":
    main(sys.argv[1:])
