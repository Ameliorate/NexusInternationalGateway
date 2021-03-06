#!/usr/bin/python3

import toml
import os
from sys import stderr
from collections import deque
from copy import deepcopy
import json

datadir = r'./data'

data = {}

def processFile(path, name):
    print(f"Processing file {path}", file=stderr)
    name = name.removesuffix('.toml')
    myData = toml.load(path)
    if 'links' not in myData:
        myData['links'] = []
    if 'BadLinks' not in myData:
        myData['BadLinks'] = {}
    data[name] = myData

for subdir, dirs, files in os.walk(datadir):
    for filename in files:
        filepath = subdir + os.sep + filename

        if filepath.endswith('.toml'):
            processFile(filepath, filename)

has_error = False

coordinates = {}

for destination in data.keys():
    dest_data = data[destination]

    # has an x and z
    if 'x' not in dest_data:
        print(f"{destination} does not have an x coordinate")
        has_error = True
    if 'z' not in dest_data:
        print(f"{destination} does not have a z coordinate")
        has_error = True

    # doesn't share an x and z with any other station
    if 'x' in dest_data and 'z' in dest_data:
        coord = (dest_data['x'], dest_data['z'])
        if coord in coordinates:
            shares = coordinates[coord]
            print(f"{destination} shares coordinate with {shares}")
            has_error = True

        coordinates[coord] = destination

    # lists what it is linked to
    if 'links' not in dest_data:
        print(f"{destination} does not list what stations it is connected to")
        has_error = True

    # check over all links
    for link in dest_data['links']:

        # make sure link exists
        if link not in data:
            print(f"{destination} contains unknown link {link}")
            has_error = True
            continue

        link_data = data[link]

        # if a link is listed, make sure the link lists the destination too
        if destination not in link_data.get('links'):
            print(f"{destination} lists link {link}, however {link} does not list link {destination}")
            has_error = True

if has_error:
    exit(1)
