'''Show similarities in a text file, graphically'''

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.pylab import plot, show
import sys
import optparse


def get_line_tokens(line_producer, start_token=None, ignore_these = ('\n', '')):
    lineiter = iter(line_producer)
    lineno = 0 
    while True:
        line = lineiter.next()
        if line not in ignore_these:
            yield lineno, line
        lineno += 1

def show_similiarities(filenames, get_tokens = get_line_tokens):
    x_positions = []
    y_positions = []
    lines_x = []
    lines_y = []
    possible_line_continuations = {}
    filename = filenames[0]
    f = open(filename, 'r')
    lines = list(get_tokens(f))

    for xPos, first_line in lines[:-1]:
        for yPos, second_line in lines[xPos+1:]:
            if first_line == second_line:
                if (xPos, yPos) in possible_line_continuations:
                    possible_line_continuations[xPos + 1, yPos + 1] =\
                    possible_line_continuations.pop((xPos, yPos))
                else:
                    possible_line_continuations[xPos + 1, yPos + 1] = (xPos, yPos)
                x_positions.append(xPos)
                y_positions.append(yPos)
    for after_line_end in possible_line_continuations.iterkeys():
        start = possible_line_continuations[after_line_end]
        stop = (after_line_end[0]-1, after_line_end[1]-1)
        if start != stop:
            lines_x.extend(range(start[0] - 1, after_line_end[0]))
            lines_y.extend(range(start[1] - 1, after_line_end[1]))
    plot(x_positions, y_positions, 'b.')
    plot(lines_x, lines_y, 'ro')
    show()

if __name__ == '__main__':
    

    from optparse import OptionParser
    usage = ("usage: %prog [options] filename [filenames]\n" +
             "Show duplicated lines in filename.\n" + 
             "If more than one file is specified, show duplicates " +
             "in all of them")
    parser = OptionParser(usage=usage)
    available_parsers = ['text', 'python']
    parser.add_option("-p", "--parser", dest="parse_with", type='choice',
                      choices=available_parsers,
                      help="specify parser to use\n%s" % available_parsers, metavar='PARSER')
    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose", default=False,
                      help="print additional informations to stderr")

    (options, args) = parser.parse_args()
    if not args:
        parser.print_help()
        sys.exit(2)
    show_similiarities(args)
# vim: ts=4,et,sw=4

    

