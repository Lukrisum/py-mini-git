import argparse
import collections
import configparser
import hashlib
from math import ceil
import os
import re
import sys
import zlib

import utils.repo_os as repo_os

parser = argparse.ArgumentParser(description='PY-MINI-GIT')
subparser = parser.add_subparsers(dest='command')
subparser.required = True


def main(argv=sys.argv[1:]):
    args = parser.parse_args(argv)

    if args.command == "init":
        cmd_init(args)

    # if args.command == "add":
    #     cmd_add(args)
    # elif args.command == "commit":
    #     cmd_commit(args)
    # elif args.command == "init":
    #     cmd_init(args)
    # elif args.command == "log":
    #     cmd_log(args)


class GitRepository(object):
    """A git repository"""

    # 工作区路径
    worktree = None
    # .git 路径
    gitdir = None
    conf = None

    # force 允许强制创建（即日常将空目录初始化为 git 仓库）
    def __init__(self, path, force=False):
        self.worktree = path
        self.gitdir = os.path.join(path, '.git')

        if not (force or os.path.isdir(self.gitdir)):
            raise Exception("Not a Git repository %s" % path)

        # Read configuration file in .git/config
        self.conf = configparser.ConfigParser()
        cf = repo_os.repo_path(self, "config")

        if cf and os.path.isfile(cf):
            self.conf.read([cf])
        elif not force:
            raise Exception("Configuration file missing")

        # 仓库版本
        if not force:
            vers = int(self.conf.get("core", "repositoryformatversion"))
            if vers != 0:
                raise Exception(
                    "Unsupported repositoryformatversion %s" % vers)


def repo_create(path):
    """Create a new repository at path."""
    repo = GitRepository(path, force=True)

    # First, we make sure the path either doesn't exist or is an
    # empty dir.

    if os.path.exists(repo.worktree):
        if not os.path.isdir(repo.worktree):
            raise Exception("%s is not a directory!" % path)
        if os.listdir(repo.worktree):
            raise Exception("%s is not empty!" % path)

    else:
        os.makedirs(repo.worktree)

    assert (repo_os.repo_dir(repo, "branches", mkdir=True))
    assert (repo_os.repo_dir(repo, "object", mkdir=True))
    assert (repo_os.repo_dir(repo, "refs", "tags", mkdir=True))
    assert (repo_os.repo_dir(repo, "refs", "heads", mkdir=True))

    # .git/description
    with open(repo_os.repo_file(repo, "HEAD"), "w") as f:
        f.write(
            "Unnamed repository; edit this file 'description' to name the repository.\n")

    # .git/HEAD
    with open(repo_os.repo_file(repo, "HEAD"), "w") as f:
        f.write("ref: refs/heads/master\n")

    with open(repo_os.repo_file(repo, "config"), "w") as f:
        config = repo_default_config()
        config.write(f)

    return repo


def repo_default_config():
    ret = configparser.ConfigParser()
    ret.add_section("core")
    # 仓库版本
    ret.set("core", "repositoryformatversion", "0")
    # diff 是否考虑文件权限
    ret.set("core", "filemode", "false")
    # 裸仓库*
    ret.set("core", "bare", "false")

    return ret


# 挂载 init 命令
init_parser = subparser.add_parser(
    'init', help="Initialize a new, empty repository.")
init_parser.add_argument("path", metavar="directory", nargs="?",
                         default=".", help="Where to create the repository.")


def cmd_init(args):
    # print(args)
    repo_create(args.path)
