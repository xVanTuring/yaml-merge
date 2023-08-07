#! /usr/bin/python

from yaml import load, dump

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

import sys
import os
print(sys.argv)
if len(sys.argv) != 3:
    print("Yaml Merge:")
    print("main.py", "source-file","append-filed")
    print("e.g.", "main.py","appendee.yaml","appender.yaml")
    exit()


appendee_path = sys.argv[1]
appender_path = sys.argv[2]

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