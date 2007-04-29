'''Show similarities in a text file, graphically'''

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.pylab import plot, show
import sys
import optparse
import tokenize
import itertools

def get_line_tokens(line_producer, start_token=None, ignore_these = ('\n', '')):
    lineiter = iter(line_producer)
    lineno = 0 
    while True:
        line = lineiter.next()
        if line not in ignore_these:
            tok_start = lineno, 0
            tok_end = lineno, len(line)
            yield tok_start, tok_end, line
        lineno += 1

def get_python_tokens(line_producer, start_token=None, ignore_these = ('\n', '')):
    lineiter = iter(line_producer)
    for token in tokenize.generate_tokens(lineiter.next):
        (tok_type,
         tok_string,
         tok_start,
         tok_end,
         tok_line) = token
        yield tok_start, tok_end, tok_string
        print tok_string

def similiar_tokens(filenames, get_tokens):
    files = [open(filename, 'r') for filename in filenames[0:]]
    tokens = []
    for f in files:
        tokens.extend(list(get_tokens(f)))
    print len(files)
    c =  itertools.chain([get_tokens(f) for f in files])
    lines = list(enumerate(tokens))
    for xPos, x_token in lines[:-1]:
        for yPos, y_token in lines[xPos+1:]:
            (tok_start, tok_end, first_line) = x_token
            (tok_start, tok_end, second_line) = y_token
            if first_line == second_line:
                yield xPos, x_token, yPos, y_token

def show_similiarities(filenames, get_tokens = get_line_tokens, verbose=False):
    x_positions = []
    y_positions = []

    #
    possible_line_continuations = {}
    for (xPos, (_, _, first_line),
         yPos, (_, _, second_line)) in similiar_tokens(filenames, get_tokens):
                if (xPos, yPos) in possible_line_continuations:
                    possible_line_continuations[xPos + 1, yPos + 1] =\
                    possible_line_continuations.pop((xPos, yPos))
                else:
                    possible_line_continuations[xPos + 1, yPos + 1] = (xPos, yPos)
                x_positions.append(xPos)
                y_positions.append(yPos)
    make_plot(x_positions, y_positions, possible_line_continuations, verbose)

def make_plot(x_positions, y_positions, possible_line_continuations, verbose=False):
    lines_x = []
    lines_y = []

    for after_line_end in possible_line_continuations.iterkeys():
        start = possible_line_continuations[after_line_end]
        stop = (after_line_end[0]-1, after_line_end[1]-1)
        if start != stop:
            lines_x.extend(range(start[0] - 1, after_line_end[0]))
            lines_y.extend(range(start[1] - 1, after_line_end[1]))
    if verbose:
        plot(x_positions, y_positions, 'b.')
    plot(lines_x, lines_y, 'ro')
    show()

PARSERS = {
            'text' : get_line_tokens,
            'python' : get_python_tokens,
          }

if __name__ == '__main__':

    from optparse import OptionParser
    usage = ("usage: %prog [options] filename [filenames]\n" +
             "Show duplicated lines in filename.\n" + 
             "If more than one file is specified, show duplicates " +
             "in all of them")
    parser = OptionParser(usage=usage)
    available_parsers = PARSERS.keys() 
    parser.add_option("-p", "--parser", dest="parse_with", type='choice',
                      choices=available_parsers, default='text',
                      help="specify parser to use\n%s" % available_parsers, metavar='PARSER')
    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose", default=False,
                      help="print additional informations to stderr")

    (options, args) = parser.parse_args()
    print args
    if not args:
        parser.print_help()
        sys.exit(2)
    show_similiarities(args, get_tokens=PARSERS[options.parse_with], verbose=options.verbose)

# vim: ts=4 et sw=4

    

