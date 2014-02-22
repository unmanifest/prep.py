#!/usr/bin/env python
from __future__ import print_function
import argparse
import re
import json
import sys
from StringIO import StringIO

parser = argparse.ArgumentParser("A generic pre-preprocessor")
parser.add_argument("-v", "--verbose", help="Increase verbosity",
                    action="count", default=0)
parser.add_argument("-t", "--template", help="Template file name",
                    required=True)
parser.add_argument("-s", "--spec", help="Specification file in JSON format",
                    nargs='+')
parser.add_argument("-p", "--python", help="Intermediate python file")
parser.add_argument("-o", "--output", help="Output file name",
                    type=argparse.FileType('wb'), default=sys.stdout)
args = parser.parse_args()

def process_inputs():
    spec = ""
    if args.spec:
        spec = process_specs()
    code = parse_template()
    if (args.python):
        with open(args.python, "wb") as file:
            file.write(code)
    buffer = StringIO()
    sys.stdout = buffer          # change stdout to capture exec output
    exec(code)
    sys.stdout = sys.__stdout__  # restore default stdout
    args.output.write(buffer.getvalue())
    buffer.close()

def process_specs():
    for f in args.spec:
        with open(f, "r") as file:
            spec = json.loads(file.read()) # @todo: no merge yet
    return spec

def parse_template():
    res = ""
    indent = "    "
    level = 0
    pat = re.compile(r'^//;|^#%')
    i_pat = re.compile(r'^ *#{3} *level(?P<suffix>[-+]{2}) *$');
    begin_here_doc = 'print("""'
    end_here_doc = '""" % locals(), end="")\n'
    state = 0 # 0 = python; 1 = template txt
    file_t = open(args.template, "r")
    for line in file_t:
        if (pat.match(line)):
            line = pat.sub('', line) # string replace
            m = i_pat.match(line)
            if m is not None:
                if m.group('suffix') == '++':
                    level += 1
                else:
                    level -= 1
            if state == 1:
                line = end_here_doc + line # end here doc
            state = 0
        else:
            if state == 0:
                line = level * indent + begin_here_doc + line
                state = 1
        res += line
    if state == 1: # one final time
        res += end_here_doc
    file_t.close()
    return(res)

if __name__ == "__main__":
    process_inputs()
