#!/bin/sh

# reference: https://help.github.com/articles/changing-author-info

git filter-branch --env-filter '

an="$GIT_AUTHOR_NAME"
am="$GIT_AUTHOR_EMAIL"
cn="$GIT_COMMITTER_NAME"
cm="$GIT_COMMITTER_EMAIL"

if [ "$GIT_COMMITTER_EMAIL" = "chris_yt_huang@wistron.com" ]
then
    cn="Chris YT Huang"
    cm="ythuang@gmail.com"
fi
if [ "$GIT_AUTHOR_EMAIL" = "chris_yt_huang@wistron.com" ]
then
    an="Chris YT Huang"
    am="ythuang@gmail.com"
fi

export GIT_AUTHOR_NAME="$an"
export GIT_AUTHOR_EMAIL="$am"
export GIT_COMMITTER_NAME="$cn"
export GIT_COMMITTER_EMAIL="$cm"
'


