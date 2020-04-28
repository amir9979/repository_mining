#!/usr/bin/env python

import json
import sys
from argparse import ArgumentParser, FileType
from itertools import repeat
from xml.etree import ElementTree

# Parse arguments
parser = ArgumentParser(description='Convert and print checkstyle from stdin to \
    json file with context.')
parser.add_argument('source', type=FileType('r'), help='Source checkstyle XML file path')
parser.add_argument('dest', type=FileType('w'), help='Destination JSON file path')
parser.add_argument(
    '-B, --before',
    dest='before',
    type=int,
    default=3,
    help='Amount of lines before used for file context fetch'
)
parser.add_argument(
    '-A, --after',
    dest='after',
    type=int,
    default=3,
    help='Amount of lines after used for file context fetch'
)
args = parser.parse_args()

##
# Get n-th line context from file
##
def get_context(filepath, n, before=3, after=3):
    lines = {}

    skip = max(0, n - before)
    before = n - skip

    with open(filepath, "r") as handle:
        # Skip `n - before` lines
        for _ in repeat(None, skip):
            handle.readline()

        # Read the context
        for i in range(1, before + after + 2):
            lines[skip + i] = (handle.readline())

    return lines

# Gathered files data
files = {}

# Iterate over all files
for fileElement in ElementTree.parse(args.source).getroot():
    filepath = fileElement.attrib['name']

    # Gathered items data
    items = []

    # Iterate over all errors
    for errorElement in fileElement:
        line = int(errorElement.attrib['line'])
        if "max allowed" not in errorElement.attrib['message']:
                continue
        items.append({
            #'severity': errorElement.attrib['severity'],
            #'source': errorElement.attrib['source'].split(".")[-1].replace("Check", ""),
            'line': line,
            #'column': errorElement.attrib['column'],
            'message': errorElement.attrib['message'],
            'key': "_".join(errorElement.attrib['message'].replace("lines", "").replace(",","").split('(')[0].split()[:-2]),
            'value': int(errorElement.attrib['message'].replace("lines", "").replace(",","").split('(')[0].split()[-1].strip()),
            'file': filepath,
             #   before=args.before, after=args.after),
        })

    files[filepath] = items

# Print gathered files in json format
args.dest.write(
    json.dumps(files, indent=4, sort_keys=False)
)
