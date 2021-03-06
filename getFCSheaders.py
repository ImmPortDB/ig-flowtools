#!/usr/bin/env python
######################################################################
#                  Copyright (c) 2016 Northrop Grumman.
#                          All rights reserved.
######################################################################
from __future__ import print_function
import subprocess
import os
import sys

from argparse import ArgumentParser


def get_fcs_marker_list(marker_file):
    with open(marker_file, "r") as mrkrs:
        mrkrs.readline()
        channels = []
        markers = []
        for lines in mrkrs:
            stuff = lines.strip().split("\t")
            channels.append(stuff[1].strip("\""))
            markers.append(stuff[2].strip("\""))
    fcs_markers = [
        "\t".join(channels),
        "\t".join(markers)
    ]
    return(fcs_markers)


def print_fcs_headers(files, filenames, outfile):
    headers = {}
    tool = "getFCSheader.R"
    for eachfile in files:
        tmp_output = "tmp_fcs_headers.txt"
        try:
            subprocess.call(" ".join([tool, eachfile, tmp_output]), env=os.environ.copy(), shell=True)
        except:
            sys.stderr.write("Could not run getFCSheader.R\n")
            sys.exit(2)
        headers[eachfile] = get_fcs_marker_list(tmp_output)

    h = len(headers[files[0]][0].strip().split("\t")) + 1
    idx = [str(x) for x in range(1, h)]

    with open(outfile, "w") as outf:
        outf.write("Filename\tIndex\t")
        outf.write("\t".join(idx) + "\n")
        for i, flc in enumerate(files):
            outf.write("\t".join([filenames[i], "channels", headers[flc][0]]) + "\n")
        for j, flm in enumerate(files):
            outf.write("\t".join([filenames[j], "markers", headers[flm][1]]) + "\n")
    return


if __name__ == "__main__":
    parser = ArgumentParser(
             prog="GetFCSHeaders",
             description="Gets the headers of all files in given set.")

    parser.add_argument(
            '-i',
            dest="input_files",
            required=True,
            action='append',
            help="File location for the text files.")

    parser.add_argument(
            '-n',
            dest="file_names",
            required=True,
            action='append',
            help="File names.")

    parser.add_argument(
            '-o',
            dest="output_file",
            required=True,
            help="Name of the output file.")

    args = parser.parse_args()
    input_files = [f for f in args.input_files]
    file_names = [fn for fn in args.file_names]
    print_fcs_headers(input_files, file_names, args.output_file)
