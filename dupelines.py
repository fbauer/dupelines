'''Show similarities in a text file, graphically'''

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.pylab import plot, show
import sys
import optparse
import tokenize
import itertools
import time
# try:
#     import psyco
#     print 'wheeeee!!'
#     psyco.profile()
# except ImportError:
#     print 'no psyco'
    

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

def similiar_tokens(filenames, get_tokens):
    files = [open(filename, 'r') for filename in filenames[0:]]
    tokens = []
    for f in files:
        tokens.extend(list(get_tokens(f)))
    lines = list(enumerate(tokens))
#     for xPos, x_token in lines[:-1]:
#         for yPos, y_token in lines[xPos+1:]:
#             (tok_start, tok_end, first_line) = x_token
#             (tok_start, tok_end, second_line) = y_token
#             if first_line == second_line:
#                 yield xPos, x_token, yPos, y_token
    all_toks = {}
    for pos, (tok_start, tok_end, token) in lines:
        if token in all_toks:
            all_toks[token].append((pos, tok_start, tok_end))
        else:
            # we haven't seen this token before
            all_toks[token] = [(pos, tok_start, tok_end)]
    #for token, stuff in all_toks.iteritems():
    #for token, stuff in all_toks.iteritems():
    for xpos, (xstart, xend, token) in lines:
        # we can pop the first element from all_toks[token]
        # as it is xpos
        stuff = all_toks[token][1:]
        all_toks[token] = stuff
        if stuff   and token not in ('\n', ''):
            #for xpos, xstart, xend in stuff:
            for ypos, ystart, yend in stuff:
                assert ypos > xpos
                print xpos, ypos
                yield xpos, (xstart, xend, token), ypos, (ystart, yend, token)
 
def show_similiarities(filenames, get_tokens = get_line_tokens, verbose=False):
    
    x_positions = []
    y_positions = []
    cand_start = cand_end = None
    #
    possible_line_continuations = {}
    for (xPos, (_, _, first_line),
         yPos, (_, _, second_line)) in similiar_tokens(filenames, get_tokens):
                if (xPos, yPos) == cand_end: 
                    cand_end = (xPos+1, yPos+1)
                else:
                    if cand_end and (cand_end[0] - cand_start[0] > 1):
                        possible_line_continuations[(cand_end[0]+1,cand_end[1]+1)] = cand_start
                    cand_start = (xPos, yPos)
                    cand_end = (xPos+1, yPos+1)

                #print 'Appending point'
                x_positions.append(xPos)
                y_positions.append(yPos)
    print 'done'
    return x_positions, y_positions, possible_line_continuations


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
    if not args:
        parser.print_help()
        sys.exit(2)
    start_time = time.time()
    x_positions, y_positions, possible_line_continuations = show_similiarities(
                       args, get_tokens=PARSERS[options.parse_with], verbose=options.verbose)
    stop_time = time.time()
    print 'elapsed time %.2f seconds' % (stop_time - start_time)
    make_plot(x_positions, y_positions, possible_line_continuations, verbose=options.verbose)
# vim: ts=4 et sw=4
