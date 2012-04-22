from xml.etree.cElementTree import ElementTree
import sys
from optparse import OptionParser
import json
usage = "usage: %prog logfile"

parser = OptionParser(usage=usage)
(options, args) = parser.parse_args()
if len(args) != 1:
    parser.error('You must provide a log filename')

filename = args[0]

tree = ElementTree()
print 'before parse'
tree.parse(filename)
print 'after parse'
iterations = tree.findall('iteration')

plyData = {}

def getKey(action, move):
    key = action
    if action == "pass":
        pass
    elif action == "exchange":
        key += ':' + move.attrib['tiles']
    elif action == "place":
        key += ':' + move.attrib['tiles'] + ':' + move.attrib['position'] + ':' + move.attrib['score']
    return key

for iteration in iterations:
    pas = iteration.findall('playahead')
    # each of playahead is one of the different moves we're simming/comparing
    for pa in pas:
        plies = pa.findall('ply')
        zeroply = plies[0]
        assert(plies[0].attrib['index']=="0")
        move = plies[0].find('move')
        action = move.attrib['action']
        key = getKey(action, move)

        thisData = []

        for ply in plies[1:]:
            # even plies (starting with 0) are us, odd plies are opponent
            index = ply.attrib['index']
            move = ply.find('move')
            action = move.attrib['action']
            inKey = getKey(action, move)

            rack = ply.find('rack')
            pc = ply.find('pc')
            if pc is not None:
                leaveValue = pc.attrib['value']
            else:
                leaveValue = None
            tiles = rack.attrib['tiles']
            thisData.append( {index: tiles + ':' + inKey + (':' + leaveValue if leaveValue else '')} )

        if key not in plyData:
            plyData[key] = [thisData]
        else:
            plyData[key].append(thisData)

print json.dumps(plyData, indent=2)


