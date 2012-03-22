from xml.etree.cElementTree import ElementTree
import sys
from optparse import OptionParser

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

for iteration in iterations:
    pas = iteration.findall('playahead')
    # each of playahead is one of the different moves we're simming/comparing
    for pa in pas:
        plies = pa.findall('ply')
        for ply in plies:
            # even plies (starting with 0) are us, odd plies are opponent
            index = ply.attrib['index']
            move = ply.find('move')
            action = move.attrib['action']
            tiles = move.attrib['tiles']
            position = move.attrib['position']
            score = move.attrib['score']

            print index, action, tiles, position, score




