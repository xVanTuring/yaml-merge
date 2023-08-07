#! /usr/bin/python

from yaml import load, dump

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

import sys
import os
import argparse
parser = argparse.ArgumentParser(
    prog='YamlMerge',
    description='Merge two yaml file and output to stdout',
    epilog='xVanTuring with ♥'
)
parser.add_argument('-b','--behaviour',help='behaviour when key exists in both yaml.[todo]',choices=['o','m'])
parser.add_argument('source_file')
parser.add_argument('append_file')
args = parser.parse_args()



appendee_path = args.source_file
appender_path = args.append_file

if not os.path.exists(appendee_path) or not os.path.exists(appender_path):
    print("Can't find input files")
    exit(1)

appendee_content = ""
appender_content = ""
with open(appendee_path) as f:
    appendee_content = f.read()

with open(appender_path) as f:
    appender_content = f.read()

appendee_yaml: dict = load(appendee_content, Loader=Loader)
appender_yaml: dict = load(appender_content, Loader=Loader)
appendee_yaml.update(appender_yaml)
print(dump(appendee_yaml,Dumper=Dumper))