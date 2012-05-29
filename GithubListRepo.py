"""
    Given github user name, list all public repositories
"""

__author__ = 'Huang Yung-Tai'

import getopt
import sys
import json
import urllib2

GITHUB_API_V3="https://api.github.com"
GITHUB_USER_FMT=[GITHUB_API_V3 + "/users/%s/repos",GITHUB_API_V3 + "/users/%s/repos?type=all"]

def list_repos(username):
    """
    list repositories given a github user
    @param username
    @return set of urls
    """
    urllist=list()
    for FMT in GITHUB_USER_FMT:
        url = FMT % username
        try:

            usock = urllib2.urlopen(url)
        except (IOError,OSError):
            print "Something went wrong when trying to find %s repos" % str(username)
            sys.exit()

        response = json.load(usock)
        usock.close()
        urllist.extend([gitrepo['clone_url'] for gitrepo in response])

    urlset = set(urllist)
    return urlset

def main(argv):
    """
    main function loop for GithubListProjects
    """
    try:
        if not len(argv): raise getopt.GetoptError("No options given")
        opts, args = getopt.getopt(argv, "hu:", ["help","user="])
    except getopt.GetoptError:
        usage()
        sys.exit()

    if not len(opts): usage()
    for opt, arg in opts:
        if opt in ("-h","--help"):
            usage()
            sys.exit()
        elif opt in ("-u","--user"):
            urls = list_repos(arg)
            print "\n".join(u for u in sorted(urls))

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