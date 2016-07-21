#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Apkstats: simple script to visualize APK size from file types
# Code by Laurent Mallet aka ellis2323 in 2014

# Licence
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions and limitations under the License.

import zipfile
import os
import argparse

sort_by = [	{ 'grp': 'audio', 'ext': [ 'wav', 'mp3', 'ogg'] },
			{ 'grp': 'gfx', 'ext': [ 'png', 'webp'] },
			{ 'grp': 'gfx_compressed', 'ext': [ 'ktx', 'ktx2', 'atc', 'dxt', 'pvr' ] },
			{ 'grp': 'c-libs', 'ext': [ 'so' ] },
			{ 'grp': 'java-libs', 'ext': [ 'dex' ] },
			{ 'grp': 'conf', 'ext': [ 'jspine', 'json', ] },
			{ 'grp': 'i18n', 'ext': [ 'mo', 'po' ] },
			{ 'grp': 'wear', 'ext': [ 'apk', ] },
			{ 'grp': 'gwd', 'ext': [ 'gwd', 'GWD', ] },
			{ 'grp': 'other', 'ext': [] },
		]

def completeGrp(groups):
	for grp in groups:
		grp['size'] = 0
		grp['csize'] = 0
		grp['objs'] = []

def findGrpByExt(groups, ext):
	#import pdb
	#pdb.set_trace()
	other = None
	for grp in groups:
		if grp['grp'] == 'other':
			other = grp
		for e in grp['ext']:
			if e == ext[1:]:
				return grp
	return grp

def APKAnalyze(filezipped):
	completeGrp(sort_by)
	zip = zipfile.ZipFile(filezipped)
	for z in zip.infolist():
		filename, ext = os.path.splitext(z.filename)
		grp = findGrpByExt(sort_by, ext)
		grp['size'] += z.file_size
		grp['csize'] += z.compress_size
		grp['objs'].append(z)
	for g in sort_by:
		print "Group: %20s size:%9d compress size:%9d" % (g['grp'], g['size'], g['csize'])


if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Give stats of an APK file')
    parser.add_argument('file', nargs=1, help='APK file')
    args = parser.parse_args()
    APKAnalyze(args.file[0])
