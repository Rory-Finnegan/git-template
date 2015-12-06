# git-template
My git template folder

## Dependencies
* pip
* virtualenv

## Install
```shell
> git clone https://github.com/Rory-Finnegan/git-template
> cd git-template
> ./INSTALL
```
The INSTALL script will:

1. build a virtualenv in the root `git-template` directory called `venv`
1. install the requirements.txt into that virtualenv
1. write the full path of the `venv/bin/python` (to be exported) to `template/hooks/settings.sh`
1. sets `init.template` and `clone.template` to the `template` folder.

## Usage
The template folder provided will only be used for new git repos.

#### Local user pre-commit hook
This hook will try and set the local user.name and user.email (if not already set) using the repo remotes
and the url patterns per multi-user in your global gitconfig.

Setting a multi-user in your `~/.gitconfig`:
```
[multi-user "github-personal"]
    name = Rory-Finnegan
    email = rory.finnegan@gmail.com
    url = (https://|git@)github.com(/|:)Rory-Finnegan/*
```
The above entry will allow for automatic setting of the local user.name and user.email to the values provided for all git remote urls that match the regex provided.

NOTE: you can also create that entry with:
```
> git config --global --add multi-user.github-personal.name Rory-Finnegan
> git config --global --add multi-user.github-personal.email rory.finnegan@gmail.com
> git config --global --add multi-user.github-personal.url="(https://|git@)github.com(/|:)Rory-Finnegan/*"
```
