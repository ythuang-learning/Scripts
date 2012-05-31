#!/usr/bin/env python

import os
import subprocess

def getdirectories(path): 
  flist = os.listdir(path)
  directories = [ f for f in flist if os.path.isdir(os.path.join(path,f)) ]
  return directories

def findgit(path):
  os.chdir(path)
  print "Looking at: " + path
  dlist = getdirectories(path)
  if ".git" in dlist:
    subprocess.call(["git", "pull"])
  else:
    for d in dlist:
      p = os.path.join(path,d)
      findgit(p)
  os.chdir("..")

cwd = os.getcwd()
findgit(cwd)
