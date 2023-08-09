#! /usr/bin/python
# coding=utf-8
from yaml import load, dump

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

import os
import argparse

parser = argparse.ArgumentParser(
    prog="YamlMerge",
    description="Merge two yaml file and output to stdout",
    epilog="xVanTuring with ♥",
)
# parser.add_argument(
#     "-r", "--recursive", help="merge recursive", type=bool, default=True
# )
parser.add_argument("source_file")
parser.add_argument("append_file")
args = parser.parse_args()


appendee_path = args.source_file
appender_path = args.append_file

if not os.path.exists(appendee_path) or not os.path.exists(appender_path):
    print("Can't find input files")
    exit(1)


def merge_dict(appendee_dict: dict, appender_dict: dict):
    for key in appender_dict.keys():
        if key in appendee_dict:
            field_type = type(appendee_dict[key])
            check_type_same(appendee_dict[key], appender_dict[key], key=key)
            if field_type is dict:
                merge_dict(appendee_dict[key], appender_dict[key])
            elif field_type is list:
                merge_list(appendee_dict[key], appender_dict[key])
            else:
                appendee_dict[key] = appender_dict[key]
        else:
            appendee_dict[key] = appender_dict[key]


def merge_list(appendee_list: list, appender_list: list):
    appendee_list.extend(appender_list)


def check_type_same(a, b, key="<root>"):
    if type(a) is not type(b):
        print(f"Appendee and Appender has different merge type at {key}")
        exit(1)


def check_type_mergeable(a, b):
    a_type = type(a)
    b_type = type(b)
    if (a_type is not list and a_type is not dict) or (
        b_type is not list and b_type is not dict
    ):
        print("we current ly only support merge list and dict")
        exit(1)


def merge():
    appendee_content = ""
    appender_content = ""
    with open(appendee_path, encoding="UTF-8") as f:
        appendee_content = f.read()

    with open(appender_path, encoding="UTF-8") as f:
        appender_content = f.read()

    appendee_yaml: dict or list or str = load(appendee_content, Loader=Loader)
    appender_yaml: dict or list or str = load(appender_content, Loader=Loader)
    check_type_same(appendee_yaml, appender_yaml)
    check_type_mergeable(appendee_yaml, appender_yaml)
    if type(appendee_yaml) is list:
        merge_list(appendee_yaml, appender_yaml)
    else:
        merge_dict(appendee_yaml, appender_yaml)
    data = dump(appendee_yaml, Dumper=Dumper, encoding="utf-8", sort_keys=False)
    print(data.decode("unicode_escape"))
merge()
