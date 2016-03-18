#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Create a Android.mk with a template Android.mk.template
# insert at the begin of the file lines as:
# $SRC = { "path": "cpufeatures", "ext": ".c", "exceptFiles": [],  "exceptDirs": [] }
# 
# it will generate a Android.mk that compiles all c files from "cpufeatures" directory


# Code by Laurent Mallet aka ellis2323 in 2014

# Licence
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions and limitations under the License.

import os
import sys
import json
import argparse

def listFilesByExt(path, ext, exceptFiles, exceptDirs):
    """Path """
    res = []
    for r, dirs, files in os.walk(path):
        # do not walk dot files
        files = [f for f in files if not f[0] == '.']
        dirs[:] = [d for d in dirs if not d[0] == '.']
        # do not walk into exceptDirs
        dirs[:] = [d for d in dirs if d not in exceptDirs]
        for f in files:
            if f.endswith(ext):
                if f not in exceptFiles:
                    path = r + '/' + f
                    if path.startswith('./'):
                        path = path[2:]
                    res.append(path)
    return res

def outputSourcesFiles(content, value):
    """replace ${SRC_FILES} """
    return content.replace("""${SRC_FILES}""", value)

def readTemplate(filepath):
    """read Template"""
    f = open(filepath, "r")
    content = ""
    files = []
    lines = f.readlines()
    count = 0
    for l in lines:
        if l.startswith('$SRC'):
            jtxt = l.split('=', 1)[1]
            d = json.loads(jtxt)
            if d.has_key("path") and d.has_key("ext") and d.has_key("exceptFiles") and d.has_key("exceptDirs"):
                files += (listFilesByExt(d["path"], d["ext"], d["exceptFiles"], d["exceptDirs"]))
            else:
                print "invalid $SRC at line " + str(count)
                sys.exit(-1)
        else:
            content += l
        count += 1
    value = ""
    count = 0
    qty = len(files)
    for f in files:
        if count != 0:
            value += "    "
        value += f 
        if count != qty-1:
            value += " \\\n"
        count += 1
    return outputSourcesFiles(content, value)

def checkTemplate(filepath):
    """Check if template is present"""
    if not os.path.exists(filepath):
        print "No Android.mk.template"
        sys.exit(-1)

if __name__=='__main__':
    fp = 'Android.mk.template'
    checkTemplate(fp)
    fo = open('Android.mk', 'r')
    oldValue = fo.read()
    fo.close()
    newValue = readTemplate(fp)
    if oldValue !=  newValue:
        fo = open('Android.mk', 'w')
        fo.write(newValue)
        print "New Android.mk written"
    ##print listFilesByExt('.', '.cpp', [ 'CompositeTestReporter.cpp' ], ['tests', 'Win32'])

