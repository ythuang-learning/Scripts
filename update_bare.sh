#!/bin/bash

find -maxdepth 3 -regex .*\.git$ | grep  -v \/\.git$ | xargs -n 1 -I {} sh -c '(echo working on {}; cd {};git fetch)'

find -maxdepth 3 -regex .*\.git$ | grep \/\.git$ | xargs -n 1 -I {} sh -c '(echo working on `dirname {}`;cd `dirname {}`; git svn rebase )'
