#!/usr/bin/env python3

from util import *

# Simple template/macro library.
# Anything between ! signs, e.g. !KEYWORD!, gets replaced with simple
# substitution.
#
# Anything between double !! signs, e.g. !!KEYWORD!!, gets expanded with the
# text generator callback function supplied for KEYWORD.

DELIM_CHAR = '!'


def fillTemplate(srcFileName, destFileName, subsMap, callbackMap=None):
    destChars = []

    with open(srcFileName, 'r') as src:
        data = src.read()
        i = 0
        while (i < len(data)):
            char = data[i]
            if char == DELIM_CHAR:
                if data[i+1] == DELIM_CHAR:     # double delim; do callback expansion
                    if callbackMap == None:
                        die("ERROR: requested callback expansion, but no callbacks supplied.")

                    endDelimIdx = data.index(DELIM_CHAR, i+2)
                    callbackName = data[i+2:endDelimIdx]
                    destChars.append(callbackMap[callbackName]())

                    i += 2 + len(callbackName) + 2

                else:                          # single delim; do simple substitution
                    if subsMap == None:
                        die("ERROR: requested variable expansion, but no variables supplied.")

                    endDelimIdx = data.index(DELIM_CHAR, i+1)
                    varName = data[i+1:endDelimIdx]
                    destChars.append(subsMap[varName])

                    i += 1 + len(varName) + 1

            else:       # just a regular character
                destChars.append(char)

                i += 1

    with open(destFileName, 'w') as dest:
        dest.write(''.join(destChars))
