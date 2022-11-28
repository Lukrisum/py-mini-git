# 用于解析命令行参数
import argparse

# 提供特殊的的容器类型
import collections

# Git 使用的配置文件格式基本上是微软的 INI 格式，该模块用于读写这些文件
import configparser

# Git 相当广泛地使用 SHA-1 函数
import hashlib

# 一个数学函数
from math import ceil

# 提供文件系统抽象例程
import os

# 处理正则表达式
import re

# 我们还需要 sys 来访问实际的命令行参数（在 sys.argv 中）
import sys

# Git 使用 zlib 压缩一切。 Python 也含有该模块
import zlib

# 引入部分完成，开始正文

# argparse 使用见官方文档
argparser = argparse.ArgumentParser(description="PY-MINI-GIT")
argparser.add_argument("integers",type=str,help="传入的数字")
args = argparser.parse_args()

print(args.integers)